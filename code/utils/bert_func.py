import torch
import numpy as np
from flair.data import Sentence
from sklearn.metrics.pairwise import cosine_similarity as cos


def cos_compare(word, sentences, embeddings):

    ss = [Sentence(s.lower()) for s in sentences]  # Change to flair format
    compare = []

    for s in ss:
        embeddings.embed(s)
        for tok in s:
            if tok.text == word:
                compare.append(tok.embedding)

    compare = torch.stack(compare).cpu().clone().numpy()

    return cos(compare, compare)[2]


def adp_child_is_parameter(doc, word, embeddings):
    """ Check whether the adp "word" in doc is part of parameter """

    if word == "on":
        sentences = [
            "Turn on the lights",
            "Put the cup on the table",
        ]
    elif word == "up":
        return True

    elif word == "off":
        return False

    elif word == "to":
        sentences = [
            "Connect to my laptop",
            "Set the temperature to mild"
        ]

    else:
        #print(
        #    "INFO: '{}' not used in comparisons, assume that it is part of parameter...".format(
        #        word
        #    )
        #)
        return True

    sentences.append(doc.text)
    results = cos_compare(word, sentences, embeddings)
    
    return results[0] < results[1]


def word_is_conditional(doc, word, embeddings):
    """ Check if the "word" is for a condition """

    if word in ["if", "at"]:
        return True

    elif word == "while":
        sentences = [
            "The car won't be coming for a while",
            "Strike the iron while it is hot",
        ]

    elif word == "when":
        sentences = [
            "When does the bus come", 
            "Open the door when he arrives",
        ]


    else:
        #print(
        #    "INFO: '{}' not used in comparisons, assume that it is not part of a conditional...".format(word)
        #)
        return False

    sentences.append(doc.text)
    results = cos_compare(word, sentences, embeddings)

    return results[0] < results[1]


