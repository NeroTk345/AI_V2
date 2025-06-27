import torch
import os
from model import GPTLanguageModel
from tokenizer import encode, decode, vocab_size

from config import device, max_iters, eval_interval, eval_iters, learning_rate, batch_size, block_size

def get_batch(data, split):
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x.to(device), y.to(device)

@torch.no_grad()
def estimate_loss(model, data):
    model.eval()
    out = {}
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            x, y = get_batch(data[split], split)
            _, loss = model(x, y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

def main():
    os.makedirs("checkpoints", exist_ok=True)
    encode, _, vocab_size = get_tokenizer()
    with open("data/input.txt", "r", encoding="utf-8") as f:
        text = f.read()
    data = torch.tensor(encode(text), dtype=torch.long)
    split_idx = int(0.9 * len(data))
    dataset = {
        'train': data[:split_idx],
        'val': data[split_idx:]
    }

    model = GPTLanguageModel(vocab_size).to(device)
    print(f"{sum(p.numel() for p in model.parameters()) / 1e6:.2f}M parameters")
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    for iter in range(max_iters):
        if iter % eval_interval == 0:
            losses = estimate_loss(model, dataset)
            print(f"Step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")

        xb, yb = get_batch(dataset['train'], 'train')
        _, loss = model(xb, yb)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    torch.save(model.state_dict(), "checkpoints/gpt_model.pt")
    print("✅ Model opgeslagen in checkpoints/gpt_model.pt")

if __name__ == "__main__":
    main()
