import torch
from model import GPTLanguageModel, decode, encode, block_size, device

def generate_interactive(load_path='checkpoints/gpt_model.pth', max_new_tokens=100):
    print(f"Model laden van {load_path}...")
    model = GPTLanguageModel()
    model.load_state_dict(torch.load(load_path, map_location=device))
    model.to(device)
    model.eval()
    print("Model geladen. Start interactieve sessie (type 'exit' om te stoppen).\n")

    context = []  # opgebouwde conversatie als lijst van tokens

    while True:
        user_input = input("Jij: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        # Voeg prompt toe aan context
        prompt_tokens = encode(user_input + "\nAI: ")
        context.extend(prompt_tokens)

        # Trim context indien nodig
        context = context[-block_size:]

        # Zet naar tensor
        input_tensor = torch.tensor([context], dtype=torch.long, device=device)

        # Genereer antwoord
        with torch.no_grad():
            output = model.generate(input_tensor, max_new_tokens=max_new_tokens)

        # Haal alleen het nieuwe gedeelte uit de output
        generated = output[0].tolist()[len(context):]
        answer = decode(generated).split('\n')[0].strip()

        # Voeg gegenereerde tokens toe aan context
        context.extend(generated)
        print(f"AI: {answer}\n")
