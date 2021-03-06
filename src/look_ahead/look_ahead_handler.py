#!/usr/local/bin/python
# -*- coding: utf-8 -*-
"""
- LICENCE

The MIT License (MIT)

Copyright (c) 2016 Eleftherios Anagnostopoulos for Ericsson AB (EU FP7 CityPulse Project)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


- DESCRIPTION OF DOCUMENTS

-- MongoDB Database Documents:

address_document: {
    '_id', 'name', 'node_id', 'point': {'longitude', 'latitude'}
}
bus_line_document: {
    '_id', 'bus_line_id', 'bus_stops': [{'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}}]
}
bus_stop_document: {
    '_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}
}
bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_object_id]]
}
bus_vehicle_document: {
    '_id', 'bus_vehicle_id', 'maximum_capacity',
    'routes': [{'starting_datetime', 'ending_datetime', 'timetable_id'}]
}
detailed_bus_stop_waypoints_document: {
    '_id', 'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[edge_document]]
}
edge_document: {
    '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
    'max_speed', 'road_type', 'way_id', 'traffic_density'
}
node_document: {
    '_id', 'osm_id', 'tags', 'point': {'longitude', 'latitude'}
}
point_document: {
    '_id', 'osm_id', 'point': {'longitude', 'latitude'}
}
timetable_document: {
    '_id', 'timetable_id', 'bus_line_id', 'bus_vehicle_id',
    'timetable_entries': [{
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime', 'number_of_onboarding_passengers',
        'number_of_deboarding_passengers', 'number_of_current_passengers',
        'route': {
            'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
            'distances_from_starting_node', 'times_from_starting_node',
            'distances_from_previous_node', 'times_from_previous_node'
        }
    }],
    'travel_requests': [{
        '_id', 'client_id', 'bus_line_id',
        'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        'departure_datetime', 'arrival_datetime',
        'starting_timetable_entry_index', 'ending_timetable_entry_index'
    }]
}
traffic_event_document: {
    '_id', 'event_id', 'event_type', 'event_level', 'point': {'longitude', 'latitude'}, 'datetime'
}
travel_request_document: {
    '_id', 'client_id', 'bus_line_id',
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'departure_datetime', 'arrival_datetime',
    'starting_timetable_entry_index', 'ending_timetable_entry_index'
}
way_document: {
    '_id', 'osm_id', 'tags', 'references'
}

-- Route Generator Responses:

get_route_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}
get_route_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'route': {
        'total_distance', 'total_time', 'node_osm_ids', 'points', 'edges',
        'distances_from_starting_node', 'times_from_starting_node',
        'distances_from_previous_node', 'times_from_previous_node'
    }
}]
get_waypoints_between_two_bus_stops: {
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}
get_waypoints_between_multiple_bus_stops: [{
    'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
    'waypoints': [[{
        '_id', 'starting_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'ending_node': {'osm_id', 'point': {'longitude', 'latitude'}},
        'max_speed', 'road_type', 'way_id', 'traffic_density'
    }]]
}]
"""
from src.common.parameters import mongodb_host, mongodb_port
from src.mongodb_database.mongodb_database_connection import MongodbDatabaseConnection
from src.route_generator.route_generator_client import get_waypoints_between_two_bus_stops
from src.common.logger import log
from src.look_ahead.timetable_generator import *
from src.look_ahead.timetable_updater import *

__author__ = 'Eleftherios Anagnostopoulos'
__email__ = 'eanagnostopoulos@hotmail.com'
__credits__ = [
    'Azadeh Bararsani (Senior Researcher at Ericsson AB) - email: azadeh.bararsani@ericsson.com'
    'Aneta Vulgarakis Feljan (Senior Researcher at Ericsson AB) - email: aneta.vulgarakis@ericsson.com'
]


class LookAheadHandler(object):
    def __init__(self):
        self.mongodb_database_connection = MongodbDatabaseConnection(host=mongodb_host, port=mongodb_port)
        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='mongodb_database_connection: established')

    def generate_bus_line(self, bus_stop_names, bus_line_id=None):
        """
        Generate a bus_line, consisted of a bus_line_id and a list of bus_stops, and store it to the corresponding
        collection of the System Database. Moreover, identify all the possible waypoints between the bus_stops
        of the bus_line, and populate the BusStopWaypoints collection.

        :param bus_stop_names: [string]
        :param bus_line_id: int
        :return: None
        """
        # 1: The inputs: bus_line_id and bus_stop_names are provided to the function, so as as a bus_line
        #    with the corresponding bus_line_id and bus_stops to be generated.
        #
        # 2: The Look Ahead connects to the System Database and retrieves the bus_stops which correspond to
        #    the provided bus_stop_names. The function returns None and the bus_line is not generated,
        #    in case there is a bus_stop_name which does not correspond to a stored bus_stop.
        #
        if bus_line_id is None:
            maximum_bus_line_id = self.mongodb_database_connection.get_maximum_or_minimum(collection='bus_line')
            bus_line_id = maximum_bus_line_id + 1

        bus_stops = []

        for bus_stop_name in bus_stop_names:
            bus_stop_document = self.mongodb_database_connection.find_bus_stop_document(name=bus_stop_name)

            if bus_stop_document is None:
                log_message = 'find_bus_stop_document (mongodb_database) - name:', bus_stop_name, '- result: None'
                log(module_name='look_ahead_handler', log_type='DEBUG', log_message=log_message)
                return None
            else:
                bus_stops.append(bus_stop_document)

        # 3: The intermediate waypoints of the bus_routes, which are generated while combining starting and
        #    ending bus_stops of the bus_line, should be stored as bus_stop_waypoints_documents at the System Database.
        #    The Look Ahead checks the existing bus_stop_waypoints_documents and communicates with the Route Generator
        #    in order to identify the waypoints of the bus_routes which are not already stored. The newly generated
        #    bus_stop_waypoints_documents are getting stored to the corresponding collection of the System Database.
        #    The function returns None and the bus_line is not generated, in case the Route Generator can not identify
        #    a possible route in order to connect the bus_stops of the bus_line.
        #
        number_of_bus_stops = len(bus_stops)

        for i in range(0, number_of_bus_stops - 1):
            starting_bus_stop = bus_stops[i]
            ending_bus_stop = bus_stops[i + 1]

            bus_stop_waypoints_document = self.mongodb_database_connection.find_bus_stop_waypoints_document(
                starting_bus_stop=starting_bus_stop,
                ending_bus_stop=ending_bus_stop
            )
            if bus_stop_waypoints_document is None:
                route_generator_response = get_waypoints_between_two_bus_stops(
                    starting_bus_stop=starting_bus_stop,
                    ending_bus_stop=ending_bus_stop
                )
                if route_generator_response is None:
                    log(module_name='look_ahead_handler', log_type='DEBUG',
                        log_message='get_waypoints_between_two_bus_stops (route_generator): None')
                    return None
                else:
                    waypoints = route_generator_response.get('waypoints')

                    if len(waypoints) == 0:
                        log(module_name='look_ahead_handler', log_type='DEBUG',
                            log_message='get_waypoints_between_two_bus_stops (route_generator): None')
                        return None

                    lists_of_edge_object_ids = []

                    for list_of_edges in waypoints:
                        list_of_edge_object_ids = []

                        for edge in list_of_edges:
                            edge_object_id = edge.get('_id')
                            list_of_edge_object_ids.append(edge_object_id)

                        lists_of_edge_object_ids.append(list_of_edge_object_ids)

                    # waypoints: [[edge_object_id]]
                    #
                    waypoints = lists_of_edge_object_ids

                    self.mongodb_database_connection.insert_bus_stop_waypoints_document(
                        starting_bus_stop=starting_bus_stop,
                        ending_bus_stop=ending_bus_stop,
                        waypoints=waypoints
                    )

        # 4: The Look Ahead stores the newly generated bus_line_document, which is consisted of the bus_line_id
        #    and the list of bus_stops, to the corresponding collection of the System Database.
        #    In case there is an already existing bus_line_document, with the same bus_line_id,
        #    then the list of bus_stops gets updated.
        #
        bus_line_document = {'bus_line_id': bus_line_id, 'bus_stops': bus_stops}
        self.mongodb_database_connection.insert_bus_line_document(bus_line_document=bus_line_document)

        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='insert_bus_line_document (mongodb_database): ok')

    def generate_timetables_for_bus_line(self, timetables_starting_datetime, timetables_ending_datetime,
                                         requests_min_departure_datetime, requests_max_departure_datetime,
                                         bus_line=None, bus_line_id=None):
        """
        Generate timetables for a bus_line, for a selected datetime period,
        evaluating travel_requests of a specific datetime period.

        - The input: timetables_starting_datetime and input: timetables_ending_datetime
          are provided to the function, so as timetables for the specific datetime period
          to be generated.

        - The input: requests_min_departure_datetime and input: requests_max_departure_datetime
          are provided to the function, so as travel_requests with departure_datetime corresponding
          to the the specific datetime period to be evaluated.

        - The input: bus_line or input: bus_line_id is provided to the function,
          so as timetables for the specific bus_line to be generated.

        :param timetables_starting_datetime: datetime
        :param timetables_ending_datetime: datetime
        :param requests_min_departure_datetime: datetime
        :param requests_max_departure_datetime: datetime
        :param bus_line: bus_line_document
        :param bus_line_id: int
        :return: None
        """

        maximum_timetable_id_in_database = self.mongodb_database_connection.get_maximum_or_minimum(
            collection='timetable'
        )

        # 1: The list of bus_stops corresponding to the provided bus_line is retrieved.
        #
        # bus_stop_document: {
        #     '_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}
        # }
        # bus_stops: [bus_stop_document]
        #
        if bus_line is None and bus_line_id is None:
            return None
        elif bus_line is None:
            bus_line = self.mongodb_database_connection.find_bus_line_document(bus_line_id=bus_line_id)
        else:
            bus_line_id = bus_line.get('bus_line_id')

        bus_stops = bus_line.get('bus_stops')

        # 2: The Look Ahead retrieves from the System Database the travel_requests with
        #    departure_datetime higher than requests_min_departure_datetime and
        #    lower than requests_max_departure_datetime.
        #
        # travel_request_document: {
        #     '_id', 'client_id', 'bus_line_id',
        #     'starting_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #     'ending_bus_stop': {'_id', 'osm_id', 'name', 'point': {'longitude', 'latitude'}},
        #     'departure_datetime', 'arrival_datetime'
        # }
        # travel_requests: [travel_request_document]
        #
        travel_requests = self.mongodb_database_connection.find_travel_request_documents(
            bus_line_ids=[bus_line_id],
            min_departure_datetime=requests_min_departure_datetime,
            max_departure_datetime=requests_max_departure_datetime
        )

        # 3: (TimetableGenerator is initialized) The Look Ahead sends a request to the Route Generator so as
        #    to identify the less time-consuming bus_route between the bus_stops of bus_line,
        #    while taking into consideration the current levels of traffic density.
        #
        timetable_generator = TimetableGenerator(
            maximum_timetable_id_in_database=maximum_timetable_id_in_database,
            bus_line_id=bus_line_id,
            bus_stops=bus_stops,
            travel_requests=travel_requests
        )

        # The list of bus_stops of a bus_line might contain the same bus_stop_osm_ids more than once.
        # For this reason, each travel_request needs to be related with the correct index in the bus_stops list.
        # So, the values 'starting_timetable_entry_index' and 'ending_timetable_entry_index' are estimated.
        #
        correspond_travel_requests_to_bus_stops(
            travel_requests=timetable_generator.travel_requests,
            bus_stops=timetable_generator.bus_stops
        )

        # 4: Based on the response of the Route Generator, which includes details about the followed bus_route,
        #    and using only one bus vehicle, the Look Ahead generates some initial timetables which cover the
        #    whole datetime period from timetables_starting_datetime to timetables_ending_datetime.
        #    Initially, the list of travel requests of these timetables is empty, and the departure_datetime and
        #    arrival_datetime values of the timetable_entries are based exclusively on the details of the bus_route.
        #    In the next steps of the algorithm, these timetables are used in the initial clustering
        #    of the travel requests.
        #
        timetable_generator.timetables = generate_initial_timetables(
            bus_line_id=bus_line_id,
            timetables_starting_datetime=timetables_starting_datetime,
            timetables_ending_datetime=timetables_ending_datetime,
            route_generator_response=timetable_generator.route_generator_response
        )

        current_average_waiting_time_of_timetables = float('Inf')

        while True:
            new_timetables = generate_new_timetables_based_on_travel_requests(
                current_timetables=timetable_generator.timetables,
                travel_requests=timetable_generator.travel_requests
            )
            new_average_waiting_time_of_timetables = calculate_average_waiting_time_of_timetables_in_seconds(
                timetables=new_timetables
            )
            if new_average_waiting_time_of_timetables < current_average_waiting_time_of_timetables:
                timetable_generator.timetables = new_timetables
                current_average_waiting_time_of_timetables = new_average_waiting_time_of_timetables
                print_timetables(timetables=timetable_generator.timetables)
            else:
                break

        print_timetables(timetables=timetable_generator.timetables)

        self.mongodb_database_connection.delete_timetable_documents(
            bus_line_id=bus_line.get('bus_line_id')
        )
        self.mongodb_database_connection.insert_timetable_documents(
            timetable_documents=timetable_generator.timetables
        )
        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='insert_timetable_documents (mongodb_database): ok')

    def generate_timetables_for_bus_lines(self, timetables_starting_datetime, timetables_ending_datetime,
                                          requests_min_departure_datetime, requests_max_departure_datetime):
        """
        Generate timetables for all bus_lines, for a selected datetime period,
        evaluating travel_requests of a specific datetime period.

        :param timetables_starting_datetime: datetime
        :param timetables_ending_datetime: datetime
        :param requests_min_departure_datetime: datetime
        :param requests_max_departure_datetime: datetime
        :return: None
        """
        bus_lines = self.mongodb_database_connection.find_bus_line_documents()

        for bus_line in bus_lines:
            self.generate_timetables_for_bus_line(
                bus_line=bus_line,
                timetables_starting_datetime=timetables_starting_datetime,
                timetables_ending_datetime=timetables_ending_datetime,
                requests_min_departure_datetime=requests_min_departure_datetime,
                requests_max_departure_datetime=requests_max_departure_datetime
            )

    def update_timetables_of_bus_line(self, bus_line=None, bus_line_id=None):
        """
        Update the timetables of a bus_line, taking into consideration the current levels of traffic_density.

        :param bus_line: bus_line_document
        :param bus_line_id: int
        :return: None
        """
        if bus_line is None and bus_line_id is None:
            return None
        elif bus_line is None:
            bus_line = self.mongodb_database_connection.find_bus_line_document(bus_line_id=bus_line_id)
        else:
            bus_line_id = bus_line.get('bus_line_id')

        bus_stops = bus_line.get('bus_stops')
        timetables = self.mongodb_database_connection.find_timetable_documents(bus_line_ids=[bus_line_id])
        travel_requests = get_travel_requests_of_timetables(timetables=timetables)

        timetable_updater = TimetableUpdater(
            bus_stops=bus_stops,
            timetables=timetables,
            travel_requests=travel_requests
        )
        update_entries_of_timetables(
            timetables=timetable_updater.timetables,
            route_generator_response=timetable_updater.route_generator_response
        )
        current_average_waiting_time_of_timetables = calculate_average_waiting_time_of_timetables_in_seconds(
            timetables=timetable_updater.timetables
        )
        print_timetables(timetables=timetable_updater.timetables)

        while True:
            new_timetables = generate_new_timetables_based_on_travel_requests(
                current_timetables=timetable_updater.timetables,
                travel_requests=timetable_updater.travel_requests
            )
            new_average_waiting_time_of_timetables = calculate_average_waiting_time_of_timetables_in_seconds(
                timetables=new_timetables
            )
            if new_average_waiting_time_of_timetables < current_average_waiting_time_of_timetables:
                timetable_updater.timetables = new_timetables
                current_average_waiting_time_of_timetables = new_average_waiting_time_of_timetables
                print_timetables(timetables=timetable_updater.timetables)
            else:
                break

        print_timetables(timetables=timetable_updater.timetables)

        self.mongodb_database_connection.delete_timetable_documents(
            bus_line_id=bus_line.get('bus_line_id')
        )
        self.mongodb_database_connection.insert_timetable_documents(
            timetable_documents=timetable_updater.timetables
        )
        log(module_name='look_ahead_handler', log_type='DEBUG',
            log_message='update_timetable_documents (mongodb_database): ok')

    def update_timetables_of_bus_lines(self):
        """
        Update the timetables of all bus_lines, taking into consideration the current levels of traffic_density.

        :return: None
        """
        bus_lines = self.mongodb_database_connection.find_bus_line_documents()

        for bus_line in bus_lines:
            self.update_timetables_of_bus_line(bus_line=bus_line)


def generate_new_timetables_based_on_travel_requests(current_timetables, travel_requests):
    """
    This function is capable of generating new_timetables, evaluating a list of travel_requests.
    Initially, the timetables_entries of new_timetables are based on the corresponding timetable_entries
    of current_timetables, and  their travel_requests entry is empty. In the next processing steps,
    each travel_request is corresponded to the new_timetable which produces the minimum_individual_waiting_time
    for the passenger, while updating in parallel the timetable_entries of new_timetables.

    :param current_timetables: [timetable_document]
    :param travel_requests: [travel_request_document]
    :return: new_timetables: [timetable_document]
    """
    # The timetables_entries of new_timetables are initialized, based on the corresponding timetable_entries
    # of current_timetables, and their travel_requests entry is empty.
    new_timetables = generate_additional_timetables(timetables=current_timetables)

    # 6: (Initial Clustering) Each one of the retrieved travel_requests is corresponded to the timetable
    #    which produces the minimum_individual_waiting_time for the passenger. The waiting time is calculated
    #    as the difference between the departure_datetime of the travel_request and the departure_datetime of
    #    the timetable_entry from where the passenger departs from (identified by the
    #    'starting_timetable_entry_index' value).
    #
    correspond_travel_requests_to_timetables(
        travel_requests=travel_requests,
        timetables=new_timetables
    )

    # 7: (Handling of Undercrowded Timetables) After the initial clustering step, there might be timetables
    #    where the number of travel_requests is lower than the input: minimum_number_of_passengers_in_timetable.
    #    This is usual during night hours, where transportation demand is not so high. These timetables are
    #    removed from the list of generated timetables and each one of their travel_requests is corresponded
    #    to one of the remaining timetables, based on the individual_waiting_time of the passenger.
    #
    travel_requests_of_undercrowded_timetables = handle_undercrowded_timetables(timetables=new_timetables)
    correspond_travel_requests_to_timetables(
        travel_requests=travel_requests_of_undercrowded_timetables,
        timetables=new_timetables
    )

    # 8: (Handling of Overcrowded Timetables) In addition, there might be timetables where the
    #    number_of_current_passengers is higher than the input: maximum_bus_capacity, which indicates that
    #    each one of these timetables cannot be served by one bus vehicle. For this reason, each one of these
    #    timetables should be divided into two timetables, and the corresponding travel_requests are partitioned.
    #    The whole procedure is repeated until there is no timetable where the number_of_current_passengers
    #    exceeds the maximum_bus_capacity.
    #
    #    The first step is to calculate the number_of_current_passengers in each one of the timetable_entries.
    #
    calculate_number_of_passengers_of_timetables(timetables=new_timetables)
    handle_overcrowded_timetables(timetables=new_timetables)

    # 9: (Adjust Departure Datetimes) At this point of processing, the number of travel_requests in each timetable
    #    is higher than the minimum_number_of_passengers_in_timetable and lower than the maximum_bus_capacity.
    #    So, the departure_datetime and arrival_datetime values of each timetable_entry are re-estimated,
    #    taking into consideration the departure_datetime values of the corresponding travel_requests.
    #    In each timetable and for each travel_request, the ideal departure_datetimes from all bus_stops
    #    (not only the bus stop from where the passenger desires to depart) are estimated. Then, the ideal
    #    departure_datetimes of the timetable, for each bus stop, correspond to the mean values of the ideal
    #    departure_datetimes of the corresponding travel_requests. Finally, starting from the initial bus_stop
    #    and combining the ideal departure_datetimes of each bus_stop and the required traveling time between
    #    bus_stops, included in the response of the Route Generator, the departure_datetimes of the
    #    timetable_entries are finalized.
    adjust_departure_datetimes_of_timetables(timetables=new_timetables)

    # 10: (Individual Waiting Time) For each timetable, the individual_waiting_time of each passenger is calculated.
    #     For each one of the travel_requests where individual_waiting_time is higher than the
    #     input: individual_waiting_time_threshold, alternative existing timetables are investigated, based on the
    #     new individual_waiting_time, the average_waiting_time and the number_of_current_passengers of each
    #     timetable. For the travel_requests which cannot be served by the other existing timetables, if their
    #     number is greater or equal than the mini_number_of_passengers_in_timetable, then a new timetable is
    #     generated with departure_datetimes based on the ideal departure_datetimes of the
    #     aforementioned passengers.
    #
    # handle_travel_requests_of_timetables_with_waiting_time_above_threshold(
    #     timetables=new_timetables
    # )
    # calculate_number_of_passengers_of_timetables(timetables=new_timetables)
    # adjust_departure_datetimes_of_timetables(timetables=new_timetables)

    # 11: (Average Waiting Time) For each timetable, the average_waiting_time of passengers is calculated.
    #     If the average waiting time is higher than the input: average-waiting-time-threshold, then the
    #     possibility of dividing the timetable is investigated. If the two new timetables have lower
    #     average_waiting_time than the initial one and both have more travel_requests than the
    #     minimum_number_of_passengers_in_timetable, then the initial timetable is divided, its travel_requests
    #     are partitioned, and the departure_datetime and arrival_datetime values of the timetable_entries of
    #     the new timetables, are estimated based on the departure_datetime values of the partitioned requests.
    #
    handle_timetables_with_average_waiting_time_above_threshold(timetables=new_timetables)
    calculate_number_of_passengers_of_timetables(timetables=new_timetables)
    adjust_departure_datetimes_of_timetables(timetables=new_timetables)

    return new_timetables


def get_travel_requests_of_timetables(timetables):
    """
    Retrieve a list containing all the travel_request_documents,
    which are included in a list of timetable_documents.

    :param timetables: [timetable_documents]
    :return: travel_requests: [travel_request_documents]
    """
    travel_requests = []

    for timetable in timetables:
        travel_requests_of_timetable = timetable.get('travel_requests')
        travel_requests.extend(travel_requests_of_timetable)

    return travel_requests
