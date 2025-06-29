import torch

# Hyperparameters - "Mild-Medium" Model
# Een goede balans tussen prestaties en stabiliteit.
# Vereist minder GPU-geheugen dan de zwaarste versie.

batch_size = 64      # Standaardwaarde, prima voor de meeste systemen
block_size = 512     # We houden het langere geheugen, dit is erg waardevol
max_iters = 50000    # Iets minder iteraties, past beter bij een iets kleiner model

eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200

# --- De "Stap Terug" Aanpassingen ---
n_embd = 512         # Terug van 768. Nog steeds breder dan de start (384).
n_head = 8           # Aangepast aan n_embd (512 is deelbaar door 8).
n_layer = 8          # Terug van 12. Nog steeds dieper dan de start (6).
# ------------------------------------

dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)