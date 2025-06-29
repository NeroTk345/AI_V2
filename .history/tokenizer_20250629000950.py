import os
import torch

# We verwijzen nu expliciet naar de 'data' map
INPUT_PATH = "./data/input.txt"
TOKENIZER_PATH = 'checkpoints/tokenizer.pt'

# Definieer de globale variabelen
text = ""
chars = []
vocab_size = 0
stoi = {}
itos = {}

def initialize_tokenizer():
    """
    Leest de data en initialiseert de tokenizer variabelen.
    Deze functie moet één keer worden aangeroepen vanuit het hoofdscript.
    """
    global text, chars, vocab_size, stoi, itos
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"'{INPUT_PATH}' niet gevonden. Voer eerst een data-genereer script uit, zoals 'prepare_dataset.py'.")

    print("Tokenizer: input.txt wordt ingelezen...")
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    print("Tokenizer: Inlezen voltooid.")

    chars = sorted(list(set(text)))
    vocab_size = len(chars)
    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for i, ch in enumerate(chars)}

def encode(s):
    # Als de tokenizer nog niet is geïnitialiseerd, doe dat dan nu.
    if not stoi:
        initialize_tokenizer()
    return [stoi[c] for c in s]

def decode(l):
    # Als de tokenizer nog niet is geïnitialiseerd, doe dat dan nu.
    if not itos:
        initialize_tokenizer()
    return ''.join([itos[i] for i in l])

def save_tokenizer():
    if not vocab_size:
        print("FOUT: Tokenizer is niet geïnitialiseerd en kan niet worden opgeslagen.")
        return
    # Zorg ervoor dat de 'checkpoints' map bestaat
    os.makedirs("checkpoints", exist_ok=True)
    torch.save({'stoi': stoi, 'itos': itos, 'vocab_size': vocab_size}, TOKENIZER_PATH)

def load_tokenizer():
    if not os.path.exists(TOKENIZER_PATH):
        raise FileNotFoundError(f"Tokenizer-bestand niet gevonden op {TOKENIZER_PATH}. Train eerst een model met 'python train.py'.")
    data = torch.load(TOKENIZER_PATH)
    loaded_stoi = data['stoi']
    loaded_itos = data['itos']
    loaded_vocab_size = data['vocab_size']

    # Definieer de encode/decode functies binnen de scope van de geladen data
    def loaded_encode(s):
        return [loaded_stoi.get(c, -1) for c in s] # .get() voor robuustheid

    def loaded_decode(l):
        return ''.join([loaded_itos.get(i, '') for i in l]) # .get() voor robuustheid

    return loaded_encode, loaded_decode, loaded_vocab_size