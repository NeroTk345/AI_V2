# In train.py

import os
import torch
from torch.optim.lr_scheduler import CosineAnnealingLR # <<< BELANGRIJK: import toevoegen
from model import GPTLanguageModel, block_size, device
from tokenizer import encode, decode, vocab_size, text, save_tokenizer

# ... (de rest van je imports en hyperparameters) ...

# ... (get_batch en estimate_loss functies blijven hetzelfde) ...

def train_model(save_path='checkpoints/gpt_model.pth'):
    # Zorg dat vocab_size van de NIEUWE tokenizer komt!
    model = GPTLanguageModel(vocab_size).to(device)
    print(f"{sum(p.numel() for p in model.parameters())/1e6:.2f}M parameters")

    optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)
    
    # Voeg de scheduler toe
    scheduler = CosineAnnealingLR(optimizer, T_max=max_iters, eta_min=learning_rate/10)
    
    # Houd de beste validation loss bij
    best_val_loss = float('inf')

    for iter in range(max_iters):
        if iter % eval_interval == 0 or iter == max_iters - 1:
            losses = estimate_loss(model)
            print(f"Step {iter}: Train loss {losses['train']:.4f}, Val loss {losses['val']:.4f}")

            # Sla het model op als de validation loss verbetert
            if losses['val'] < best_val_loss:
                best_val_loss = losses['val']
                os.makedirs("checkpoints", exist_ok=True)
                print(f"--> Nieuwe beste validation loss! Model wordt opgeslagen naar {save_path}")
                torch.save(model.state_dict(), save_path)

        xb, yb = get_batch('train')
        _, loss = model(xb, yb)
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        
        # Update de learning rate na elke stap
        scheduler.step()

    # save_tokenizer() hoeft hier niet per se, want die is al gemaakt, maar het kan geen kwaad.
    print("Training voltooid.")

if __name__ == "__main__":
    # Optioneel: verwijder het oude model zodat je zeker weet dat je met een schone lei begint
    if os.path.exists('checkpoints/gpt_model.pth'):
        print("Oud model gevonden en verwijderd.")
        os.remove('checkpoints/gpt_model.pth')
    train_model()