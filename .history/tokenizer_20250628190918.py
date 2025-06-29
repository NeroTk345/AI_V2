import os
import torch

INPUT_PATH = "./input.txt"
TOKENIZER_PATH = 'checkpoints/tokenizer.pt'

text = ""
chars = []
vocab_size = 0
stoi = {}
itos = {}

def initialize_tokenizer():
    global text, chars, vocab_size, stoi, itos
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError("input.txt niet gevonden. Voer eerst 'prepare_dataset.py' uit.")

    print("Tokenizer: input.txt wordt ingelezen...")
    with open(INPUT_PATH, 'r', encoding='utf-8') as f:
        text = f.read()
    print("Tokenizer: Inlezen voltooid.")

    chars = sorted(list(set(text)))
    vocab_size = len(chars)
    stoi = {ch: i for i, ch in enumerate(chars)}
    itos = {i: ch for i, ch in enumerate(chars)}

def encode(s):
    return [stoi[c] for c in s]

def decode(l):
    return ''.join([itos[i] for i in l])

def save_tokenizer():
    if not vocab_size:
        print("FOUT: Tokenizer niet geïnitialiseerd.")
        return
    torch.save({'stoi': stoi, 'itos': itos, 'vocab_size': vocab_size}, TOKENIZER_PATH)

def load_tokenizer():
    data = torch.load(TOKENIZER_PATH)
    loaded_stoi = data['stoi']
    loaded_itos = data['itos']
    loaded_vocab_size = data['vocab_size']

    def loaded_encode(s):
        return [loaded_stoi[c] for c in s]

    def loaded_decode(l):
        return ''.join([loaded_itos[i] for i in l])

    return loaded_encode, loaded_decode, loaded_vocab_size