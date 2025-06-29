import torch


batch_size =      
block_size = 512  
max_iters = 60000   
eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200
n_embd = 768  
n_head = 12   
n_layer = 12        
dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)