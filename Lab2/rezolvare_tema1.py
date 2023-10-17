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

def is_final_state(state):
    final_state = [[1,2,3],[4,5,6],[7,8,0]]
    return state == final_state

# -------- 3 -------- #

def move(state, direction):
    new_state = [row[:] for row in state]
    row, col = find_empty_cell(state)

    if direction == "up" and row < 2:
        new_state[row][col] = new_state[row + 1][col]
        new_state[row + 1][col] = 0
    elif direction == "down" and row > 0 :
        new_state[row][col] = new_state[row - 1][col]
        new_state[row - 1][col] = 0
    elif direction == "left" and col < 2:
        new_state[row][col] = new_state[row][col + 1]
        new_state[row][col + 1] = 0
    elif direction == "right" and col > 0:
        new_state[row][col] = new_state[row][col - 1]
        new_state[row][col - 1] = 0
    
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
    for depth in range(max_depth + 1):
        result = dls(initial_state, depth)
        if result is not None:
            return result, depth
    return None, 0

def dls(state, depth):
    if depth == 0:
        if is_final_state(state):
            return [state]
        else:
            return None
        
    for direction in ["up", "down", "left", "right"]:
        new_state = move(state, direction)
        if new_state is not None:
            result = dls(new_state, depth - 1)
            if result is not None:
                return [state] + result
            
    return None

# -------- TESTS -------- #

# instances = [[8, 6, 7, 2, 5, 4, 0, 3, 1],
#              [2, 5, 3, 1, 0, 6, 4, 7, 8],
#              [2, 7, 5, 0, 8, 4, 3, 1, 6]]

# instances = [[2, 5, 3, 1, 0, 6, 4, 7, 8]]

instances = [[2, 7, 5, 0, 8, 4, 3, 1, 6]]

for instance in instances:
    try:
        initial_state = initialize_state(instance)
    except Exception as e:
        print(e)

    max_depth = 22
    start_time = time.time()
    solution, depth = iddfs(initial_state, max_depth)
    end_time = time.time()

    total_time_seconds = end_time - start_time
    total_time_milis = int(total_time_seconds * 1000)

    if solution is not None:
        for step, state in enumerate(solution):
            print(f"Step {step}:")
            for row in state:
                print(row)
        print(f"Depth: {depth}")
        print(f"Time taken: {total_time_seconds} seconds")
    else:
        print("No solution for this depth")