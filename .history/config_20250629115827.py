import torch

# Hyperparameters - "Veilig & Krachtig" Model
# Ontworpen om te werken op GPU's met ~12GB VRAM zonder geheugenproblemen.
batch_size = 32      # Lager voor minder geheugengebruik
block_size = 450     # Langer geheugen voor betere context
max_iters = 20000    # Genoeg trainingstijd voor een groter model
eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200
n_embd = 410         # Een solide, brede basis
n_layer = 6          # Genoeg diepte voor complexiteit
n_head = 6           # Aangepast aan n_embd
dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)