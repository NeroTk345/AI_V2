from datasets import load_dataset
import os

# --- DE AANPASSING ---
# We specificeren nu het pad inclusief de 'data' map
output_directory = "data"
output_filename = os.path.join(output_directory, "input.txt")
# --------------------

def create_final_dataset():
    print("--- Definitief Script Gestart (voor data map) ---")
    
    # Maak de 'data' map aan als deze nog niet bestaat
    os.makedirs(output_directory, exist_ok=True)
    print(f"Zorgen dat de map '{output_directory}' bestaat.")

    try:
        dataset = load_dataset("aacudad/86k_DUTCH_conversational", split='train')
    except Exception as e:
        print(f"!!! FOUT bij het downloaden: {e}")
        return

    print(f"Dataset geladen. Wordt nu naar '{output_filename}' geschreven...")
    lines_written = 0
    with open(output_filename, "w", encoding="utf-8") as f:
        for conversation in dataset:
            if (len(conversation['conversations']) >= 2 and 
                conversation['conversations'][0]['role'] == 'user' and 
                conversation['conversations'][1]['role'] == 'assistant'):
                
                user_text = conversation['conversations'][0]['content'].strip()
                ai_text = conversation['conversations'][1]['content'].strip()
                
                if not user_text or not ai_text:
                    continue

                f.write(f"user: {user_text}\n")
                f.write(f"AI: {ai_text}\n")
                lines_written += 2
    
    file_size = os.path.getsize(output_filename) / (1024 * 1024)
    print(f"\nKLAAR! '{output_filename}' is aangemaakt ({file_size:.2f} MB, {lines_written} regels).")
    print("\nJe bent nu helemaal klaar om je model te trainen met 'python train.py'")


if __name__ == "__main__":
    create_final_dataset()