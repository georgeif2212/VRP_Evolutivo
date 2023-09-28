from ReadInstance import *


def swap_elements(lst: List, position1: int, position2: int) -> None:
    tmp = lst[position1]
    lst[position1] = lst[position2]
    lst[position2] = tmp


def generate_initial_routes(num_clients: int, num_trucks: int, probability:
                            float, capacity: int,
                            demand_per_client: Dict[int,
                                                    int]) -> List[List[int]]:

    routes = [[] for _ in range(num_trucks)]
    aux = list(demand_per_client.keys())
    current_demand_per_client = [0] * num_clients
    i = 0

    while aux:
        num_aleatorio = random.random()

        if probability < num_aleatorio:
            position = random.randint(0, len(aux) - 1)
            client = aux[position]

            calculated_route = i % num_trucks

            if current_demand_per_client[calculated_route] + demand_per_client[
                    client] <= capacity:

                routes[calculated_route].append(client)

                current_demand_per_client[
                    calculated_route] += demand_per_client[client]

                swap_elements(aux, position, -1)

                aux.pop()

            i += random.randint(1, len(aux) + 1)

    x = [[demand_per_client[client] for client in route] for route in routes]
    for y in x:
        print(y, end=" ")
        print(f"suma-> {sum(y)}")

    print("")
    return routes


def main(instance_file, routes_file):

    with open(instance_file, "r") as file:
        lines = file.readlines()

    customer_coordinates, customer_demands = read_customer_data(instance_file)
    extracted_variables = extract_instance_variables(lines)
    num_trucks, optimal_value, dimension, capacity = extracted_variables
    result_routes = read_routes_data(routes_file)
    distance_matrix = calculate_distance_matrix(customer_coordinates)
    probability = 0.77

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

    # WARNING: En construcción...
    routes = generate_initial_routes(
        dimension, num_trucks, probability, capacity, customer_demands)
    for route in routes:
        print(route)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py instance_file routes_file")
    else:
        instance_file = sys.argv[1]
        routes_file = sys.argv[2]
        main(instance_file, routes_file)
