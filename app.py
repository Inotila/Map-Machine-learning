from flask import Flask, jsonify
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt
import heapq

app = Flask(__name__)

class Places(Enum):
    GARDEN_MALL = 1
    POLICE_STATION = 2
    LIBRARY = 3
    OUT_STATION = 4
    UNIVERSITY_SCHOOL = 5
    CLUB = 6
    PARK_STATION = 7
    EDU_STATION = 8
    DUCK_PARK = 9
    PRETEND_PARK = 10
    EMPTY = 11

class Street:
    def __init__(self, name, street_name, method_of_transport, weather, distance, duration):
        self.name = name
        self.street_name = street_name
        self.method_of_transport = method_of_transport
        self.weather = weather
        self.distance = distance
        self.duration = duration

class FakeCityGraph:
    def __init__(self):
        self.adjacency_list = {}

    def add_place(self, name):
        if name not in self.adjacency_list:
            self.adjacency_list[name] = []

    def add_street(self, place1, place2, street_name, method_of_transport, weather, distance, duration):
        self.adjacency_list[place1].append(Street(place2, street_name, method_of_transport, weather, distance, duration))
        self.adjacency_list[place2].append(Street(place1, street_name, method_of_transport, weather, distance, duration))

    def dijkstra_shortest_path(self, source, target):
        G = self._build_networkx_graph()
        try:
            path = nx.dijkstra_path(G, source, target, weight='duration')
            return self._calculate_total_duration(path)
        except nx.NodeNotFound:
            return None
        except nx.NetworkXNoPath:
            return None

    def a_star_shortest_path(self, source, target):
        G = self._build_networkx_graph()
        try:
            path = nx.astar_path(G, source, target, weight='duration')
            return self._calculate_total_duration(path)
        except nx.NodeNotFound:
            return None
        except nx.NetworkXNoPath:
            return None

    def _build_networkx_graph(self):
        G = nx.Graph()
        for place, streets in self.adjacency_list.items():
            for street in streets:
                G.add_edge(place, street.name, weight=street.duration)
        return G

    def _calculate_total_duration(self, path):
        total_duration = 0
        for i in range(len(path) - 1):
            place1 = path[i]
            place2 = path[i + 1]
            street_obj = [street for street in self.adjacency_list[place1] if street.name == place2][0]
            total_duration += street_obj.duration
        return total_duration

fake_city_graph = FakeCityGraph()

# Add places and streets to the fake city graph
fake_city_graph.add_place(Places.GARDEN_MALL)
fake_city_graph.add_place(Places.POLICE_STATION)
fake_city_graph.add_place(Places.LIBRARY)
fake_city_graph.add_place(Places.OUT_STATION)
fake_city_graph.add_place(Places.UNIVERSITY_SCHOOL)
fake_city_graph.add_place(Places.CLUB)
fake_city_graph.add_place(Places.PARK_STATION)
fake_city_graph.add_place(Places.EDU_STATION)
fake_city_graph.add_place(Places.DUCK_PARK)
fake_city_graph.add_place(Places.PRETEND_PARK)
fake_city_graph.add_place(Places.EMPTY) 

fake_city_graph.add_street(Places.GARDEN_MALL, Places.DUCK_PARK, "System street", "walking_and_cycling", "cloudy", 4, 4)
fake_city_graph.add_street(Places.GARDEN_MALL, Places.PRETEND_PARK, "Bob street", "driving", "sunny", 5, 5)
fake_city_graph.add_street(Places.GARDEN_MALL, Places.POLICE_STATION, "Tom street", "walking_and_cycling", "sunny", 10, 10)
fake_city_graph.add_street(Places.GARDEN_MALL, Places.LIBRARY, "Eveline street", "driving", "cloudy", 8, 8)
fake_city_graph.add_street(Places.LIBRARY, Places.DUCK_PARK, "Caro street", "walking_and_cycling", "cloudy", 3, 3)
fake_city_graph.add_street(Places.LIBRARY, Places.PARK_STATION, "Walkie street", "walking_and_cycling", "cloudy", 3, 3)
fake_city_graph.add_street(Places.GARDEN_MALL, Places.UNIVERSITY_SCHOOL, "blue street", "walking_and_cycling", "sunny", 10, 10)
fake_city_graph.add_street(Places.POLICE_STATION, Places.OUT_STATION, "Law street", "driving", "sunny", 4, 4)
fake_city_graph.add_street(Places.POLICE_STATION, Places.PRETEND_PARK, "Tedstreet", "driving", "sunny", 4, 4)
fake_city_graph.add_street(Places.OUT_STATION, Places.UNIVERSITY_SCHOOL, "2K street", "driving", "rainy", 5, 5)
fake_city_graph.add_street(Places.OUT_STATION, Places.EDU_STATION, "red street", "bus_and_train", "cloudy", 8, 8)
fake_city_graph.add_street(Places.UNIVERSITY_SCHOOL, Places.CLUB, "nice street", "driving", "sunny", 10, 10)
fake_city_graph.add_street(Places.CLUB, Places.PARK_STATION, "ka street", "walking_and_cycling", "cloudy", 1, 1)
fake_city_graph.add_street(Places.PARK_STATION, Places.EDU_STATION, "long street", "bus_and_train", "cloudy", 8, 8)

@app.route('/<source>/<target>', methods=['GET'])
def shortest_path_duration(source, target):
    source = Places[source.upper()]
    target = Places[target.upper()]
    dijkstra_duration = fake_city_graph.dijkstra_shortest_path(source, target)
    a_star_duration = fake_city_graph.a_star_shortest_path(source, target)
    return jsonify({
        "source": source.name,
        "target": target.name,
        "dijkstra_duration": dijkstra_duration,
        "a_star_duration": a_star_duration,
        "confidence": "high" if dijkstra_duration == a_star_duration else "low"
    })

if __name__ == "__main__":
    app.run(debug=True)