# app.py
from flask import Flask, request, jsonify
import torch
from model import GPTLanguageModel, block_size, device
from tokenizer import encode, decode, load_tokenizer

app = Flask(__name__)

# Model en tokenizer laden bij opstarten
encode, decode, vocab_size = load_tokenizer()
model = GPTLanguageModel(vocab_size)
model.load_state_dict(torch.load("checkpoints/gpt_model.pth", map_location=device))
model.to(device)
model.eval()

@app.route("/generate", methods=["POST"])
def generate_response():
    data = request.get_json()
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Geen prompt meegegeven."}), 400

    tokens = encode(prompt)
    tokens = tokens[-block_size:]  # beperk context
    input_tensor = torch.tensor([tokens], dtype=torch.long, device=device)

    with torch.no_grad():
        output = model.generate(input_tensor, max_new_tokens=100)

    generated = output[0].tolist()[len(tokens):]
    answer = decode(generated).strip().split("\n")[0]
    return jsonify({"response": answer})

if __name__ == "__main__":
    app.run(debug=True)
