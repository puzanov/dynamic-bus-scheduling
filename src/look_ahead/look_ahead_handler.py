#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
Copyright 2016 Eleftherios Anagnostopoulos for Ericsson AB

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from src.mongodb_database.mongo_connection import MongoConnection
from src.common.logger import log
from src.common.variables import mongodb_host, mongodb_port
from src.route_generator.route_generator_client import get_route_between_multiple_bus_stops, \
    get_waypoints_between_multiple_bus_stops
from datetime import datetime, timedelta


class LookAheadHandler(object):
    def __init__(self):
        self.bus_stops_dictionary = {}
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='look_ahead_handler', log_type='DEBUG', log_message='connection ok')

    def initialize_connection(self):
        self.connection = MongoConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='look_ahead_handler', log_type='DEBUG', log_message='connection ok')

    def retrieve_bus_stops_dictionary(self):
        """
        Retrieve a dictionary containing all the documents of the BusStops collection.

        bus_stops_dictionary: {name -> {'osm_id', 'point': {'longitude', 'latitude'}}}
        """
        self.bus_stops_dictionary = self.connection.get_bus_stops_dictionary()
        log(module_name='look_ahead_handler', log_type='DEBUG', log_message='bus_stops_dictionary ok')

    def generate_bus_line(self, line_id, bus_stop_names):
        """

        :param line_id: integer
        :param bus_stop_names: [string]
        :return:
        """
        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='get_waypoints_between_multiple_bus_stops (route_generator): starting')
        route_generator_response = get_waypoints_between_multiple_bus_stops(bus_stop_names=bus_stop_names)
        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='get_waypoints_between_multiple_bus_stops (route_generator): finished')
        # [{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'waypoints': [[{'_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                   'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        #                   'max_speed', 'road_type', 'way_id', 'traffic_density'}]]}]

        bus_stops = []
        starting_bus_stop_controller = True

        for intermediate_response in route_generator_response:
            starting_bus_stop = intermediate_response.get('starting_bus_stop')
            ending_bus_stop = intermediate_response.get('ending_bus_stop')
            waypoints = intermediate_response.get('waypoints')
            lists_of_edge_object_ids = []

            for list_of_edges in waypoints:
                list_of_edge_object_ids = []

                for edge in list_of_edges:
                    edge_object_id = edge.get('_id')
                    list_of_edge_object_ids.append(edge_object_id)

                lists_of_edge_object_ids.append(list_of_edge_object_ids)

            # waypoints: [[edge_object_id]]
            waypoints = lists_of_edge_object_ids
            self.connection.insert_bus_stop_waypoints(starting_bus_stop=starting_bus_stop,
                                                      ending_bus_stop=ending_bus_stop,
                                                      waypoints=waypoints)

            if starting_bus_stop_controller:
                bus_stops.append(starting_bus_stop)
                starting_bus_stop_controller = False

            bus_stops.append(ending_bus_stop)

        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='bus_stop_waypoints (mongodb_database): ok')

        self.connection.insert_bus_line(line_id=line_id, bus_stops=bus_stops)

        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='bus_line (mongodb_database): ok')

    def generate_bus_line_timetable(self, line_id):
        """

        :param line_id: integer
        :return:
        """
        starting_datetime = datetime(2016, 7, 11, 0, 0, 0, 00000)
        current_datetime = starting_datetime
        timetable = []

        # {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        bus_line = self.connection.find_bus_line(line_id=line_id)
        bus_stops = bus_line.get('bus_stops')

        # [{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        #             'distances_from_starting_node', 'times_from_starting_node',
        #             'distances_from_previous_node', 'times_from_previous_node'}}]
        route_generator_response = get_route_between_multiple_bus_stops(bus_stops=bus_stops)

        for intermediate_response in route_generator_response:
            starting_bus_stop = unicode(intermediate_response.get('starting_bus_stop').get('name')).encode('utf-8')
            ending_bus_stop = unicode(intermediate_response.get('ending_bus_stop').get('name')).encode('utf-8')
            intermediate_route = intermediate_response.get('route')
            total_time = intermediate_route.get('total_time')

            timetable.append({'starting_bus_stop': starting_bus_stop,
                              'ending_bus_stop': ending_bus_stop,
                              'departure_datetime': current_datetime,
                              'arrival_datetime': current_datetime + timedelta(minutes=total_time/60)})

            current_datetime += timedelta(minutes=total_time//60+1)

        for timetable_entry in timetable:
            starting_bus_stop = str(timetable_entry.get('starting_bus_stop'))
            departure_datetime = str(timetable_entry.get('departure_datetime'))
            ending_bus_stop = str(timetable_entry.get('ending_bus_stop'))
            arrival_datetime = str(timetable_entry.get('arrival_datetime'))
            print 'starting_bus_stop: ' + starting_bus_stop + \
                  ' - departure_datetime: ' + departure_datetime + \
                  ' - ending_bus_stop: ' + ending_bus_stop + \
                  ' - arrival_datetime: ' + arrival_datetime

    def generate_bus_line_timetables(self, line_id, timetable_starting_datetime, timetable_ending_datetime):
        """

        :param line_id:
        :param timetable_starting_datetime:
        :param timetable_ending_datetime:
        :return: [[{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                    'departure_datetime', 'arrival_datetime', 'total_time',
                    'travel_requests', 'average_waiting_time'}]]
        """
        timetables = []

        # 1: The list of bus stops corresponding to the provided bus_line_id is retrieved from the database.
        # bus_line: {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        bus_line = self.connection.find_bus_line(line_id=line_id)
        bus_stops = bus_line.get('bus_stops')

        # [{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #   'route': {'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        #             'distances_from_starting_node', 'times_from_starting_node',
        #             'distances_from_previous_node', 'times_from_previous_node'}}]
        route_generator_response = get_route_between_multiple_bus_stops(bus_stops=bus_stops)

        current_datetime = timetable_starting_datetime

        while current_datetime < timetable_ending_datetime:
            timetable = []

            for intermediate_response in route_generator_response:
                starting_bus_stop = intermediate_response.get('starting_bus_stop')
                ending_bus_stop = intermediate_response.get('ending_bus_stop')
                intermediate_route = intermediate_response.get('route')
                total_time = intermediate_route.get('total_time')

                timetable_entry = {'starting_bus_stop': starting_bus_stop,
                                   'ending_bus_stop': ending_bus_stop,
                                   'departure_datetime': current_datetime,
                                   'arrival_datetime': current_datetime + timedelta(minutes=total_time/60),
                                   'total_time': total_time,
                                   'travel_requests': [],
                                   'average_waiting_time': 0}

                timetable.append(timetable_entry)
                current_datetime += timedelta(minutes=total_time//60+1)

            timetables.append(timetable)

        # for timetable in timetables:
        #     print timetable
        return timetables

    def test_look_ahead(self, line_id, timetable_starting_datetime, timetable_ending_datetime,
                        requests_min_departure_datetime, requests_max_departure_datetime, bus_capacity,
                        minimum_number_of_passengers):

        # 1: The list of bus stops corresponding to the provided bus_line_id is retrieved from the database.
        #
        # bus_line: {'_id', 'line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]}
        bus_line = self.connection.find_bus_line(line_id=line_id)
        bus_stops = bus_line.get('bus_stops')

        # 2: The list of travel requests with departure datetime between the requests_min_departure_datetime
        #    and requests_max_departure_datetime is retrieved from the database.
        #
        # travel_requests_list: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id', 'starting_bus_stop',
        #                         'ending_bus_stop', 'departure_datetime', 'arrival_datetime'}]
        travel_requests_list = self.connection.get_travel_requests_list_based_on_bus_line_id_and_departure_datetime(
            bus_line_id=line_id,
            min_departure_datetime=requests_min_departure_datetime,
            max_departure_datetime=requests_max_departure_datetime
        )
        self.correspond_travel_requests_to_bus_stops(
            travel_requests=travel_requests_list,
            bus_stop_osm_ids=[bus_stop.get('osm_id') for bus_stop in bus_stops]
        )

        # 3:
        #
        # timetables: [[{'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #                'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #                'departure_datetime', 'arrival_datetime', 'total_time',
        #                'travel_requests', 'average_waiting_time'}]]
        timetables = self.generate_bus_line_timetables(
            line_id=line_id,
            timetable_starting_datetime=timetable_starting_datetime,
            timetable_ending_datetime=timetable_ending_datetime
        )

        # for timetable in timetables:
        #     print timetable

        # 4:
        #
        for travel_request in travel_requests_list:
            starting_bus_stop_index = travel_request.get('starting_bus_stop_index')
            # print starting_bus_stop_index

            for timetable in timetables:
                corresponding_timetable_entry = timetable[starting_bus_stop_index]
                print corresponding_timetable_entry
                # print travel_request.get('starting_bus_stop').get('name'), \
                #     corresponding_timetable_entry.get('starting_bus_stop').get('name')

    def correspond_travel_requests_to_bus_stops(self, travel_requests, bus_stop_osm_ids):
        """

        :param travel_requests: [{'_id', 'travel_request_id, 'client_id', 'bus_line_id',
                                  'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                  'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
                                  'departure_datetime', 'arrival_datetime'}]
        :param bus_stop_osm_ids: [osm_id]
        :return:
        """
        for travel_request in travel_requests:
            starting_bus_stop_osm_id = travel_request.get('starting_bus_stop').get('osm_id')
            starting_bus_stop_index = self.get_bus_stop_index(
                bus_stop_osm_id=starting_bus_stop_osm_id,
                bus_stop_osm_ids=bus_stop_osm_ids,
                start=0
            )
            travel_request['starting_bus_stop_index'] = starting_bus_stop_index

            ending_bus_stop_osm_id = travel_request.get('ending_bus_stop').get('osm_id')
            ending_bus_stop_index = self.get_bus_stop_index(
                bus_stop_osm_id=ending_bus_stop_osm_id,
                bus_stop_osm_ids=bus_stop_osm_ids,
                start=starting_bus_stop_index + 1
            )
            travel_request['ending_bus_stop_index'] = ending_bus_stop_index

    @staticmethod
    def get_bus_stop_index(bus_stop_osm_id, bus_stop_osm_ids, start):
        bus_stop_index = -1

        for i in range(start, len(bus_stop_osm_ids)):
            if bus_stop_osm_id == bus_stop_osm_ids[i]:
                bus_stop_index = i
                break

        return bus_stop_index


