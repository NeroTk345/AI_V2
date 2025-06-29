# train.py (Geoptimaliseerde versie met DataLoader)

import os
import torch
from torch.utils.data import Dataset, DataLoader
from model import GPTLanguageModel
from tokenizer import text, encode, decode, vocab_size, save_tokenizer
from config import * # Importeer alles uit config.py

# --- DE OPLOSSING VOOR SNELHEID: SCHAKEL AGRESSIEVE OPTIMALISATIES UIT ---
# Deze laten we staan, omdat het de stabiliteit verbetert.
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
# -----------------------------------------------------------

torch.manual_seed(1337)

# --- Stap 1: Maak een custom Dataset klasse ---
class GPTDataset(Dataset):
    def __init__(self, data_tensor):
        self.data = data_tensor

    def __len__(self):
        # We kunnen niet de volledige lengte retourneren, maar het aantal mogelijke startpunten
        return len(self.data) - block_size

    def __getitem__(self, idx):
        # Pak een stukje data van de juiste lengte
        x = self.data[idx:idx+block_size]
        y = self.data[idx+1:idx+block_size+1]
        return x, y

def train_model(save_path='checkpoints/gpt_model.pth'):
    # --- Stap 2: Bereid de data en DataLoaders voor ---
    full_data_tensor = torch.tensor(encode(text), dtype=torch.long)
    n = int(0.9 * len(full_data_tensor))
    train_data_tensor = full_data_tensor[:n]
    val_data_tensor = full_data_tensor[n:]

    train_dataset = GPTDataset(train_data_tensor)
    val_dataset = GPTDataset(val_data_tensor)
    
    # num_workers > 0 gebruikt aparte processen om data te laden, wat veel sneller is.
    # pin_memory=True versnelt de data transfer naar de GPU.
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)
    

    @torch.no_grad()
    def estimate_loss(model):
        out = {}
        model.eval()
        for split_name, loader in [('train', train_loader), ('val', val_loader)]:
            losses = torch.zeros(eval_iters)
            for i, (X, Y) in enumerate(loader):
                if i >= eval_iters:
                    break
                X, Y = X.to(device), Y.to(device)
                _, loss = model(X, Y)
                losses[i] = loss.item()
            out[split_name] = losses.mean()
        model.train()
        return out

    # --- De rest van het trainingsproces ---
    model = GPTLanguageModel(vocab_size).to(device)
    print(f"{sum(p.numel() for p in model.parameters())/1e6:.2f}M parameters")
    print(f"Start training voor {max_iters} iteraties op device: {device}")

    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    
    # Maak de train_loader een oneindige iterator
    train_iter = iter(train_loader)

    for iter_num in range(max_iters):
        # Evalueer op het juiste interval
        if iter_num % eval_interval == 0 or iter_num == max_iters - 1:
            losses = estimate_loss(model)
            print(f"Step {iter_num}: Train loss {losses['train']:.4f}, Val loss {losses['val']:.4f}")

        # Haal de volgende batch op
        try:
            xb, yb = next(train_iter)
        except StopIteration:
            # Als de dataloader leeg is, begin opnieuw
            train_iter = iter(train_loader)
            xb, yb = next(train_iter)
        
        xb, yb = xb.to(device), yb.to(device)

        _, loss = model(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()

    # --- Opslaan na de training ---
    os.makedirs("checkpoints", exist_ok=True)
    print(f"Training voltooid. Model opslaan naar {save_path}...")
    torch.save(model.state_dict(), save_path)
    save_tokenizer()
    print("Model en tokenizer succesvol opgeslagen.")


if __name__ == "__main__":
    # Belangrijk: op Windows moet de code die multiprocessing gebruikt binnen deze blok staan
    train_model()