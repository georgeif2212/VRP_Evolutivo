from ReadInstance import *


def generate_initial_routes(num_clients: int, num_trucks: int, probability:
                            float) -> List[List[int]]:

    routes = [[] for _ in range(num_trucks)]
    aux = [i for i in range(num_clients)]
    i = 0

    while aux:
        num_aleatorio = random.random()

        # TODO: Cambiar en base a la porbabilidad y a la capacidad
        # deacuerdo a la demanda
        if probability < num_aleatorio:
            position = random.randint(0, len(aux) - 1)

            routes[i % num_trucks].append(aux[position])
            aux.pop(position)

        i += 1

    #  NOTE: Es "mejor" así ya que se puede trabjar y se ahorra memory
    return routes
    # return fill_initial_routes(routes, num_clients, num_trucks)


def fill_initial_routes(routes: List[List[int]], num_clients: int,
                        num_trucks: int) -> List[List[int]]:

    max_length = len(routes)

    for j in range(num_trucks):
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

    # WARNING: En construcción...
    routes = generate_initial_routes(dimension, num_trucks, probability)
    for route in routes:
        print(route)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script_name.py instance_file routes_file")
    else:
        instance_file = sys.argv[1]
        routes_file = sys.argv[2]
        main(instance_file, routes_file)
