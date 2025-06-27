import os
import pickle

def get_tokenizer(text_path='data/input.txt', vocab_path='checkpoints/tokenizer.pkl'):
    if os.path.exists(vocab_path):
        with open(vocab_path, 'rb') as f:
            stoi, itos = pickle.load(f)
    else:
        with open(text_path, 'r', encoding='utf-8') as f:
            text = f.read()
        chars = sorted(list(set(text)))
        stoi = {ch: i for i, ch in enumerate(chars)}
        itos = {i: ch for i, ch in enumerate(chars)}
        with open(vocab_path, 'wb') as f:
            pickle.dump((stoi, itos), f)
    encode = lambda s: [stoi[c] for c in s]
    decode = lambda l: ''.join([itos[i] for i in l])
    vocab_size = len(stoi)
    return encode, decode, vocab_size
