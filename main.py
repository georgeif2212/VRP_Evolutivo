import sys
import math
import random
from typing import Dict, List, Tuple


def extract_instance_variables(lines: List[str]) -> Tuple[int, int, int, int]:

    num_trucks = -1
    optimal_value = -1
    dimension = -1
    capacity = -1

    for line in lines:
        if line.startswith("COMMENT"):
            parts = line.split()
            num_trucks_index = parts.index("trucks:") + 1
            optimal_value_index = parts.index("value:") + 1
            num_trucks = int(parts[num_trucks_index].replace(",", ""))
            optimal_value_str = parts[optimal_value_index].rstrip(")")
            optimal_value = int(optimal_value_str)

        elif line.startswith("DIMENSION"):
            dimension = int(line.split()[-1])

        elif line.startswith("CAPACITY"):
            capacity = int(line.split()[-1])

        elif line.startswith("NODE_COORD_SECTION"):
            break

    return num_trucks, optimal_value, dimension, capacity


def euclidean_distance(point1: Tuple[float, float],
                       point2: Tuple[float, float],
                       decimal_places: int = 2) -> float:

    x1, y1 = point1
    x2, y2 = point2
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    return round(distance, decimal_places)


def read_customer_data(file_path:
                       str) -> Tuple[Dict[int, Tuple[float, float]],
                                     Dict[int, int]]:

    customer_coordinates: Dict[int, Tuple[float, float]] = {}
    customer_demands: Dict[int, int] = {}
    in_node_coord_section = False
    in_demand_section = False

    with open(file_path, "r") as file:
        lines = file.readlines()

    for line in lines:
        if line.startswith("NODE_COORD_SECTION"):
            in_node_coord_section = True
            continue

        elif line.startswith("DEMAND_SECTION"):
            in_node_coord_section = False
            in_demand_section = True
            continue

        elif line.startswith("DEPOT_SECTION"):
            break

        if in_node_coord_section:
            parts = line.split()
            node_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            customer_coordinates[node_id] = (x, y)

        elif in_demand_section:
            parts = line.split()
            node_id = int(parts[0])
            demand = int(parts[1])
            customer_demands[node_id] = demand

    return customer_coordinates, customer_demands


def calculate_distance_matrix(customer_coordinates: Dict[int,
                              Tuple[float, float]]) -> List[List[float]]:

    num_customers = len(customer_coordinates)
    distance_matrix = [[0.0] * (num_customers + 1)
                       for _ in range(num_customers + 1)]

    for i in range(1, num_customers + 1):
        for j in range(1, num_customers + 1):
            if i != j:
                distance = euclidean_distance(
                    customer_coordinates[i], customer_coordinates[j])
                distance_matrix[i][j] = round(distance, 2)

    return distance_matrix


def print_problem_info(file_path: str) -> None:

    with open(file_path, "r") as file:
        lines = file.readlines()

    print("PROBLEM INFORMATION")
    problem_info = []
    for line in lines:
        if line.strip() == "NODE_COORD_SECTION":
            break
        problem_info.append(line.strip())

    print("\n".join(problem_info))


def print_customer_demands(customer_demands: Dict[int, int]) -> None:

    print("\nDEMANDAS DE CLIENTES:")
    for node_id, demand in customer_demands.items():
        print(f"Cliente {node_id}: Demanda {demand}")


def print_distance_matrix(distance_matrix: List[List[float]]) -> None:

    num_customers = len(distance_matrix) - 1

    print("\nDISTANCE MATRIX:")
    print("  0.00 ", end="")

    formatted_numbers = ["{:.2f}".format(float(x))
                         for x in range(1, num_customers + 1)]
    print(" ".join(map(lambda x: x.rjust(6), formatted_numbers)))

    for i in range(1, len(distance_matrix)):
        row = [i] + distance_matrix[i][1:]
        formatted_row = ["{:.2f}".format(float(x)) for x in row]
        print(" ".join(map(lambda x: x.rjust(6), formatted_row)))


def read_routes_data(file_path: str) -> List[List[int]]:

    routes = []
    with open(file_path, "r") as file:
        for line in file:
            if line.startswith("Route #"):
                route_str = line.strip().split(": ")[1]
                route = [int(node) for node in route_str.split()]
                routes.append(route)
    return routes


def print_routes(routes: List[List[int]]) -> None:

    print("\nRUTAS ASIGNADAS A LOS CAMIONES:")
    for i, route in enumerate(routes):
        print(f"Camión #{i + 1}: {' '.join(map(str, route))}")


def initialize_routes(num_clients: int, trucks: int, probability:
                      float) -> List[List[int]]:

    routes = [[] for _ in range(trucks)]
    aux = [i for i in range(num_clients)]

    i = 0
    while aux:
        num_aleatorio = random.random()

        if probability < num_aleatorio:
            position = random.randint(0, len(aux) - 1)

            routes[i % trucks].append(aux[position])
            aux.pop(position)

        i += 1

    max_length = len(routes)

    for j in range(trucks):
        last_element = routes[j][-1]
        length = len(routes[j])

        while length <= num_clients - 1:
            routes[j].append(last_element)
            length += 1

    return routes


def main(instance_file, routes_file):

    with open(instance_file, "r") as file:
        lines = file.readlines()

    customer_coordinates, customer_demands = read_customer_data(instance_file)
    extracted_variables = extract_instance_variables(lines)
    num_trucks, optimal_value, dimension, capacity = extracted_variables
    result_routes = read_routes_data(routes_file)
    distance_matrix = calculate_distance_matrix(customer_coordinates)
    probability = 0.65

    # print_problem_info(instance_file)
    #
    # print("\nINSTANCE DATA:")
    # print(f"num_trucks: {num_trucks}")
    # print(f"optimal_value: {optimal_value}")
    # print(f"dimension: {dimension}")
    # print(f"capacity: {capacity}")
    #
    # print_customer_demands(customer_demands)
    # print_distance_matrix(distance_matrix)
    # print_routes(result_routes)

    #####################
    initial_routes = initialize_routes(dimension, num_trucks, probability)
    print(initial_routes)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py instance_file routes_file")
    else:
        instance_file = sys.argv[1]
        routes_file = sys.argv[2]
        main(instance_file, routes_file)
