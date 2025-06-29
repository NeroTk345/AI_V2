import torch



batch_size = 64      
block_size = 512     # We houden het langere geheugen, dit is erg waardevol
max_iters = 50000    # Iets minder iteraties, past beter bij een iets kleiner model

eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200


n_embd = 512        
n_head = 8           
n_layer = 8          

dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)