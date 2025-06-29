from datasets import load_dataset

# De naam van de dataset op Hugging Face
dataset_name = "aacudad/86k_DUTCH_conversational"

def inspect_data_structure():
    """
    Laadt het eerste item van de dataset om de kolomnamen te inspecteren.
    """
    print("--- Inspectie Script Gestart ---")
    print("Het eerste item van de dataset wordt geladen om de structuur te bekijken...")

    try:
        # Gebruik 'streaming=True' om niet de hele dataset te downloaden
        dataset = load_dataset(dataset_name, split='train', streaming=True)
        
        # Pak alleen het allereerste item uit de dataset
        first_item = next(iter(dataset))
        
        print("\n--- Structuur Gevonden! ---")
        print("Dit is de volledige structuur van één item in de dataset:")
        print(first_item)
        
        print("\nDe beschikbare kolomnamen (keys) zijn:")
        print(list(first_item.keys()))
        
        print("\n--- Actie Vereist ---")
        print("Zoek in de lijst hierboven naar de juiste namen voor de vraag van de gebruiker en het antwoord van de AI.")
        print("Gebruik deze namen in de definitieve versie van het script in de volgende stap.")

    except Exception as e:
        print(f"!!! FOUT: Kon de dataset niet laden. Foutmelding: {e}")
        print("Controleer je internetverbinding en probeer het opnieuw.")

if __name__ == "__main__":
    inspect_data_structure()