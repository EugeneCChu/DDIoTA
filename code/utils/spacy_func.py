def merge_compound(doc):
    """Merge compounds with it's parents."""

    if not doc.is_parsed:
        return doc

    to_merge_deps = ["compound", "nummod"]

    with doc.retokenize() as retokenizer:
        for token in doc:
            if token.dep_ in to_merge_deps:

                beg = min(token.i, token.head.i)
                end = max(token.i, token.head.i)
                retokenizer.merge(doc[beg : end + 1])

        for ent in doc.ents:
            retokenizer.merge(ent, {"pos": "NOUN"})

    return doc


def print_dependencies(doc):

    hdr = ["text", "dependency", "parent", "coarse POS", "children"]
    row_format = "{:<25}" * (len(hdr))
    line = "-" * 25 * len(hdr)

    print(row_format.format(*hdr))
    print(line)
    for token in doc:
        print(
            row_format.format(
                *[
                    token.text,
                    token.dep_,
                    token.head.text,
                    token.pos_,
                    ", ".join([str(child) for child in token.children]),
                ]
            )
        )
    print(line)
