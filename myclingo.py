import sys
import time
from clingo import Control

def solve_game(maxtime=24, path_file="./3x3/gioco_8.asp", configurations=["jumpy"]):
    # Leggi il file gioco_8.asp
    with open(path_file) as f:
        program = f.read()

    print("Risoluzione del gioco al path: ", path_file)

    # Aggiungi la direttiva #const maxtime = <valore>
    program = f"#const maxtime = {maxtime}.\n" + program
    
    if configurations is None:
        configurations = ["jumpy", "tweety", "trendy", "crafty", "handy"]
    
    all_results = {}
    times = {}
    
    for config in configurations:
        print(f"Risoluzione con configurazione: {config}")
        
        # Crea un controllo Clingo con l'opzione multi-threading
        ctl = Control(["-t", "8"])
        
        # Aggiungi il programma
        ctl.add("base", [], program)
        
        # Ground del programma
        ctl.ground([("base", [])])
        
        # Risolvi e raccogli i risultati
        results = []
        last_holds = []  # Lista per gli holds dell'ultimo modello

        start_time = time.time()
        with ctl.solve(yield_=True) as handle:
            for model in handle:
                # Estrai le azioni dal modello
                actions = [atom for atom in model.symbols(atoms=True) if str(atom).startswith("occurs")]
                results.append(actions)
                
                # Estrai le soluzioni hold
                holds = [str(atom) for atom in model.symbols(atoms=True) if str(atom).startswith("hold")]
                last_holds = holds  # Aggiorna gli holds all'ultimo modello
                
        end_time = time.time()
        
        # Dopo aver iterato tutti i modelli, scrivi gli holds dell'ultimo nel file
        with open("holds.txt", "w") as file:
            for hold in last_holds:
                file.write(f"{hold}\n")
        
        all_results[config] = results
        times[config] = end_time - start_time
    
    return all_results, times

def main():
    path_file = "./3x3/gioco_8.asp"  # Percorso predefinito

    # Controlla se il flag -p è presente
    if "-p" in sys.argv:
        p_index = sys.argv.index("-p")
        if p_index + 1 < len(sys.argv):
            path_file = sys.argv[p_index + 1]
        else:
            print("Errore: nessun percorso specificato dopo il flag -p")
            sys.exit(1)

    if len(sys.argv) > 1 and sys.argv[1] == "-gara":
        # Risolvi il puzzle dell'8 con gara
        all_solutions, times = solve_game(path_file=path_file)
        
        # Ordina le configurazioni per tempo
        sorted_configs = sorted(times, key=times.get)
        
        # Stampa i risultati della gara
        print("Classifica della gara:")
        for i, config in enumerate(sorted_configs, 1):
            print(f"{i}. Configurazione: {config}, Tempo: {times[config]:.2f} secondi")
            solutions = all_solutions[config]
            for j, solution in enumerate(solutions, 1):
                print(f"  Soluzione {j}:")
                for action in solution:
                    print(f"    {action}")
                print("\n")
    else:
        # Risolvi il puzzle dell'8 senza gara
        all_solutions, _ = solve_game(path_file=path_file)
        
        # Stampa le soluzioni trovate
        solutions = all_solutions["jumpy"]
        for i, solution in enumerate(solutions, 1):
            print (f"\n")
            print(f"Soluzione {i}:")
            # Ordina le azioni in base al momento temporale
            sorted_actions = sorted(solution, key=lambda x: int(str(x).split(",")[-1].strip(")")))
            for action in sorted_actions:
                print(action)


if __name__ == "__main__":
    main()