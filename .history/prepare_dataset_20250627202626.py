from datasets import load_dataset
import os

# De naam van de dataset op Hugging Face
dataset_name = "aacudad/86k_DUTCH_conversational"
output_filename = "input.txt"

def create_final_dataset():
    """
    Downloadt de dataset en verwerkt de geneste 'conversations' structuur
    naar het correcte user/AI formaat in input.txt.
    """
    print("--- Definitief Script Gestart ---")
    print("De geneste datastructuur zal nu correct worden verwerkt.")
    
    try:
        # Download de volledige dataset
        dataset = load_dataset(dataset_name, split='train')
    except Exception as e:
        print(f"!!! FOUT bij het downloaden: {e}")
        return

    print("Dataset geladen. Wordt nu naar input.txt geschreven...")
    lines_written = 0
    conversations_skipped = 0
    with open(output_filename, "w", encoding="utf-8") as f:
        # Loop door elk item in de dataset
        for item in dataset:
            # Pak de lijst met gesprekken
            conversations_list = item['conversations']
            
            # Controleer of de lijst de verwachte structuur heeft (user, dan assistant)
            if (len(conversations_list) >= 2 and 
                conversations_list[0]['role'] == 'user' and 
                conversations_list[1]['role'] == 'assistant'):
                
                user_text = conversations_list[0]['content'].strip()
                ai_text = conversations_list[1]['content'].strip()
                
                # Sla over als een van de teksten leeg is
                if not user_text or not ai_text:
                    conversations_skipped += 1
                    continue

                f.write(f"user: {user_text}\n")
                f.write(f"AI: {ai_text}\n")
                lines_written += 2
            else:
                conversations_skipped += 1
    
    file_size = os.path.getsize(output_filename) / (1024 * 1024)
    print("\n--- KLAAR! ---")
    print(f"Het bestand '{output_filename}' is succesvol aangemaakt.")
    print(f"Bestandsgrootte: {file_size:.2f} MB")
    print(f"Totaal aantal geschreven regels: {lines_written}")
    if conversations_skipped > 0:
        print(f"Aantal overgeslagen (ongeldige) conversaties: {conversations_skipped}")
    
    print("\nJe bent nu helemaal klaar om je model te trainen met 'python train.py'")


if __name__ == "__main__":
    create_final_dataset()