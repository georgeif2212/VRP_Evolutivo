""" 
Implementación VRP MU + LAMBDA
Authors: Brian Rivera Martinez, Jorge Infante Fragoso, Karina Alcántara Segura

"""

from ReadInstance import *


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
            if (
                current_demand_per_client[calculated_route] + demand_per_client[client]
                <= capacity
            ):
                routes[calculated_route].append(client)
                current_demand_per_client[calculated_route] += demand_per_client[client]
                swap_elements(aux, position, -1)
                aux.pop()

            i += random.randint(1, len(aux) + 1)

    return routes


def calculate_route_cost(route: List[int], distance_matrix: List[List[float]]) -> float:
    cost = 0.0
    num_clients = len(route)
    for i in range(num_clients - 1):
        initial = route[i]
        final = route[i + 1]
        cost += distance_matrix[initial][final]
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
    solution: List[List[int]],
    num_trucks: int,
    capacity: int,
    demand_per_client: List[int],
    typeMutation: str,
) -> List[List[int]]:
    arraySolution = matrixToList(solution)

    while True:
        mutated_solution = chooseMutation(arraySolution, "inv")

        # Divide mutated_solution en rutas del mismo tamaño que las rutas de solution inicial
        routes = []
        route_sizes = [
            len(route) for route in solution
        ]  # Obtén los tamaños de las rutas de solution
        current_index = 0

        for size in route_sizes:
            route = mutated_solution[current_index : current_index + size]
            routes.append(route)
            current_index += size
        else:
            if all(
                is_route_valid(route, demand_per_client, capacity) for route in routes
            ):
                return routes


def mutation(
    solution: List[List[int]],
    num_trucks: int,
    capacity: int,
    demand_per_client,
    typeMutation: str,
) -> List[List[int]]:
    arraySolution = matrixToList(solution)
    while True:
        # Obtener num_trucks - 1 números aleatorios que no se repitan desde 0 hasta el tamaño de la lista
        mutated_solution = chooseMutation(arraySolution, typeMutation)
        numeros_aleatorios = random.sample(range(len(arraySolution)), num_trucks - 1)
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
    poblacion_inicial = generate_initial_solutions(
        dimension, num_trucks, probability, capacity, demand_per_client, mu
    )

    aptitudes = [
        evaluate_solution(solution, distance_matrix) for solution in poblacion_inicial
    ]
    print("Aquí vamos")

    combination = list(zip(poblacion_inicial, aptitudes))
    combination = sorted(combination, key=lambda x: x[1])

    poblacion_inicial = [elem[0] for elem in combination[:mu]]
    aptitudes = [elem[1] for elem in combination[:mu]]

    mejor_poblacion = poblacion_inicial[0]
    mejor_aptitud = aptitudes[0]

    generacion = 0
    generacionesSinMejora = 0
    generacionMejor = 0

    while generacionesSinMejora < num_generaciones:
        generacion = generacion + 1

        poblacion_prima = []

        # De la población inicial se mutan lambda soluciones y se añaden a poblacion Prima
        for index in range(lambdaVar):
            if generacionesSinMejora > 200 and mejor_aptitud > optimal_value * 1.08:
                poblacion_prima.append(
                    miniMutation(
                        poblacion_inicial[index],
                        num_trucks,
                        capacity,
                        demand_per_client,
                        typeMutation,
                    )
                )
            else:
                if mejor_aptitud < optimal_value * 1.08:
                    poblacion_prima.append(
                        miniMutation(
                            poblacion_inicial[index],
                            num_trucks,
                            capacity,
                            demand_per_client,
                            typeMutation,
                        )
                    )
                else:
                    poblacion_prima.append(
                        mutation(
                            poblacion_inicial[index],
                            num_trucks,
                            capacity,
                            demand_per_client,
                            typeMutation,
                        )
                    )
            

        aptitudes_primas = [
            evaluate_solution(solution, distance_matrix) for solution in poblacion_prima
        ]

        poblacion_inicial.extend(poblacion_prima)
        aptitudes.extend(aptitudes_primas)

        # Se ordena el conjunto
        combination = list(zip(poblacion_inicial, aptitudes))
        combination = sorted(combination, key=lambda x: x[1])

        poblacion_inicial = [elem[0] for elem in combination[:mu]]
        aptitudes = [elem[1] for elem in combination[:mu]]

        print(
            "Mejor aptitud: ",
            mejor_aptitud,
            "con: ",
            generacionesSinMejora,
            " generaciones sin mejora",
        )
        if aptitudes[0] < mejor_aptitud:
            mejor_poblacion = poblacion_inicial[0]
            mejor_aptitud = aptitudes[0]
            generacionMejor = generacion
            generacionesSinMejora = 0
        else:
            generacionesSinMejora = generacionesSinMejora + 1

    return mejor_poblacion, mejor_aptitud


def main(
    instance_file,
    routes_file,
    num_iterations,
    mu,
    lambdaVar,
    typeMutation,
    num_generations,
):
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
    # print_customer_demands(customer_demands)
    # print_distance_matrix(distance_matrix)
    # print_routes(result_routes)

    for _ in range(num_iterations):
        best_solution, best_solution_cost = ee(
            num_generations,
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

    print("Mejor solución encontrada:")
    for solution in best_solution:
        print(solution)

    BLACK_TEXT_LIGHT_PINK_BG = "\033[97;48;5;54m"
    RESET = "\033[0m"
    best_solution_cost_str = str(best_solution_cost)
    print(
        "Costo de la mejor solución encontrada: "
        + BLACK_TEXT_LIGHT_PINK_BG
        + best_solution_cost_str
        + RESET
    )

    ORANGE_TEXT_BLACK_BG = "\033[97;48;5;202m"
    RESET = "\033[0m"
    optimal_value_str = str(optimal_value)
    print(
        "Costo de la solución optima del problema: "
        + ORANGE_TEXT_BLACK_BG
        + optimal_value_str
        + RESET
    )
    return


if __name__ == "__main__":
    if len(sys.argv) != 8:
        print(
            "Usage: python script_name.py instance_file routes_file num_iterations mu lambdaVar typeOfMutation numGenerationWithoutUpgrade"
        )
    else:
        instance_file = sys.argv[1]
        routes_file = sys.argv[2]
        num_iterations = int(sys.argv[3])
        mu = int(sys.argv[4])
        lambdaVar = int(sys.argv[5])
        typeMutation = sys.argv[6]
        num_generations = int(sys.argv[7])
        main(
            instance_file,
            routes_file,
            num_iterations,
            mu,
            lambdaVar,
            typeMutation,
            num_generations,
        )
