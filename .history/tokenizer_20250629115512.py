import os
import torch

INPUT_PATH = "./data/input.txt"
TOKENIZER_PATH = 'checkpoints/tokenizer.pt'

text = ""
chars = []
vocab_size = 0
stoi = {}
itos = {}

def initialize_tokenizer():
    global text, chars, vocab_size, stoi, itos
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"'{INPUT_PATH}' niet gevonden. Voer eerst 'generate_custom_data.py' uit.")
    print("Tokenizer: input.txt wordt ingelezen...")
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    print("Tokenizer: Inlezen voltooid.")
    chars = sorted(list(set(text)))
    vocab_size = len(chars)
    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for i, ch in enumerate(chars)}

def encode(s):
    if not stoi: initialize_tokenizer()
    return [stoi[c] for c in s]

def decode(l):
    if not itos: initialize_tokenizer()
    return ''.join([itos[i] for i in l])

def save_tokenizer():
    os.makedirs("checkpoints", exist_ok=True)
    torch.save({'stoi': stoi, 'itos': itos, 'vocab_size': vocab_size}, TOKENIZER_PATH)

def load_tokenizer():
    if not os.path.exists(TOKENIZER_PATH):
        raise FileNotFoundError(f"Tokenizer-bestand niet gevonden. Train eerst een model.")
    data = torch.load(TOKENIZER_PATH)
    loaded_stoi, loaded_itos, loaded_vocab_size = data['stoi'], data['itos'], data['vocab_size']
    def loaded_encode(s): return [loaded_stoi.get(c, -1) for c in s]
    def loaded_decode(l): return ''.join([loaded_itos.get(i, '') for i in l])
    return loaded_encode, loaded_decode, loaded_vocab_size