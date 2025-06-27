import torch
from model import GPTLanguageModel, decode, encode, block_size, device
import torch
from model import GPTLanguageModel, block_size, device
from tokenizer import encode, decode  # voeg deze toe


def generate_interactive(load_path='checkpoints/gpt_model.pth', max_new_tokens=100):
    print(f"Model laden van {load_path}...")
    
    # Laad het model
    model = GPTLanguageModel()
    model.load_state_dict(torch.load(load_path, map_location=device))
    model.to(device)
    model.eval()

    print("Model geladen. Start interactieve sessie (type 'exit' om te stoppen).\n")

    context = []  # opgebouwde conversatie als lijst van tokens

    while True:
        user_input = input("Jij: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Sessie beëindigd.")
            break

        # Voeg gebruiker prompt + AI hint toe
        prompt_tokens = encode(user_input + "\nAI: ")
        context.extend(prompt_tokens)

        # Beperk context tot block_size tokens
        context = context[-block_size:]

        # Zet context om naar tensor
        input_tensor = torch.tensor([context], dtype=torch.long, device=device)

        # Genereer output
        with torch.no_grad():
            output = model.generate(input_tensor, max_new_tokens=max_new_tokens)

        # Haal alleen het nieuwe stuk tekst uit de output
        generated = output[0].tolist()[len(context):]
        answer = decode(generated).strip().split("\n")[0]  # Pak eerste regel (optioneel)

        # Voeg gegenereerde tokens toe aan context
        context.extend(generated)

        print(f"AI: {answer}\n")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--load_path', type=str, default='checkpoints/gpt_model.pth', help='Pad naar het modelbestand')
    parser.add_argument('--max_new_tokens', type=int, default=100, help='Aantal tokens dat gegenereerd wordt per prompt')
    args = parser.parse_args()

    generate_interactive(load_path=args.load_path, max_new_tokens=args.max_new_tokens)
