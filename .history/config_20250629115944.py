import torch

# Hyperparameters - Aangepast voor stabiliteit
batch_size = 26      
block_size = 450     
max_iters = 20000    
eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200

# --- DE CORRECTIE ---
# We kiezen een n_embd die perfect deelbaar is door n_head.
n_embd = 408         
n_layer = 6          
n_head = 6           


dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)