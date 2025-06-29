import torch

# Hyperparameters - Aangepast voor stabiliteit
batch_size = 30      
block_size = 450     
max_iters = 20000    
eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200
n_embd = 450         
n_layer = 7          
n_head = 7          
dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)

import torch

# Hyperparameters - "Stabiel & Capabel" Model
# Deze configuratie is wiskundig correct en een uitstekend startpunt.

batch_size = 32      # Een veilige waarde voor het geheugen
block_size = 512     # Een goed, lang geheugen voor de AI
max_iters = 20000    
eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200

# --- DE DEFINITIEVE CORRECTIE ---
# We kiezen waarden die perfect deelbaar zijn en veel worden gebruikt.
n_embd = 384         # 384 is deelbaar door 6 (384 / 6 = 64)
n_layer = 6          # Een solide, standaard diepte
n_head = 6           # Een solide, standaard aantal aandachtskoppen
# --------------------------------

dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)