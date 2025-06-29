import torch

# Hyperparameters - "Krachtig" Model
# Dit is nodig om de link tussen vraag en antwoord goed te leren

batch_size = 64      
block_size = 512     
max_iters = 80000    # Langer trainen om de diepere verbanden te leren

eval_interval = 500
learning_rate = 3e-4 
eval_iters = 200

# --- De "Krachtige" Aanpassingen ---
n_embd = 768         # Breder model voor meer detail
n_layer = 12         # Dieper model voor beter begrip
n_head = 12          # Aangepast aan n_embd (768 is deelbaar door 12)
# ------------------------------------

dropout = 0.2

device = 'cuda' if torch.cuda.is_available() else 'cpu'
torch.manual_seed(1337)