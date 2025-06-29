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
    print(f"Dataset '{dataset_name}' aan het downloaden...")
    
    # Download de dataset (dit kan even duren de eerste keer)
    # We gebruiken alleen de 'train' split, die de meeste data bevat.
    try:
        dataset = load_dataset(dataset_name, split='train')
    except Exception as e:
        print(f"Kon de dataset niet laden. Fout: {e}")
        print("Zorg ervoor dat je een actieve internetverbinding hebt.")
        return

    print("Downloaden voltooid. Dataset aan het verwerken...")

    # Open het outputbestand om te schrijven
    with open(output_filename, "w", encoding="utf-8") as f:
        # Loop door elke conversatie in de dataset
        for conversation in dataset:
            # Haal de tekst van de gebruiker ('prompt') en de AI ('response') op
            # .strip() haalt ongewenste spaties en nieuwe regels aan het begin/eind weg
            user_text = conversation['prompt'].strip()
            ai_text = conversation['response'].strip()
            
            # Schrijf de geformatteerde conversatie naar het bestand
            f.write(f"user: {user_text}\n")
            f.write(f"AI: {ai_text}\n")
    
    # Krijg de grootte van het bestand om een idee te geven
    file_size = os.path.getsize(output_filename) / (1024 * 1024) # in MB
    print("\nVerwerking voltooid!")
    print(f"Het bestand '{output_filename}' is succesvol aangemaakt ({file_size:.2f} MB).")
    print("Je kunt nu je model trainen met 'python train.py'")


if __name__ == "__main__":
    prepare_data()