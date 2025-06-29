import torch

# Hyperparameters - "Veilig & Krachtig" Model
# Ontworpen om te werken op GPU's met 12GB VRAM zonder geheugenproblemen.

# --- DE BELANGRIJKSTE AANPASSING OM GEHEUGEN TE BESPAREN ---
batch_size = 32      # Terug van 64. Dit halveert het geheugengebruik van de data.
# ---------------------------------------------------------

block_size = 256    # We houden het langere geheugen, dit is erg waardevol
max_iters = 10000    # Genoeg trainingstijd voor dit model

eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200

# --- Modelgrootte blijft krachtig, maar past nu wel ---
n_embd = 512         # Een solide, brede basis
n_layer = 8          # Genoeg diepte voor complexiteit
n_head = 8           # Aangepast aan n_embd (512 is deelbaar door 8)

dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)