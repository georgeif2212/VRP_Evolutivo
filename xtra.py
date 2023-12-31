from ReadInstance import *


def swap_elements(lst: List, position1: int, position2: int) -> None:
    tmp = lst[position1]
    lst[position1] = lst[position2]
    lst[position2] = tmp

def calculate_route_weight(route: List[int], demand_per_client: Dict[int,
                           int]) -> int:
    return sum(demand_per_client[client] for client in route if client != 0)


def is_route_valid(route: List[int], demand_per_client: Dict[int, int],
                   capacity: int) -> bool:
    route_weight = calculate_route_weight(route, demand_per_client)
    return route_weight <= capacity


def generate_initial_routes(num_clients: int, num_trucks: int, probability:
                            float, capacity: int, demand_per_client:
                            Dict[int, int]) -> List[List[int]]:
    routes = [[] for _ in range(num_trucks)]
    aux = list(range(2, num_clients))  
    current_demand_per_client = [0] * num_clients
    i = 0

    while aux:
        num_aleatorio = random.random()

        if probability < num_aleatorio:
            position = random.randint(0, len(aux) - 1)
            client = aux[position]
            calculated_route = i % num_trucks

            # Verifica si agregar el cliente cumple con la capacidad de la ruta
            if current_demand_per_client[calculated_route] + demand_per_client[
                    client] <= capacity:
                routes[calculated_route].append(client)
                current_demand_per_client[calculated_route
                                          ] += demand_per_client[client]
                swap_elements(aux, position, -1)
                aux.pop()

            i += random.randint(1, len(aux) + 1)


    return routes


def calculate_route_cost(route: List[int], distance_matrix: List[List[
                         float]]) -> float:
    cost = 0.0
    num_clients = len(route)

    for i in range(num_clients - 1):
        initial = route[i]
        final = route[i + 1]
        cost += distance_matrix[initial][final]

    cost += distance_matrix[route[-1]][1]
    cost += distance_matrix[route[0]][1]

    return cost


def evaluate_solution(solution: List[List[int]], distance_matrix: List[List[
                      float]]) -> float:
    total_cost = 0.0
    for route in solution:
        route_cost = calculate_route_cost(route, distance_matrix)
        total_cost += route_cost

    return total_cost


def mutation(solution, minimo, maximo, num_clients, num_trucks, capacity, demand_per_client):
    mutated_solution = [route.copy() for route in solution]
    mutation_probability = random.random()
    while True:
        non_empty_routes = [i for i in range(
            len(mutated_solution)) if mutated_solution[i]]
        if len(non_empty_routes) < 2:
            return mutated_solution
        route1_idx = random.choice(non_empty_routes)
        non_empty_routes.remove(route1_idx)
        route2_idx = random.choice(non_empty_routes)
        # Decide si realizar una mutación de intercambio de valores o cambiar la longitud de las listas
        if random.random() < mutation_probability:
            # Mutación de intercambio de valores
            if len(mutated_solution[route1_idx]) > 0 and len(mutated_solution[route2_idx]) > 0:
                client1_idx = random.randint(
                    0, len(mutated_solution[route1_idx]) - 1)
                client2_idx = random.randint(
                    0, len(mutated_solution[route2_idx]) - 1)
                client1 = mutated_solution[route1_idx].pop(client1_idx)
                client2 = mutated_solution[route2_idx].pop(client2_idx)
                # Verifica si los valores son distintos antes de intercambiar
                if client1 != client2:
                    mutated_solution[route1_idx].append(client2)
                    mutated_solution[route2_idx].append(client1)
        else:
            # Cambiar la longitud de las listas
            # Asegura que al menos un cliente permanezca en la lista
            if len(mutated_solution[route1_idx]) > 1:
                client_to_move = random.choice(mutated_solution[route1_idx])
                mutated_solution[route1_idx].remove(client_to_move)
                mutated_solution[route2_idx].append(client_to_move)

        # Verificar si las rutas son válidas después de la mutación
        is_valid = all(is_route_valid(route, demand_per_client, capacity)
                       for route in mutated_solution)
        if is_valid:
            return mutated_solution


def ee(initial_solution: List[List[int]], num_iterations: int,
       distance_matrix: List[List[float]], optimal_value: int,
       dimension: int, num_trucks: int, capacity, demand_per_client) -> Tuple[
        List[List[int]], float]:

    generacion = 0
    best_solution = initial_solution
    best_solution_cost = evaluate_solution(best_solution, distance_matrix)

    while generacion < num_iterations:
        # Se incrementa la generacion
        # TODO:
        generacion += 1

        # Se muta el vector actual x para obtener x_prima
        # TODO:
        new_solution = mutation(best_solution, 1, 100,
                                dimension, num_trucks, capacity,
                                demand_per_client)

        # print("mutación")
        # for x in new_solution:
        #     print(x)
        # print("")

        # Se evalua x_prima en la funcion objetivo
        # TODO:
        new_solution_cost = evaluate_solution(new_solution, distance_matrix)
        # print(initial_solution)
        # print(new_solution)
        # return

        # Si la mutación x_prima es factible y es mejor que x,
        # se reemplazan x, el valor y el peso
        # TODO:
        if (new_solution_cost <= best_solution_cost
                or new_solution_cost == optimal_value):
            best_solution = new_solution
            best_solution_cost = new_solution_cost

    # Al finalizar el ciclo, se regresan x, el valor y el peso
    # TODO:
    return best_solution, best_solution_cost


def main(instance_file, routes_file, num_iterations):

    with open(instance_file, "r") as file:
        lines = file.readlines()

    customer_coordinates, customer_demands = read_customer_data(instance_file)
    extracted_variables = extract_instance_variables(lines)
    num_trucks, optimal_value, dimension, capacity = extracted_variables
    result_routes = read_routes_data(routes_file)
    distance_matrix = calculate_distance_matrix(customer_coordinates)
    probability = 0.77

    print_problem_info(instance_file)

    # print("\nINSTANCE DATA:")
    # print(f"num_trucks: {num_trucks}")
    # print(f"optimal_value: {optimal_value}")
    # print(f"dimension: {dimension}")
    # print(f"capacity: {capacity}")
    #
    # print_customer_demands(customer_demands)
    # print_distance_matrix(distance_matrix)
    # print_routes(result_routes)

    initial_solution = generate_initial_routes(
        dimension, num_trucks, probability, capacity, customer_demands)

    # print("SOLUCIÓN INICIAL ")
    # print(initial_solution)

    # for route in initial_solution:
    #     print(route)
    #     route_cost = calculate_route_cost(route, distance_matrix)
    #     print(f"Costo de ruta inicial: {route_cost}")

    total_cost_initial_solution = evaluate_solution(
        initial_solution, distance_matrix)

    # # WARNING: En construcción...
    best_solution, best_solution_cost = ee(
        initial_solution, num_iterations, distance_matrix,
        optimal_value, dimension, num_trucks, capacity, customer_demands)

    print("")
    print("Mejor solución encontrada:")
    # print(best_solution, end="\n\n")
    for solution in best_solution:
        print(solution)
    print("")

    for route in best_solution:
        print(route)
        route_demand = calculate_route_weight(route, customer_demands)
        print(f"Demanda de la ruta => {route_demand}")
    print("")

    xtra = set(tuple(item) for item in best_solution)
    # xtra.add(1)
    # print(type(xtra))
    if len(xtra) == len(best_solution):
        print("BIEEEEEEN!")
    else:
        print("MAAAAAALLL!")

    print("Solución optima del problema:")
    for result in result_routes:
        print(result)

    print(
        f"\nCosto total de la solución inicial: {total_cost_initial_solution}")

    BLACK_TEXT_LIGHT_PINK_BG = "\033[97;48;5;54m"
    RESET = "\033[0m"
    best_solution_cost_str = str(best_solution_cost)
    print("Costo de la mejor solución encontrada: " +
          BLACK_TEXT_LIGHT_PINK_BG + best_solution_cost_str + RESET)

    ORANGE_TEXT_BLACK_BG = "\033[97;48;5;202m"
    RESET = "\033[0m"
    optimal_value_str = str(optimal_value)
    print("Costo de la solución optima del problema: " +
          ORANGE_TEXT_BLACK_BG + optimal_value_str + RESET)

    # print(f"Costo de la mejor solución encontrada: {best_solution_cost}")
    # print(f"Costo de la solution optima del problema: {optimal_value}")

    # best_solution_cost = optimal_value
    if best_solution_cost == optimal_value:
        BLACK_TEXT_LIGHT_PINK_BG = "\033[30;105m"
        RESET = "\033[0m"
        print(BLACK_TEXT_LIGHT_PINK_BG + "¡LO LOGASTE!" + RESET)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py instance_file routes_file")
    else:
        instance_file = sys.argv[1]
        routes_file = sys.argv[2]
        num_iterations = int(sys.argv[3])
        main(instance_file, routes_file, num_iterations)
