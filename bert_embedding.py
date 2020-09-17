import torch
import pandas as pd
from time import time
from typing import List
from transformers import BertTokenizer, BertModel

BERT_UNCASED = 'bert-base-uncased'
tokenizer = BertTokenizer.from_pretrained(BERT_UNCASED)
bert_model = BertModel.from_pretrained(BERT_UNCASED)
bert_model = bert_model.cuda()

def pad_items(list_of_lists):
    """Right-padding of all within a list of lists, respecting BERT's input size limit (512).
    """
    padded = []
    pad_len = 512
    for sublist in list_of_lists:
        len_to_pad = pad_len - len(sublist)
        if len_to_pad < 0:
            padded.append(sublist[:pad_len])
        else:
            padded.append(sublist + [0] * len_to_pad)
    
    assert all([len(token) == 512 for token in padded]), \
        "Padding length didn't meet BERT's treshold."

    return padded

def generate_embeddings(alist: List[str], batch_size=100):
    """Utilizes the BERT pre-trained model to generate embeddings for all within `alist`.

    Args:
        alist (list): The list of textual values for which to embed.
        batch_size (int): The number o items to embed per iteration through the model.

    Returns:
        (torch.Tensor): BERT's embeddings representing the items in `alist`.
    """
    sep = [tokenizer.tokenize('[CLS] ' + txt + ' [SEP]') for txt in alist]

    tokens = [tokenizer.convert_tokens_to_ids(txt) for txt in sep]
    tokens = pad_items(tokens)

    results = torch.zeros((len(tokens), bert_model.config.hidden_size)).long()

    started = time()
    with torch.no_grad():
        for stidx in range(0, len(tokens), batch_size):
            X = tokens[stidx:stidx + batch_size]
            X = torch.LongTensor(X).cuda()
            _, pooled_output = bert_model(X)
            results[stidx:stidx + batch_size, :] = pooled_output.cpu()
    
    print(f'Finished BERT embeddings after {time() - started:.2f}s')
    return results