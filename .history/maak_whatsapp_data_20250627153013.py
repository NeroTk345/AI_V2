# maak_whatsapp_data_v2.py (Gebruikt een betrouwbare, moderne dataset)

from datasets import load_dataset
import os

def prepare_whatsapp_style_dataset(
    output_path="data/whatsapp_stijl_dataset_500k.txt",
    max_lines=500000,
    dataset_name="BramVanroy/ultrachat_200k_dutch"  # <-- We gebruiken deze betrouwbare dataset
):
    """
    Downloadt een grote Nederlandse chat-dataset en formatteert deze naar een
    WhatsApp-stijl conversatiebestand.
    """
    print(f"Dataset '{dataset_name}' wordt gedownload. Dit kan even duren...")
    
    try:
        # Laad de dataset. 'streaming=True' downloadt niet alles in één keer.
        dataset = load_dataset(dataset_name, split="train_sft", streaming=True)
    except Exception as e:
        print(f"Kon dataset niet laden. Fout: {e}")
        print("Controleer je internetverbinding en probeer het opnieuw.")
        return

    # Zorg dat de 'data' map bestaat
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Conversaties worden verwerkt en weggeschreven naar {output_path}...")
    
    line_count = 0
    with open(output_path, 'w', encoding='utf-8') as f:
        for conversation in dataset:
            if line_count >= max_lines:
                print(f"Limiet van {max_lines} regels bereikt. Stoppen met verwerken.")
                break

            # 'messages' is een lijst met 'role' en 'content'
            messages = conversation['messages']
            
            # We doorlopen de berichten in paren (user -> assistant)
            for i in range(0, len(messages) - 1, 2):
                if messages[i]['role'] == 'user' and messages[i+1]['role'] == 'assistant':
                    # Maak de tekst schoon: verwijder nieuwe regels binnen een bericht
                    user_msg = messages[i]['content'].strip().replace('\n', ' ')
                    ai_msg = messages[i+1]['content'].strip().replace('\n', ' ')

                    # Schrijf de geformatteerde regels, alsof het twee personen zijn
                    f.write(f"Persoon 1: {user_msg}\n")
                    f.write(f"Persoon 2: {ai_msg}\n")
                    line_count += 2
            
            # Voeg een lege regel toe om gesprekken te scheiden
            f.write("\n")
            line_count += 1
            
            # Geef een update over de voortgang
            if line_count > 0 and line_count % 5000 == 0:
                print(f"  ... {line_count} regels verwerkt.")

    if line_count < max_lines:
        print(f"Dataset volledig verwerkt. Totaal {line_count} regels geschreven.")
    
    print(f"Klaar! Je nieuwe trainingsbestand staat in '{output_path}'.")

if __name__ == '__main__':
    prepare_whatsapp_style_dataset()