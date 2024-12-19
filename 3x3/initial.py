import json
import os

def convert_to_initial_state(array):
    """
    Converte un array 3x3 in configurazioni iniziali formattate, seguendo l'ordine specificato.
    """
    lines = []
    for i, value in enumerate(array):
        row, col = divmod(i, 3)
        row += 1  # Le righe iniziano da 1
        col += 1  # Le colonne iniziano da 1
        lines.append(f"initially(posizione_tessera({value}, {row}, {col})).")
    return "\n".join(lines)

def create_initial_state_files(input_file, output_dir):
    """
    Legge il file JSON, converte gli array in configurazioni iniziali
    e salva ogni configurazione in un file separato nella cartella specificata.
    """
    # Legge il file JSON
    with open(input_file, "r") as file:
        data = json.load(file)

    # Assicurati che la cartella di output esista
    os.makedirs(output_dir, exist_ok=True)

    # Processa ogni array
    for index, array in enumerate(data):
        formatted_state = convert_to_initial_state(array)
        output_file = os.path.join(output_dir, f"state_{index + 1}.pl")
        with open(output_file, "w") as file:
            file.write(formatted_state)
        print(f"Configurazione salvata in: {output_file}")

# Esempio di utilizzo
if __name__ == "__main__":
    input_file = "3x3.json"          # File JSON di input
    output_dir = "initial_state"    # Cartella per i file di output
    create_initial_state_files(input_file, output_dir)
