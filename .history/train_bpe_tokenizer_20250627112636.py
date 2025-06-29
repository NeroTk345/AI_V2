# train_bpe_tokenizer.py

import os
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.trainers import BpeTrainer
from tokenizers.pre_tokenizers import Whitespace

# Zorg ervoor dat de 'checkpoints' map bestaat
os.makedirs("checkpoints", exist_ok=True)

# 1. Initialiseer een lege BPE (Byte-Pair Encoding) tokenizer
tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
tokenizer.pre_tokenizer = Whitespace()

# 2. Maak een trainer voor de tokenizer
#    - vocab_size: Hoeveel unieke "woorddelen" de tokenizer moet leren. 5000 is een goed startpunt.
#    - special_tokens: Tokens die we willen toevoegen, zoals een token voor onbekende woorden.
trainer = BpeTrainer(vocab_size=5000, special_tokens=["[UNK]", "[PAD]"])

# 3. Train de tokenizer op je dataset
#    Geef het pad naar je tekstbestand op.
files = ["./data/input.txt"]
tokenizer.train(files, trainer)

# 4. Sla de getrainde tokenizer op
#    Dit creëert een .json bestand dat de regels en het vocabulaire bevat.
output_path = "checkpoints/bpe_tokenizer.json"
tokenizer.save(output_path)

print(f"BPE Tokenizer succesvol getraind en opgeslagen in: {output_path}")
print(f"Nieuwe vocabulaire grootte (vocab_size): {tokenizer.get_vocab_size()}")