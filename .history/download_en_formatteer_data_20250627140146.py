# download_en_formatteer_data.py

from datasets import load_dataset
import os

def prepare_large_dataset(
    output_path="data/grote_dataset_500k.txt",
    max_lines=500000,
    dataset_name="BramVanroy/ultrachat_200k_dutch"
):
    """
    Downloadt een grote Nederlandse chat-dataset en formatteert deze naar een
    WhatsApp-stijl conversatiebestand.
    """
    print(f"Dataset '{dataset_name}' wordt gedownload. Dit kan even duren...")
    
    # Laad de dataset. 'streaming=True' downloadt niet alles in één keer.
    dataset = load_dataset(dataset_name, split="train_sft", streaming=True)
    
    # Zorg dat de 'data' map bestaat
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Conversaties worden verwerkt en weggeschreven naar {output_path}...")
    
    line_count = 0
    with open(output_path, 'w', encoding='utf-8') as f:
        # We doorlopen de dataset en stoppen als we de max_lines hebben bereikt
        for conversation in dataset:
            if line_count >= max_lines:
                print(f"Limiet van {max_lines} regels bereikt. Stoppen met verwerken.")
                break

            # 'messages' is een lijst van dicts met 'role' en 'content'
            messages = conversation['messages']
            
            # We doorlopen de berichten in paren (user -> assistant)
            for i in range(0, len(messages) - 1, 2):
                if messages[i]['role'] == 'user' and messages[i+1]['role'] == 'assistant':
                    user_msg = messages[i]['content'].strip().replace('\n', ' ')
                    ai_msg = messages[i+1]['content'].strip().replace('\n', ' ')

                    # Schrijf de geformatteerde regels naar het bestand
                    f.write(f"User 1: {user_msg}\n")
                    f.write(f"Ai: {ai_msg}\n")
                    line_count += 2
            
            # Voeg een lege regel toe om gesprekken te scheiden
            f.write("\n")
            line_count += 1
            
            # Geef een update over de voortgang
            if line_count % 5000 == 0:
                print(f"  ... {line_count} regels verwerkt.")

    if line_count < max_lines:
        print(f"Dataset volledig verwerkt. Totaal {line_count} regels geschreven.")
    
    print(f"Klaar! Je nieuwe trainingsbestand staat in '{output_path}'.")

if __name__ == '__main__':
    prepare_large_dataset()