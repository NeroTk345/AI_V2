# maak_whatsapp_data.py (gecorrigeerde versie)

from datasets import load_dataset
import os

def prepare_whatsapp_style_dataset(
    output_path="data/whatsapp_stijl_dataset_500k.txt",
    max_lines=500000
):
    """
    Downloadt een dataset met filmdialogen (OpenSubtitles) en formatteert
    deze als een WhatsApp-gesprek tussen twee personen.
    """
    print("Dataset 'open_subtitles' (Nederlands) wordt geladen. Dit kan even duren...")
    
    try:
        # DE AANPASSING STAAT HIER: trust_remote_code=True is toegevoegd
        dataset = load_dataset(
            "open_subtitles", 
            lang1="nl", 
            lang2="nl", 
            split="train", 
            streaming=True, 
            trust_remote_code=True
        )
    except Exception as e:
        print(f"Kon dataset niet laden. Fout: {e}")
        print("Controleer je internetverbinding en probeer het opnieuw.")
        return

    # Zorg dat de 'data' map bestaat
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Dialogen worden verwerkt en weggeschreven naar {output_path}...")
    
    line_count = 0
    with open(output_path, 'w', encoding='utf-8') as f:
        for item in dataset:
            if line_count >= max_lines:
                print(f"Limiet van {max_lines} regels bereikt. Stoppen met verwerken.")
                break

            # 'translation' bevat het dialoogpaar. Voor nl-nl is dit hetzelfde.
            dialogue_lines = item['translation']['nl']
            
            # We verwerken alleen als er daadwerkelijk tekst is.
            if isinstance(dialogue_lines, str) and dialogue_lines.strip():
                lines = dialogue_lines.strip().split('\n')
                
                # We simuleren een gesprek tussen twee personen
                for i, line in enumerate(lines):
                    # Verwijder eventuele ondertiteling-opmaak en maak de tekst schoon
                    clean_line = line.strip()
                    if not clean_line:
                        continue
                    
                    # Wissel tussen "Persoon 1" en "Persoon 2"
                    person = "Persoon 1" if i % 2 == 0 else "Persoon 2"
                    
                    f.write(f"{person}: {clean_line}\n")
                    line_count += 1
                
                # Voeg een lege regel toe na elk dialoogblok om gesprekken te scheiden
                f.write("\n")
                line_count += 1

            # Geef een update over de voortgang
            if line_count > 0 and line_count % 10000 == 0:
                print(f"  ... {line_count} regels verwerkt.")

    if line_count < max_lines:
        print(f"Dataset volledig verwerkt. Totaal {line_count} regels geschreven.")
    
    print(f"Klaar! Je WhatsApp-stijl trainingsbestand staat in '{output_path}'.")

if __name__ == '__main__':
    prepare_whatsapp_style_dataset()