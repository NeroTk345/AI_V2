import os
import torch

# Pad naar input.txt (moet in dezelfde directory staan)
INPUT_PATH = "./data/input.txt"
TOKENIZER_PATH = 'checkpoints/tokenizer.pt'

if not os.path.exists(INPUT_PATH):
    raise FileNotFoundError("input.txt niet gevonden. Zorg dat het bestand in de projectmap staat.")

with open(INPUT_PATH, 'r', encoding='utf-8') as f:
    text = f.read()

# Alle unieke karakters
chars = sorted(list(set(text)))
vocab_size = len(chars)

# Mapping
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for i, ch in enumerate(chars)}

# Encode / decode functies
def encode(s):
    return [stoi[c] for c in s]

def decode(l):
    return ''.join([itos[i] for i in l])

def save_tokenizer():
    torch.save({
        'stoi': stoi,
        'itos': itos,
        'vocab_size': vocab_size
    }, TOKENIZER_PATH)

def load_tokenizer():
    data = torch.load(TOKENIZER_PATH)
    stoi = data['stoi']
    itos = data['itos']
    vocab_size = data['vocab_size']

    def encode(s):
        return [stoi[c] for c in s]

    def decode(l):
        return ''.join([itos[i] for i in l])

    return encode, decode, vocab_size
