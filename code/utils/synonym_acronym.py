from nltk.corpus import wordnet


def handle_syn_acr(wordin):
    synonyms = []
    acronyms = []
    syns = wordnet.synsets(wordin)

    for item in syns:
        name = item.name()
        if name.split(".")[0] not in synonyms:
            synonyms.append(name.split(".")[0])

    if len(wordin.split(" ")) > 1:
        words = wordin.split(" ")
        acr_out = ""
        for item in words:
            acr_out += item[0].upper()
        acronyms.append(acr_out)

    return synonyms, acronyms


if __name__ == "__main__":
    syn, acr = handle_syn_acr("switch")
    print(syn, acr)
