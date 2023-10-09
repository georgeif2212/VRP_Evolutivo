from ReadInstance import *
from typing import List
from random import choice


def swap_elements(lst: List, position1: int, position2: int) -> None:
    tmp = lst[position1]
    lst[position1] = lst[position2]
    lst[position2] = tmp


def calculate_route_weight(route: List[int], demand_per_client: Dict[int, int]) -> int:
    return sum(demand_per_client[client] for client in route if client != 0)


def is_route_valid(
    route: List[int], demand_per_client: Dict[int, int], capacity: int
) -> bool:
    route_weight = calculate_route_weight(route, demand_per_client)
    return route_weight <= capacity


def generate_initial_solutions(
    num_clients: int,
    num_trucks: int,
    probability: float,
    capacity: int,
    demand_per_client: Dict[int, int],
    num_solutions: int,
) -> List[List[List[int]]]:
    initial_solutions = []

    for _ in range(num_solutions):
        initial_solution = generate_initial_routes(
            num_clients, num_trucks, probability, capacity, demand_per_client
        )
        initial_solutions.append(initial_solution)

    return initial_solutions


def generate_initial_routes(
    num_clients: int,
    num_trucks: int,
    probability: float,
    capacity: int,
    demand_per_client: Dict[int, int],
) -> List[List[int]]:
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
            if (
                current_demand_per_client[calculated_route] +
                    demand_per_client[client]
                <= capacity
            ):
                routes[calculated_route].append(client)
                current_demand_per_client[calculated_route] += demand_per_client[client]
                swap_elements(aux, position, -1)
                aux.pop()

            i += random.randint(1, len(aux) + 1)

    #     # for route in routes:
    #     #     x = calculate_route_weight(route, demand_per_client)
    #     #     print(f"{route} -> {x}")
    #     #
    #     # print("")
    #     # print(routes)

    return routes


# def generate_initial_routes(
#     num_clients: int,
#     num_trucks: int,
#     probability: float,
#     capacity: int,
#     demand_per_client: Dict[int, int],
# ) -> List[List[int]]:
#     while True:
#         solucionInicial = random.sample(range(2, num_clients + 1), num_clients - 1)
#         numeros_aleatorios = random.sample(range(len(solucionInicial)), num_trucks - 1)
#         # Ordenar los números de menor a mayor
#         numeros_ordenados = sorted(numeros_aleatorios)

#         # Dividir la solución mutada en rutas usando los índices generados aleatoriamente
#         routes = []
#         start_idx = 0
#         for end_idx in numeros_ordenados:
#             routes.append(solucionInicial[start_idx:end_idx])
#             start_idx = end_idx
#         # Agregar la última ruta
#         routes.append(solucionInicial[start_idx:])

#         all_routes_valid = all(
#             is_route_valid(route, demand_per_client, capacity) for route in routes
#         )

#         # Si todas las rutas son válidas, retornar la lista de rutas
#         if all_routes_valid:
#             # print("ROUTES", routes)
#             return routes


def calculate_route_cost(route: List[int], distance_matrix: List[List[float]]) -> float:
    cost = 0.0
    num_clients = len(route)

    for i in range(num_clients - 1):
        initial = route[i]
        final = route[i + 1]
        cost += distance_matrix[initial][final]

    # cost += distance_matrix[route[-1]][route[0]]
    # TEST: SE AGREGA EL DEPOSITO
    # print("OJO")
    # print(route)
    # print(route[-1])
    cost += distance_matrix[route[-1]][1]
    cost += distance_matrix[route[0]][1]

    return cost


def evaluate_solution(
    solution: List[List[int]], distance_matrix: List[List[float]]
) -> float:
    total_cost = 0.0
    for route in solution:
        route_cost = calculate_route_cost(route, distance_matrix)
        total_cost += route_cost

    return total_cost


def chooseMutation(solution, mut):
    if mut == "int":
        solutionPrima = intercambio(solution)
    elif mut == "ins":
        solutionPrima = insercion(solution)
    elif mut == "inv":
        solutionPrima = inversion(solution)
    else:
        if random() <= 1.0 / 3:
            solutionPrima = insercion(solution)
        elif random() <= 0.5:
            solutionPrima = intercambio(solution)
        else:
            solutionPrima = inversion(solution)
    return solutionPrima


def matrixToList(solution: List[List[int]]) -> List[int]:
    flat_list = []
    # Iterar sobre cada sublista en la matriz
    for sublist in solution:
        # Iterar sobre cada elemento en la sublista y agregarlo a flat_list
        for item in sublist:
            flat_list.append(item)
    return flat_list


# Mutacion por intercambio
def intercambio(x):
    n = len(x)
    xprima = x * 1
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    temp = xprima[i]
    xprima[i] = xprima[j]
    xprima[j] = temp
    return xprima


# Mutacion por insercion
def insercion(x):
    n = len(x)
    xprima = x * 1
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    if j < i:
        temp = i
        i = j
        j = temp
    xprima.pop(j)
    xprima.insert(i, x[j])
    return xprima


# Mutacion por inversion
def inversion(x):
    n = len(x)
    xprima = x * 1
    i = choice(range(n))
    j = choice(range(n))
    while j == i:
        j = choice(range(n))
    for k in range(j - i + 1):
        xprima[i + k] = x[j - k]
    return xprima


def miniMutation(
    solution,
    capacity,
    demand_per_client,
):
    mutated_solution = [route.copy() for route in solution]

    while True:
        non_empty_routes = [
            i for i in range(len(mutated_solution)) if mutated_solution[i]
        ]

        if len(non_empty_routes) < 2:
            return mutated_solution

        route1_idx = random.choice(non_empty_routes)
        non_empty_routes.remove(route1_idx)
        route2_idx = random.choice(non_empty_routes)

        # Seleccionar clientes aleatorios de ambas rutas
        client1_idx = random.randint(0, len(mutated_solution[route1_idx]) - 1)
        client2_idx = random.randint(0, len(mutated_solution[route2_idx]) - 1)

        # Obtener los clientes seleccionados
        client1 = mutated_solution[route1_idx][client1_idx]
        client2 = mutated_solution[route2_idx][client2_idx]

        # Verificar si la mutación respeta la capacidad de las rutas y no repite valores
        if (
            (
                sum(
                    demand_per_client[client1]
                    for client1 in mutated_solution[route1_idx]
                )
                - demand_per_client[client1]
                + demand_per_client[client2]
                <= capacity
            )
            and (
                sum(
                    demand_per_client[client2]
                    for client2 in mutated_solution[route2_idx]
                )
                - demand_per_client[client2]
                + demand_per_client[client1]
                <= capacity
            )
            and (client1 not in mutated_solution[route2_idx])
            and (client2 not in mutated_solution[route1_idx])
        ):
            # Intercambiar los clientes entre las rutas
            mutated_solution[route1_idx][client1_idx] = client2
            mutated_solution[route2_idx][client2_idx] = client1

            # Verificar si las rutas son válidas después de la mutación
            if all(
                is_route_valid(route, demand_per_client, capacity)
                for route in mutated_solution
            ):
                return mutated_solution


def mutation(
    solution: List[List[int]],
    minimo: int,
    maximo: int,
    num_clients: int,
    num_trucks: int,
    capacity: int,
    demand_per_client,
    typeMutation: str,
    optimal_value: int,
    mejor_aptitud,
) -> List[List[int]]:
    arraySolution = matrixToList(solution)

    while True:
        # Obtener num_trucks - 1 números aleatorios que no se repitan desde 0 hasta el tamaño de la lista
        mutated_solution = chooseMutation(arraySolution, typeMutation)
        numeros_aleatorios = random.sample(
            range(len(arraySolution)), num_trucks - 1)
        # Ordenar los números de menor a mayor
        numeros_ordenados = sorted(numeros_aleatorios)

        # Dividir la solución mutada en rutas usando los índices generados aleatoriamente
        routes = []
        start_idx = 0
        for end_idx in numeros_ordenados:
            routes.append(mutated_solution[start_idx:end_idx])
            start_idx = end_idx
        # Agregar la última ruta
        routes.append(mutated_solution[start_idx:])

        all_routes_valid = all(
            is_route_valid(route, demand_per_client, capacity) for route in routes
        )

        # Si todas las rutas son válidas, retornar la lista de rutas
        if all_routes_valid:
            # print("ROUTES", routes)
            return routes


def ee(
    num_generaciones: int,
    distance_matrix: List[List[float]],
    optimal_value: int,
    dimension: int,
    num_trucks: int,
    capacity,
    demand_per_client,
    probability,
    lambdaVar,
    mu,
    typeMutation,
) -> Tuple[List[List[int]], float]:
    # TODO:
    # Se crea una poblcion de  individuos (permutaciones) aleatorios
    # BUG: ¡AL TIRO! A VECES SE MUERE PA
    poblacion_inicial = generate_initial_solutions(
        dimension, num_trucks, probability, capacity, demand_per_client, mu
    )
    aptitudes = [
        evaluate_solution(solution, distance_matrix) for solution in poblacion_inicial
    ]

    # for x in poblacion_inicial:
    #     for y in x:
    #         print(y)
    #     print("")

    # print(f"Aptitudes: {aptitudes}")
    # print("")

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
    print("POBLACIÓN INICIAL", poblacion_inicial)
    while generacionesSinMejora < num_generaciones:
        generacion = generacion + 1

        # TODO:
        # Se mutan los individuos actuales x para obtener
        # los nuevos individuos x'
        # y se evalua x' en la funcion de aptitud
        # xprima, aptitudprima = mutarPoblacion(x, d, mut, l)
        poblacion_prima = []
        # for poblacion in poblacion_inicial:
        #     poblacion_prima.append(mutation(poblacion, 1, 100,
        #                                     dimension, num_trucks, capacity,
        #                                     demand_per_client))

        # De la población inicial se mutan lambda soluciones y se añaden a poblacion Prima
        for index in range(lambdaVar):
            if mejor_aptitud < optimal_value * 1.1:
                poblacion_prima.append(
                    miniMutation(
                        poblacion_inicial[index], capacity, demand_per_client)
                )
            else:
                poblacion_prima.append(
                    mutation(
                        poblacion_inicial[index],
                        1,
                        100,
                        dimension,
                        num_trucks,
                        capacity,
                        demand_per_client,
                        typeMutation,
                        optimal_value,
                        mejor_aptitud,
                    )
                )

        aptitudes_primas = [
            evaluate_solution(solution, distance_matrix) for solution in poblacion_prima
        ]

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
        #
        # return

        # TODO:
        # Se mezclan los invidiuos originales y
        # los resultados de la mutacion
        # x.extend(xprima)
        # aptitud.extend(aptitudprima)
        poblacion_inicial.extend(poblacion_prima)
        aptitudes.extend(aptitudes_primas)
        print(f"Aptitudes: {aptitudes}")
        # print(f"AptitudesPrimas: {aptitudes_primas}")
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
        print("GENERACIONES SIN MEJORA", generacionesSinMejora)
        if aptitudes[0] < mejor_aptitud:
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

        # print(poblacion_inicial[0])

        # TODO:
        # regresar lo mejor
        # return poblacion_inicial[0], (-1 * aptitudes[0]), generacionMejor,
        # generacion

    print("Mejor Aptitud encontrada:", mejor_aptitud)
    print("Mejor solución encontrada:", mejor_poblacion)
    print("Mejor población encontrada:", poblacion_inicial)
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


def main(instance_file, routes_file, num_iterations, mu, lambdaVar, typeMutation):
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
            num_iterations,
            distance_matrix,
            optimal_value,
            dimension,
            num_trucks,
            capacity,
            customer_demands,
            probability,
            lambdaVar,
            mu,
            typeMutation,
        )
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
    if len(sys.argv) != 7:
        print(
            "Usage: python script_name.py instance_file routes_file num_iterations mu lambdaVar"
        )
    else:
        instance_file = sys.argv[1]
        routes_file = sys.argv[2]
        num_iterations = int(sys.argv[3])
        mu = int(sys.argv[4])
        lambdaVar = int(sys.argv[5])
        typeMutation = sys.argv[6]
        main(instance_file, routes_file, num_iterations,
             mu, lambdaVar, typeMutation)
