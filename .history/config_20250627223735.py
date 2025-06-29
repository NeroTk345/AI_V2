import torch

# Hyperparameters - "Medium" Model
# LET OP: Dit vereist een krachtige GPU met veel geheugen (>10 GB VRAM is aan te raden)

batch_size = 64      # Kun je hetzelfde houden, of verlagen naar 32 als je geheugenproblemen krijgt
block_size = 512     # Langer geheugen
max_iters = 60000    # Langer trainen
eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200
n_embd = 768  
n_head = 12   
n_layer = 12        
dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)