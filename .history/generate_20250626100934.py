import torch
from model import GPTLanguageModel
from tokenizer import get_tokenizer
from config import device

def main():
    _, decode, vocab_size = get_tokenizer()
    model = GPTLanguageModel(vocab_size)
    model.load_state_dict(torch.load("checkpoints/gpt_model.pt", map_location=device))
    model.to(device)
    model.eval()

    context = torch.zeros((1, 1), dtype=torch.long, device=device)
    output = model.generate(context, max_new_tokens=500)
    print("\n--- GEGENEREERDE TEKST ---\n")
    print(decode(output[0].tolist()))
    print("\n--- EINDE ---\n")

if __name__ == "__main__":
    main()
