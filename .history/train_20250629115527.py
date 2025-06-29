import os
import torch
from torch.utils.data import Dataset, DataLoader
from model import GPTLanguageModel
import tokenizer  # Importeer de hele module
# Importeer de specifieke variabelen die we nodig hebben
from config import (device, batch_size, block_size, max_iters, learning_rate, 
                    eval_interval, eval_iters)

# --- Stabiliteits- en snelheidsinstellingen ---
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
torch.manual_seed(1337)

# --- De Dataset Klasse ---
# Deze is nu correct en gebruikt de block_size die hij meekrijgt.
class GPTDataset(Dataset):
    def __init__(self, data_tensor, block_size_arg):
        self.data = data_tensor
        self.block_size = block_size_arg

    def __len__(self):
        return len(self.data) - self.block_size

    def __getitem__(self, idx):
        x = self.data[idx:idx+self.block_size]
        y = self.data[idx+1:idx+self.block_size+1]
        return x, y

# --- De Hoofd Trainingsfunctie ---
def train_model(save_path='checkpoints/gpt_model.pth'):
    # Initialiseer de tokenizer en laad de data één keer
    tokenizer.initialize_tokenizer()
    full_data_tensor = torch.tensor(tokenizer.encode(tokenizer.text), dtype=torch.long)
    current_vocab_size = tokenizer.vocab_size

    # Splits de data
    n = int(0.9 * len(full_data_tensor))
    train_data_tensor = full_data_tensor[:n]
    val_data_tensor = full_data_tensor[n:]

    # Maak de datasets aan en geef block_size expliciet mee
    train_dataset = GPTDataset(train_data_tensor, block_size)
    val_dataset = GPTDataset(val_data_tensor, block_size)

    # Maak de DataLoaders aan
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0, pin_memory=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0, pin_memory=True)

    # --- De Loss Estimatie Functie (nu correct) ---
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

    # Initialiseer het model
    model = GPTLanguageModel(current_vocab_size).to(device)
    print(f"{sum(p.numel() for p in model.parameters())/1e6:.2f}M parameters")
    print(f"Start training voor {max_iters} iteraties op device: {device}")

    # Maak de optimizer aan
    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)

    # Maak de train_loader een oneindige iterator
    train_iter = iter(train_loader)

    # --- De Trainingsloop ---
    for iter_num in range(max_iters):
        if iter_num % eval_interval == 0 or iter_num == max_iters - 1:
            losses = estimate_loss(model)
            print(f"Step {iter_num}: Train loss {losses.get('train', -1):.4f}, Val loss {losses.get('val', -1):.4f}")

        try:
            xb, yb = next(train_iter)
        except StopIteration:
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
    tokenizer.save_tokenizer()
    print("Model en tokenizer succesvol opgeslagen.")


# --- De Start van het Script ---
if __name__ == "__main__":
    train_model()