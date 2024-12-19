import random
import json
from heapq import heappop, heappush

# Funzione per generare una configurazione valida del gioco del 11
def generate_valid_configuration():
    tiles = list(range(12))  # Cifre da 0 a 11, dove 0 rappresenta lo spazio vuoto
    while True:
        random.shuffle(tiles)
        if is_solvable(tiles):
            return tiles

# Funzione per verificare se una configurazione è risolvibile
def is_solvable(tiles):
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] != 0 and tiles[j] != 0 and tiles[i] > tiles[j]:
                inversions += 1
    zero_row = tiles.index(0) // 4
    return (inversions + zero_row) % 2 == 0

# Funzione per stampare una configurazione
def print_configuration(tiles):
    for i in range(0, 12, 4):
        print(tiles[i:i + 4])
    print()

# Funzione per salvare una configurazione in un file JSON
def save_configuration_to_file(tiles, filename="3x4.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(tiles)

    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Funzione per trovare la posizione dello spazio vuoto
def find_zero(tiles):
    return tiles.index(0)

# Funzione per calcolare le mosse valide a partire da una configurazione
def valid_moves(zero_pos):
    moves = []
    row, col = divmod(zero_pos, 4)
    if row > 0: moves.append(-4)  # Su
    if row < 2: moves.append(4)   # Giù
    if col > 0: moves.append(-1)  # Sinistra
    if col < 3: moves.append(1)   # Destra
    return moves

# Funzione per eseguire una mossa
def make_move(tiles, zero_pos, move):
    new_tiles = tiles[:]
    new_zero_pos = zero_pos + move
    new_tiles[zero_pos], new_tiles[new_zero_pos] = new_tiles[new_zero_pos], new_tiles[zero_pos]
    return new_tiles

# Funzione euristica: distanza di Manhattan
def manhattan_distance(tiles):
    distance = 0
    for i, tile in enumerate(tiles):
        if tile != 0:
            correct_pos = 11 - tile  # Posizione corretta invertita
            current_row, current_col = divmod(i, 4)
            correct_row, correct_col = divmod(correct_pos, 4)
            distance += abs(current_row - correct_row) + abs(current_col - correct_col)
    return distance

# Risoluzione del gioco usando l'algoritmo A*
def solve_puzzle(start_tiles):
    zero_pos = find_zero(start_tiles)
    frontier = []
    heappush(frontier, (0, start_tiles, zero_pos, 0, []))  # (priorità, tiles, posizione 0, costo, percorso)
    explored = set()

    while frontier:
        _, current_tiles, zero_pos, cost, path = heappop(frontier)

        if current_tiles == list(range(11, -1, -1)):
            return path

        explored.add(tuple(current_tiles))

        for move in valid_moves(zero_pos):
            new_tiles = make_move(current_tiles, zero_pos, move)
            new_path = path + [new_tiles]

            if tuple(new_tiles) not in explored:
                priority = cost + 1 + manhattan_distance(new_tiles)
                heappush(frontier, (priority, new_tiles, zero_pos + move, cost + 1, new_path))

    return None

# Esempio di esecuzione
if __name__ == "__main__":
    initial_tiles = generate_valid_configuration()
    print("Configurazione iniziale:")
    print_configuration(initial_tiles)

    # Salva la configurazione iniziale
    save_configuration_to_file(initial_tiles)

    solution_path = solve_puzzle(initial_tiles)

    if solution_path:
        print("Risoluzione del puzzle:")
        for step, tiles in enumerate(solution_path):
            print(f"Passo {step + 1}:")
            print_configuration(tiles)
    else:
        print("Nessuna soluzione trovata.")