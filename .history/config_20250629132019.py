import torch
batch_size = 32     
block_size = 512   
max_iters = 20000   
eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200
n_embd = 384 
n_layer = 6 
n_head = 6        
dropout = 0.2
device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)