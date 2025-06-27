# tokenizer.py
import os
import torch

# Pad naar input.txt (moet in dezelfde directory staan)
INPUT_PATH = "./data/input.txt"

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

TOKENIZER_PATH = 'checkpoints/tokenizer.pt'

def save_tokenizer():
    torch.save({
        'encode': encode,
        'decode': decode,
        'vocab_size': vocab_size
    }, TOKENIZER_PATH)

def load_tokenizer():
    data = torch.load(TOKENIZER_PATH)
    return data['encode'], data['decode'], data['vocab_size']

