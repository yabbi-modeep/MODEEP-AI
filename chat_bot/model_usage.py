# # byt5 usage

# from transformers import T5ForConditionalGeneration, AutoTokenizer, AutoModelForSeq2SeqLM
# import torch

# model = T5ForConditionalGeneration.from_pretrained('google/byt5-small')
# tokenizer = AutoTokenizer.from_pretrained('google/byt5-small')

# # model_inputs = tokenizer(["Life is like a box of chocolates.", "Today is Monday."], padding="longest", return_tensors="pt")
# # labels = tokenizer(["La vie est comme une boîte de chocolat.", "Aujourd'hui c'est lundi."], padding="longest", return_tensors="pt").input_ids

# input_ids_prompt = ""
# input_ids = tokenizer(input_ids_prompt).input_ids
# input_ids = torch.tensor([input_ids[:8] + [258] + input_ids[14:21] + [257] + input_ids[28:]])

# output_ids = model.generate(input_ids, max_length=100)[0].tolist()

# output_ids_list = []
# start_token = 0
# sentinel_token = 258

# while sentinel_token in output_ids:
#   split_idx = output_ids.index(sentinel_token)
#   output_ids_list.append(output_ids[start_token:split_idx])
#   start_token = split_idx
#   sentinel_token = -1

# # loss = model(**model_inputs, labels=labels).loss # forward pass

# # gemma usage

from transformers import AutoTokenizer, AutoModelForCausalLM
from keys import access_token
import torch

tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it", token=access_token)
model = AutoModelForCausalLM.from_pretrained(
    "google/gemma-2b-it",
    torch_dtype=torch.bfloat16,
    token=access_token
)

input_text = "Write me a poem about Machine Learning."
input_ids = tokenizer(input_text, return_tensors="pt")

outputs = model.generate(**input_ids)
print(tokenizer.decode(outputs[0]))
