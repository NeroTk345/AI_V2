import torch
from model import GPTLanguageModel
from tokenizer import load_tokenizer
from config import device, block_size

def generate_interactive(load_path='checkpoints/gpt_model.pth', max_new_tokens=100, temperature=0.8):
    print(f"Model laden van {load_path}...")
    print(f"Gebruikte temperatuur: {temperature}")
    try:
        encode, decode, vocab_size = load_tokenizer()
    except FileNotFoundError as e:
        print(f"FOUT: {e}\nZorg ervoor dat je eerst een model traint.")
        return

    model = GPTLanguageModel(vocab_size)
    try:
        model.load_state_dict(torch.load(load_path, map_location=device))
    except FileNotFoundError:
        print(f"FOUT: Modelbestand niet gevonden op {load_path}. Train eerst een model.")
        return
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
    parser.add_argument('--temperature', type=float, default=0.9, help='De creativiteit van de AI (hoger = creatiever)')
    args = parser.parse_args()
    generate_interactive(load_path=args.load_path, max_new_tokens=args.max_new_tokens, temperature=args.temperature)