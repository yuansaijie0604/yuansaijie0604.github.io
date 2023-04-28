"""
transformer-xl
"""

TRANSFO_XL_MODEL = "TRANSFO_XL"

# from transformers import AutoTokenizer, TransfoXLModel
# import torch
#
# tokenizer = AutoTokenizer.from_pretrained("transfo-xl-wt103")
# model = TransfoXLModel.from_pretrained("transfo-xl-wt103")
#
# inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
# print(inputs)
#
# # 想看memory模块的运行原理
# inputs["input_ids"] = torch.randint(0, 267734, (1, 200005))
#
# outputs = model(**inputs)
#
# last_hidden_states = outputs.last_hidden_state

"""
longformer
"""

LONGFORMER_MODEL = "longformer"

import torch
from transformers import LongformerModel, AutoTokenizer, LongformerConfig

tokenizer = AutoTokenizer.from_pretrained("allenai/longformer-base-4096")
# model = LongformerModel.from_pretrained("allenai/longformer-base-4096")

configuration = LongformerConfig.from_json_file("allenai/longformer-base-4096")
configuration.attention_window = [4] * 2
configuration.hidden_size = 6
configuration.intermediate_size = 24
configuration.num_attention_heads = 2
configuration.num_hidden_layers = 2

model = LongformerModel(config=configuration)

# SAMPLE_TEXT = " ".join(["Hello world! "] * 1000)  # long input document
# input_ids = torch.tensor(tokenizer.encode(SAMPLE_TEXT)).unsqueeze(0)  # batch of size 1

input_ids = torch.tensor(tokenizer.encode("hello world yes no ok")).unsqueeze(0)

attention_mask = torch.ones(
    input_ids.shape, dtype=torch.long, device=input_ids.device
)  # initialize to local attention
global_attention_mask = torch.zeros(
    input_ids.shape, dtype=torch.long, device=input_ids.device
)  # initialize to global attention to be deactivated for all tokens
global_attention_mask[
    :,
    [1, 3],
] = 1  # Set global attention to random tokens for the sake of this example
# Usually, set global attention based on the task. For example,
# classification: the <s> token
# QA: question tokens
# LM: potentially on the beginning of sentences and paragraphs
outputs = model(
    input_ids,
    attention_mask=attention_mask,
    global_attention_mask=global_attention_mask,
)
sequence_output = outputs.last_hidden_state
pooled_output = outputs.pooler_output
