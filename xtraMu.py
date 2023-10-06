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


def generate_initial_solutions(num_clients: int, num_trucks: int, probability:
                               float, capacity: int, demand_per_client:
                               Dict[int, int], num_solutions:
                               int) -> List[List[List[int]]]:

    initial_solutions = []

    for _ in range(num_solutions):
        initial_solution = generate_initial_routes(
            num_clients, num_trucks, probability, capacity, demand_per_client)
        initial_solutions.append(initial_solution)

    return initial_solutions


def generate_initial_routes(num_clients: int, num_trucks: int, probability:
                            float, capacity: int, demand_per_client:
                            Dict[int, int]) -> List[List[int]]:

    routes = [[] for _ in range(num_trucks)]
    aux = list(range(2, num_clients))  # TEST: SE CAMBIÓ EL 1 POR EL 2
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

    # for route in routes:
    #     x = calculate_route_weight(route, demand_per_client)
    #     print(f"{route} -> {x}")
    #
    # print("")
    # print(routes)

    return routes


def calculate_route_cost(route: List[int], distance_matrix: List[List[
                         float]]) -> float:
    cost = 0.0
    num_clients = len(route)

    for i in range(num_clients - 1):
        initial = route[i]
        final = route[i + 1]
        cost += distance_matrix[initial][final]

    # cost += distance_matrix[route[-1]][route[0]]
    # TEST: SE AGREGA EL DEPOSITO
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


def mutation(solution: List[List[int]], minimo: int, maximo: int, num_clients:
             int, num_trucks: int, capacity: int,
             demand_per_client) -> List[List[int]]:

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

        client1_idx = random.randint(0, len(mutated_solution[route1_idx]) - 1)
        client2_idx = random.randint(0, len(mutated_solution[route2_idx]) - 1)

        client1 = mutated_solution[route1_idx].pop(client1_idx)
        client2 = mutated_solution[route2_idx].pop(client2_idx)

        mutated_solution[route1_idx].append(client2)
        mutated_solution[route2_idx].append(client1)

        # TEST: Verificar si las rutas son válidas después de la mutación
        if is_route_valid(mutated_solution[route1_idx], demand_per_client,
                          capacity) and is_route_valid(mutated_solution[
                              route2_idx], demand_per_client, capacity):
            return mutated_solution


def ee(num_generaciones: int, distance_matrix: List[List[float]],
       optimal_value: int, dimension: int, num_trucks: int, capacity,
       demand_per_client, probability) -> Tuple[List[List[int]], float]:

    # TODO:
    # Se crea una poblcion de  individuos (permutaciones) aleatorios
    # BUG: ¡AL TIRO! A VECES SE MUERE PA
    poblacion_inicial = generate_initial_solutions(
        dimension, num_trucks, probability, capacity, demand_per_client, mu)
    aptitudes = [evaluate_solution(solution, distance_matrix)
                 for solution in poblacion_inicial]

    # for x in poblacion_inicial:
    #     for y in x:
    #         print(y)
    #     print("")
    #
    print(f"Aptitudes: {aptitudes}")
    print("")

    # TODO:
    # Se ordena el conjunto
    combination = list(zip(poblacion_inicial, aptitudes))
    combination = sorted(combination, key=lambda x: x[1])

    poblacion_inicial = [elem[0] for elem in combination[:mu]]
    aptitudes = [elem[1] for elem in combination[:mu]]

    mejor_poblacion = poblacion_inicial[0]
    mejor_aptitud = aptitudes[0]

    # print(mejor_poblacion)
    # print(mejor_aptitud)

    generacion = 0
    generacionesSinMejora = 0
    generacionMejor = 0
    # best_solution = initial_solution
    # best_solution_cost = evaluate_solution(best_solution, distance_matrix)

    while (generacionesSinMejora < num_generaciones):
        generacion = generacion + 1

        # TODO:
        # Se mutan los individuos actuales x para obtener
        # los nuevos individuos x'
        # y se evalua x' en la funcion de aptitud
        # xprima, aptitudprima = mutarPoblacion(x, d, mut, l)
        poblacion_prima = []
        for poblacion in poblacion_inicial:
            poblacion_prima.append(mutation(poblacion, 1, 100,
                                            dimension, num_trucks, capacity,
                                            demand_per_client))

        aptitudes_primas = [evaluate_solution(solution, distance_matrix)
                            for solution in poblacion_prima]

        # print("")
        # print(f"Aptitudes: {aptitudes}")
        # print(f"AptitudesPrimas: {aptitudes_primas}")

        # print("")
        # print("AQUI")
        # for x in poblacion_inicial:
        #     for y in x:
        #         print(y)
        #     print("")
        # print("ODA")
        # for x in poblacion_prima:
        #     for y in x:
        #         print(y)
        #     print("")

        # TODO:
        # Se mezclan los invidiuos originales y
        # los resultados de la mutacion
        # x.extend(xprima)
        # aptitud.extend(aptitudprima)
        poblacion_inicial.extend(poblacion_prima)
        aptitudes.extend(aptitudes_primas)

        # TODO:
        # Se ordena el conjunto
        combination = list(zip(poblacion_inicial, aptitudes))
        combination = sorted(combination, key=lambda x: x[1])

        # TODO:
        # Se seleccionan los mejores mu
        # x = [elem[0] for elem in comb[:m]]
        # aptitud = [elem[1] for elem in comb[:m]]
        poblacion_inicial = [elem[0] for elem in combination[:mu]]
        aptitudes = [elem[1] for elem in combination[:mu]]

        # TODO:
        # Si la solucion actual x' es mejor que x,
        # se actualiza x
        # if aptitud[0] > mejoraptitud:
        #     mejorx = x[0]
        #     mejoraptitud = aptitud[0]
        #     generacionMejor = generacion
        #     generacionesSinMejora = 0
        # else:
        #     generacionesSinMejora = generacionesSinMejora + 1
        if aptitudes[0] > mejor_aptitud:
            mejor_poblacion = poblacion_inicial[0]
            mejor_aptitud = aptitudes[0]
            generacionMejor = generacion
            generacionesSinMejora = 0
        else:
            generacionesSinMejora = generacionesSinMejora + 1

        # for x in poblacion_inicial:
        #     for y in x:
        #         print(y)
        #     print("")

        print(f"Aptitudes: {aptitudes}")
        # print(poblacion_inicial[0])
        print("")

        # TODO:
        # regresar lo mejor
        # return poblacion_inicial[0], (-1 * aptitudes[0]), generacionMejor,
        # generacion

    # while generacion < num_iterations:
    #     # Se incrementa la generacion
    #     # TODO:
    #     generacion += 1
    #
    #     # Se muta el vector actual x para obtener x_prima
    #     # TODO:
    #     new_solution = mutation(best_solution, 1, 100,
    #                             dimension, num_trucks, capacity,
    #                             demand_per_client)
    #
    #     # Se evalua x_prima en la funcion objetivo
    #     # TODO:
    #     new_solution_cost = evaluate_solution(new_solution, distance_matrix)
    #     # print(initial_solution)
    #     # print(new_solution)
    #     # return
    #
    #     # Si la mutación x_prima es factible y es mejor que x,
    #     # se reemplazan x, el valor y el peso
    #     # TODO:
    #     if (new_solution_cost <= best_solution_cost
    #             or new_solution_cost == optimal_value):
    #         best_solution = new_solution
    #         best_solution_cost = new_solution_cost
    #
    # # Al finalizar el ciclo, se regresan x, el valor y el peso
    # # TODO:
    # return best_solution, best_solution_cost


def main(instance_file, routes_file, num_iterations, mu, lambdaVar):

    with open(instance_file, "r") as file:
        lines = file.readlines()

    customer_coordinates, customer_demands = read_customer_data(instance_file)
    extracted_variables = extract_instance_variables(lines)
    num_trucks, optimal_value, dimension, capacity = extracted_variables
    result_routes = read_routes_data(routes_file)
    distance_matrix = calculate_distance_matrix(customer_coordinates)
    probability = 0.666

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

    # NOTE:
    # initial_solution = generate_initial_routes(
    #     dimension, num_trucks, probability, capacity, customer_demands)
    # print("SOLUCIÓN INICIAL ")
    # for route in initial_solution:
    #     print(route)

    # print(f"MU {mu}")
    # print(f"LAMDA {lambdaVar}")

    # for route in initial_solution:
    #     print(route)
    #     route_cost = calculate_route_cost(route, distance_matrix)
    #     print(f"Costo de ruta inicial: {route_cost}")

    # total_cost_initial_solution = evaluate_solution(
    #     initial_solution, distance_matrix)

    #  WARNING: En construcción...
    for iteracion in range(num_iterations):
        best_solution, best_solution_cost = ee(
            num_iterations, distance_matrix,
            optimal_value, dimension, num_trucks, capacity, customer_demands,
            probability)
    #
    # print("")
    # print("Mejor solución encontrada:")
    # # print(best_solution, end="\n\n")
    # for solution in best_solution:
    #     print(solution)
    # print("")
    #
    # for route in best_solution:
    #     print(route)
    #     route_demand = calculate_route_weight(route, customer_demands)
    #     print(f"Demanda de la ruta => {route_demand}")
    # print("")
    #
    # xtra = set(tuple(item) for item in best_solution)
    # # xtra.add(1)
    # # print(type(xtra))
    # if len(xtra) == len(best_solution):
    #     print("BIEEEEEEN!")
    # else:
    #     print("MAAAAAALLL!")
    #
    # print("Solución optima del problema:")
    # for result in result_routes:
    #     print(result)
    #
    # print(
    #     f"\nCosto total de la solución inicial: {total_cost_initial_solution}")
    #
    # BLACK_TEXT_LIGHT_PINK_BG = "\033[97;48;5;54m"
    # RESET = "\033[0m"
    # best_solution_cost_str = str(best_solution_cost)
    # print("Costo de la mejor solución encontrada: " +
    #       BLACK_TEXT_LIGHT_PINK_BG + best_solution_cost_str + RESET)
    #
    # ORANGE_TEXT_BLACK_BG = "\033[97;48;5;202m"
    # RESET = "\033[0m"
    # optimal_value_str = str(optimal_value)
    # print("Costo de la solución optima del problema: " +
    #       ORANGE_TEXT_BLACK_BG + optimal_value_str + RESET)
    #
    # # print(f"Costo de la mejor solución encontrada: {best_solution_cost}")
    # # print(f"Costo de la solution optima del problema: {optimal_value}")
    #
    # # best_solution_cost = optimal_value
    # if best_solution_cost == optimal_value:
    #     BLACK_TEXT_LIGHT_PINK_BG = "\033[30;105m"
    #     RESET = "\033[0m"
    #     print(BLACK_TEXT_LIGHT_PINK_BG + "¡LO LOGASTE!" + RESET)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script_name.py instance_file routes_file num_iterations mu lambdaVar")
    else:
        instance_file = sys.argv[1]
        routes_file = sys.argv[2]
        num_iterations = int(sys.argv[3])
        mu = int(sys.argv[4])
        lambdaVar = int(sys.argv[5])
        main(instance_file, routes_file, num_iterations, mu, lambdaVar)
