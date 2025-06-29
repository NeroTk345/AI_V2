import torch
from model import GPTLanguageModel, block_size, device
from tokenizer import load_tokenizer

def generate_interactive(load_path='checkpoints/gpt_model.pth', max_new_tokens=100, temperature=0.8):
    print(f"Model laden van {load_path}...")
    print(f"Gebruikte temperatuur: {temperature}")

    # Laad tokenizer om vocab_size en de functies te krijgen
    encode, decode, vocab_size = load_tokenizer()

    # Initialiseer model met vocab_size
    model = GPTLanguageModel(vocab_size)
    model.load_state_dict(torch.load(load_path, map_location=device))
    model.to(device)
    model.eval()

    print("Model geladen. Start interactieve sessie (type 'exit' om te stoppen).\n")

    context_str = "" 

    while True:
        user_input = input("Jij: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Sessie beëindigd.")
            break

        prompt = context_str + "user: " + user_input + "\nAI: "
        input_tokens = encode(prompt)[-block_size:]
        input_tensor = torch.tensor([input_tokens], dtype=torch.long, device=device)

        with torch.no_grad():
            # Geef de temperatuur nu door aan de generate functie
            output_tokens = model.generate(input_tensor, max_new_tokens=max_new_tokens, temperature=temperature)
        
        generated_part = decode(output_tokens[0].tolist()[len(input_tokens):])
        answer = generated_part.strip().split("\n")[0]

        print(f"AI: {answer}\n")
        
        context_str += "user: " + user_input + "\nAI: " + answer + "\n"

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="Genereer tekst met een GPT-model.")
    parser.add_argument('--load_path', type=str, default='checkpoints/gpt_model.pth', help='Pad naar het modelbestand')
    parser.add_argument('--max_new_tokens', type=int, default=100, help='Aantal tokens dat gegenereerd wordt per prompt')
    # --- NIEUW ARGUMENT HIERONDER ---
    parser.add_argument('--temperature', type=float, default=0.8, help='De creativiteit van de AI (hoger = creatiever)')
    
    args = parser.parse_args()

    generate_interactive(load_path=args.load_path, max_new_tokens=args.max_new_tokens, temperature=args.temperature)