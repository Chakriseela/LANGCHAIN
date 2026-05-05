from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

from huggingface_hub import login
login("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")

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

tokenizer = AutoTokenizer.from_pretrained(model_name)

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    dtype=torch.float32,     # safe for CPU
    # device_map="cpu"         # force CPU
)

input_text = "write code for prime numbers in python"
inputs = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**inputs, max_new_tokens=100)

print(tokenizer.decode(outputs[0]))