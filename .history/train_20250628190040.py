import os
    import torch
    from torch.utils.data import Dataset, DataLoader
    from model import GPTLanguageModel
    # We importeren nu de functies uit de aangepaste tokenizer
    from tokenizer import initialize_tokenizer, encode, save_tokenizer, vocab_size as tokenizer_vocab_size
    from config import * torch.backends.cuda.matmul.allow_tf32 = False
    torch.backends.cudnn.allow_tf32 = False

    torch.manual_seed(1337)

    class GPTDataset(Dataset):
        def __init__(self, data_tensor):
            self.data = data_tensor

        def __len__(self):
            return len(self.data) - block_size

        def __getitem__(self, idx):
            x = self.data[idx:idx+block_size]
            y = self.data[idx+1:idx+block_size+1]
            return x, y

    def train_model(save_path='checkpoints/gpt_model.pth'):
        # --- BELANGRIJKSTE WIJZIGING: DATA EENMALIG LADEN ---
        initialize_tokenizer()
        full_data_tensor = torch.tensor(encode(text), dtype=torch.long)
        # ---------------------------------------------------

        n = int(0.9 * len(full_data_tensor))
        train_data_tensor = full_data_tensor[:n]
        val_data_tensor = full_data_tensor[n:]

        train_dataset = GPTDataset(train_data_tensor)
        val_dataset = GPTDataset(val_data_tensor)
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4, pin_memory=True)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4, pin_memory=True)
        
        @torch.no_grad()
        def estimate_loss(model):
            out = {}
            model.eval()
            for split_name, loader in [('train', train_loader), ('val', val_loader)]:
                losses = torch.zeros(eval_iters)
                # Voeg een try-except blok toe voor robuustheid
                try:
                    for i, (X, Y) in enumerate(loader):
                        if i >= eval_iters:
                            break
                        X, Y = X.to(device), Y.to(device)
                        _, loss = model(X, Y)
                        losses[i] = loss.item()
                    out[split_name] = losses.mean()
                except Exception as e:
                    print(f"Fout tijdens loss estimatie voor {split_name}: {e}")
                    out[split_name] = -1 # Geef een foutwaarde terug
            model.train()
            return out

        model = GPTLanguageModel(tokenizer_vocab_size).to(device)
        print(f"{sum(p.numel() for p in model.parameters())/1e6:.2f}M parameters")
        print(f"Start training voor {max_iters} iteraties op device: {device}")

        optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
        
        train_iter = iter(train_loader)

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

        os.makedirs("checkpoints", exist_ok=True)
        print(f"Training voltooid. Model opslaan naar {save_path}...")
        torch.save(model.state_dict(), save_path)
        save_tokenizer()
        print("Model en tokenizer succesvol opgeslagen.")


    if __name__ == "__main__":
        train_model()