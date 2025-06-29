from datasets import load_dataset
import os

# De naam van de dataset op Hugging Face
dataset_name = "aacudad/86k_DUTCH_conversational"
# De naam van het bestand waar we alles in opslaan
output_filename = "input.txt"

def prepare_data():
    """
    Downloadt de dataset van Hugging Face en converteert deze
    naar het "user: ...\nAI: ...\n" formaat voor training.
    """
    print("--- Stap 1: Script gestart ---")
    print(f"Dataset '{dataset_name}' wordt nu gedownload. Dit kan de eerste keer even duren.")
    
    try:
        dataset = load_dataset(dataset_name, split='train')
    except Exception as e:
        print(f"!!! FOUT: Kon de dataset niet laden. Foutmelding: {e}")
        print("Controleer je internetverbinding en probeer het opnieuw.")
        return

    print("\n--- Stap 2: Download voltooid! ---")
    print("Dataset wordt nu verwerkt en naar input.txt geschreven...")

    lines_written = 0
    with open(output_filename, "w", encoding="utf-8") as f:
        # Loop door elke conversatie in de dataset
        for conversation in dataset:
            # --- DEZE REGELS ZIJN NU GECORRIGEERD ---
            # De kolom voor de gebruiker heet 'text'
            user_text = conversation['text'].strip()
            # De kolom voor de AI heet 'reply'
            ai_text = conversation['reply'].strip()
            
            # Sla over als een van de teksten leeg is
            if not user_text or not ai_text:
                continue

            f.write(f"user: {user_text}\n")
            f.write(f"AI: {ai_text}\n")
            lines_written += 2
    
    file_size = os.path.getsize(output_filename) / (1024 * 1024) # in MB
    
    print("\n--- Stap 3: Verwerking voltooid! ---")
    print(f"Het bestand '{output_filename}' is succesvol aangemaakt.")
    print(f"Totaal aantal geschreven regels: {lines_written}")
    print(f"Bestandsgrootte: {file_size:.2f} MB")
    print("\nJe kunt nu je model trainen met 'python train.py'")


if __name__ == "__main__":
    prepare_data()