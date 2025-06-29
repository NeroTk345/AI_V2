# tokenizer.py (Nieuwe versie)

from tokenizers import Tokenizer

# Pad naar het getrainde tokenizer-bestand
TOKENIZER_PATH = "checkpoints/bpe_tokenizer.json"

# Laad de getrainde tokenizer vanuit het bestand
tokenizer = Tokenizer.from_file(TOKENIZER_PATH)

# Haal de vocab_size direct uit de tokenizer
vocab_size = tokenizer.get_vocab_size()

# Definieer de encode en decode functies met de nieuwe tokenizer
def encode(s: str) -> list[int]:
    return tokenizer.encode(s).ids

def decode(l: list[int]) -> str:
    return tokenizer.decode(l)

# Je hebt geen save/load functies meer nodig hier, alles staat in het .json bestand.