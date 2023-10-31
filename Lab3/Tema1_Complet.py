# Problema: Avem o matrice 3x3 cu 8 dintre celule numerotate de la 1 la 8 și una goală. 
# Știind că poziția inițială a celulelor este aleatoare și că putem muta o celulă doar în locul celulei goale 
# și doar dacă este adiacentă acesteia, să se găsească, dacă există, o secvență de mutări ale celulelor astfel 
# încât toate să fie plasate în ordine crescătoare în matrice. După mutarea unei celule, ea nu mai poate fi 
# mutată din nou decât după ce unul din vecinii săi a fost mutat. Poziția celulei goale nu contează pentru 
# validarea stării finale.

# (0.2) 1. Alegeți o reprezentare a unei stări a problemei. Reprezentarea trebuie să fie suficient de explicită
#          pentru a conține toate informaţiile necesare pentru continuarea găsirii unei soluții dar trebuie să 
#          fie și suficient de formalizată pentru a fi ușor de prelucrat/memorat. 
# (0.2) 2. Identificați stările speciale (inițială și finală) și implementați funcția de inițializare (primește 
#          ca parametri instanța problemei, întoarce starea inițială) și funcția booleană care verifică dacă o 
#          stare primită ca parametru este finală.
# (0.2) 3. Implementați tranzițiile ca funcții care primesc parametri o stare și parametrii tranziției și 
#          întoarce starea rezultată în urma aplicării tranziției. Validarea tranzițiilor se face în una sau mai
#          multe  funcții booleană, cu aceeași parametri. 
# (0.4) 4. Implementați strategia IDDFS.
# (0.5) 5. Implementați strategia Greedy și testați cel puțin trei euristici: distanța Manhattann, distanța Hamming, 
#          plus cel puțin încă o euristică diferită.
# (0.5) 6. Implementați un program care rulează toate cele 4 strategii (IDDFS și Greedy cu cele trei euristici) pentru 
#          cele trei instanțe și afișează soluția (dacă e găsită), lungimea sa (numărul de mutări) și durata execuției 
#          pentru fiecare din cele 4 strategii.


# Folosiți pentru testarea implementărilor instanțele: 
# [8, 6, 7, 2, 5, 4, 0, 3, 1]
# [2, 5, 3, 1, 0, 6, 4, 7, 8]
# [2, 7, 5, 0, 8, 4, 3, 1, 6]

# -------- 1 -------- #
# A state will be representet by a 3x3 matrix
# State example: state = [[8,6,7],
#                         [2,5,4],
#                         [0,3,1]]
# Where all possible values are from 0 to 8, 0 representing the empty space, and no values shall repeat

# -------- 2 -------- #
# The initial state is the one given as a parameter
# The final state is [[1,2,3],[4,5,6],[7,8,0]]

import time
import heapq
import math

def initialize_state(initial_instance):
    if len(initial_instance) != 9:
        raise Exception("Invalid instance! The instance must have exactly 9 emelents!")
    
    if sorted(initial_instance) != list(range(9)):
        raise Exception("Invalid instance! The instance must have all numbers from 0 to 8!")
    
    initial_state = [[0,0,0],[0,0,0],[0,0,0]]
    initial_instance_copy = initial_instance.copy()

    for i in range(3):
        for j in range(3):
            initial_state[i][j] = initial_instance_copy.pop(0)
    
    return initial_state

def state_to_list(state):
    state_list = []
    for i in range(3):
        for j in range(3):
            state_list.append(state[i][j])

    return state_list

def print_state(state):
    for row in state:
        print(row)

def is_final_state(state):
    final_list = [1,2,3,4,5,6,7,8]
    state_list = []
    for i in range(3):
        for j in range(3):
            state_list.append(state[i][j])

    state_list.remove(0)
    
    return state_list == final_list

# -------- 3 -------- #

def move(state, direction, last_direction=None):
    new_state = [row[:] for row in state]
    row, col = find_empty_cell(state)
    
    if direction == "up" and row < 2 and last_direction != "down":
        new_state[row][col] = new_state[row + 1][col]
        new_state[row + 1][col] = 0
    elif direction == "down" and row > 0 and last_direction != "up":
        new_state[row][col] = new_state[row - 1][col]
        new_state[row - 1][col] = 0
    elif direction == "left" and col < 2 and last_direction != "right":
        new_state[row][col] = new_state[row][col + 1]
        new_state[row][col + 1] = 0
    elif direction == "right" and col > 0 and last_direction != "left":
        new_state[row][col] = new_state[row][col - 1]
        new_state[row][col - 1] = 0

    last_direction = direction

    if new_state != state:
        return new_state
    else:
        return state

def find_empty_cell(state):
    for i in range(3):
        for j in range(3):
            if (state[i][j] == 0):
                return i, j

# -------- 4 -------- #

def iddfs(initial_state, max_depth):
    initial_state_as_list = state_to_list(initial_state)
    for depth in range(max_depth + 1):
        state_dict = {tuple(initial_state_as_list): None}
        result = dls(initial_state, depth, state_dict)
        if result is not None:
            return result, depth
    return None, 0

def dls(state, depth, state_dict=None):
    if depth == 0:
        if is_final_state(state):
            return [state]
        else:
            return None
        
    for direction in ["up", "down", "left", "right"]:
        new_state = move(state, direction)
        if new_state is not None:
            new_state_as_list = state_to_list(new_state)
            if tuple(new_state_as_list) not in state_dict:
                state_as_list = state_to_list(state)
                state_dict[tuple(new_state_as_list)] = tuple(state_as_list)
                result = dls(new_state, depth - 1, state_dict)
                if result is not None:
                    return [state] + result

    return None

# -------- 5 -------- #

def hamming_distance(state):
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8]
    state_as_list = state_to_list(state)
    state_as_list.remove(0)
    
    distance = 0
    for i in range(8):
        if state_as_list[i] != goal_state[i]:
            distance += 1
    return distance

def manhattan_distance(state):
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8]
    distance = 0
    state_as_list = state_to_list(state)
    state_as_list.remove(0)

    for i in range(1, 9):
        state_index = state_as_list.index(i)
        goal_index = goal_state.index(i)

        state_row, state_col = state_index // 3, state_index % 3
        goal_row, goal_col = goal_index // 3, goal_index % 3

        distance += abs(state_row - goal_row) + abs(state_col - goal_col)

    return distance

def euclidean_distance(state):
    goal_state = [1, 2, 3, 4, 5, 6, 7, 8]
    distance = 0

    state_as_list = state_to_list(state)
    state_as_list.remove(0)

    for i in range(1, 9):
        state_index = state_as_list.index(i)
        goal_index = goal_state.index(i)

        state_row, state_col = divmod(state_index, 3)
        goal_row, goal_col = divmod(goal_index, 3)

        distance += math.sqrt((state_row - goal_row) ** 2 + (state_col - goal_col) ** 2)

    return distance

def greedy_search(initial_state, heuristic):
    initial_state_as_list = state_to_list(initial_state)
    state_dict = {tuple(initial_state_as_list): None}
    priority_queue = [(heuristic(initial_state), initial_state)]
    steps = 0

    while priority_queue:
        _, state = heapq.heappop(priority_queue)

        if is_final_state(state):
            return state, steps

        for direction in ["up", "down", "left", "right"]:
            new_state = move(state, direction)
            if new_state is not None:
                new_state_as_list = state_to_list(new_state)
                if tuple(new_state_as_list) not in state_dict:
                    state_as_list = state_to_list(state)
                    state_dict[tuple(new_state_as_list)] = tuple(state_as_list)
                    heapq.heappush(priority_queue, (heuristic(new_state), new_state))
                    steps += 1

    return None, steps

# -------- 6 -------- #

# -------- TESTS -------- #

instances = [[8, 6, 7, 2, 5, 4, 0, 3, 1],
             [2, 5, 3, 1, 0, 6, 4, 7, 8],
             [2, 7, 5, 0, 8, 4, 3, 1, 6]]

# instances = [[2, 5, 3, 1, 0, 6, 4, 7, 8]]
print("IDDFS:")
for instance in instances:
    try:
        initial_state = initialize_state(instance)
    except Exception as e:
        print(e)

    print("Initial state:")
    print_state(initial_state)

    max_depth = 30
    start_time = time.time()
    solution, depth = iddfs(initial_state, max_depth)
    end_time = time.time()

    total_time_seconds = end_time - start_time
    total_time_milis = int(total_time_seconds * 1000)

    if solution is not None:
        print("Solution:")
        solution_matrix = solution[-1]
        print_state(solution_matrix)
        print(f"Steps: {depth}")
        print(f"Time taken: {total_time_seconds:.3f} seconds")
    else:
        print("No solution for this depth")
    print()
print("-------------------")

print("Hamming distance:")
for instance in instances:
    try:
        initial_state = initialize_state(instance)
    except Exception as e:
        print(e)

    print("Initial state:")
    print_state(initial_state)

    start_time = time.time()
    solution, steps = greedy_search(initial_state, hamming_distance)
    end_time = time.time()

    total_time_seconds = end_time - start_time
    total_time_millis = int(total_time_seconds * 1000)

    if solution is not None:
        print("Solution:")
        for row in solution:
            print(row)
        print(f"Steps: {steps}")
        print("Time taken: {:.3f} seconds".format(total_time_seconds))
    else:
        print("No solution found.")
    print()
print("-------------------")

print("Manhattan distance:")
for instance in instances:
    try:
        initial_state = initialize_state(instance)
    except Exception as e:
        print(e)

    print("Initial state:")
    print_state(initial_state)

    start_time = time.time()
    solution, steps = greedy_search(initial_state, manhattan_distance)
    end_time = time.time()

    total_time_seconds = end_time - start_time
    total_time_millis = int(total_time_seconds * 1000)

    if solution is not None:
        print("Solution:")
        for row in solution:
            print(row)
        print(f"Steps: {steps}")
        print("Time taken: {:.3f} seconds".format(total_time_seconds))
    else:
        print("No solution found.")
    print()
print("-------------------")

print("Euclidean distance:")
for instance in instances:
    try:
        initial_state = initialize_state(instance)
    except Exception as e:
        print(e)

    print("Initial state:")
    print_state(initial_state)

    start_time = time.time()
    solution, steps = greedy_search(initial_state, euclidean_distance)
    end_time = time.time()

    total_time_seconds = end_time - start_time
    total_time_millis = int(total_time_seconds * 1000)

    if solution is not None:
        print("Solution:")
        for row in solution:
            print(row)
        print(f"Steps: {steps}")
        print("Time taken: {:.3f} seconds".format(total_time_seconds))
    else:
        print("No solution found.")
    print()




