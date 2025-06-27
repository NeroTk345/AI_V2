# train.py

import os
import torch
from torch.nn import functional as F
from model import GPTLanguageModel, block_size, device
from tokenizer import encode, decode, vocab_size, text

# Hyperparameters
batch_size = 64
max_iters = 5000
eval_interval = 500
learning_rate = 3e-4
eval_iters = 200

torch.manual_seed(1337)

# Data splits
data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data = data[:n]
val_data = data[n:]

def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x.to(device), y.to(device)

@torch.no_grad()
def estimate_loss(model):
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            _, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

def train_model(save_path='checkpoints/gpt_model.pth'):
    model = GPTLanguageModel(vocab_size).to(device)
    print(f"{sum(p.numel() for p in model.parameters())/1e6:.2f}M parameters")

    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    for iter in range(max_iters):
        if iter % eval_interval == 0 or iter == max_iters - 1:
            losses = estimate_loss(model)
            print(f"Step {iter}: Train loss {losses['train']:.4f}, Val loss {losses['val']:.4f}")

        xb, yb = get_batch('train')
        _, loss = model(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

    os.makedirs("checkpoints", exist_ok=True)
    print(f"Training voltooid. Model opslaan naar {save_path}...")
    torch.save(model.state_dict(), save_path)

    # Eventueel ook tokenizer opslaan
    with open("checkpoints/tokenizer.pt", "wb") as f:
        torch.save({'stoi': encode.__globals__['stoi'], 'itos': decode.__globals__['itos']}, f)

    print("Model en tokenizer succesvol opgeslagen.")

if __name__ == "__main__":
    train_model()
