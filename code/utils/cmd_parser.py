from spacy.tokens import Token, Doc
from .bert_func import adp_child_is_parameter, word_is_conditional

def remove_words( sentence ):

    stopwords = ['please']
    for sw in stopwords:
        sentence = sentence.replace( sw, '' )

    return sentence

def cmd_extract(doc, nlp, embeddings):

    # Separates multiple cmdDoc in the input
    cmdDocs = []

    not_para_adps = ['to']

    end_pos = len(doc)

    for token in reversed(doc):
        if token.pos_ == "VERB" and token.dep_ == "conj":
            cmdDocs.append(nlp(doc[token.i : end_pos].text))
            end_pos = token.i - 1

    cmdDocs.insert(0, nlp(doc[token.i : end_pos].text))

    Token.set_extension("is_child_parameter", default=False, force=True)
    Token.set_extension("is_condition", default=False, force=True)
    Doc.set_extension("condition", default="No condition", force=True)

    for cmdDoc in cmdDocs:
        for tok in cmdDoc:
            if tok.pos_ == "ADP" and adp_child_is_parameter(cmdDoc, tok.text, embeddings):
                for t in tok.subtree:
                    t._.set("is_child_parameter", True)

            if word_is_conditional( cmdDoc, tok.text, embeddings ):

                condition = []

                # 'at', 'in' does not start condition on head
                if tok.text in ['at', 'in']:
                    startTok = tok
                else:
                    startTok = tok.head

                for t in startTok.subtree:
                    t._.set("is_condition", True)
                    condition.append(t.text)
                

                cmdDoc._.set("condition", ' '.join(condition))
                print(condition)
                

    print('cmdDocs:', cmdDocs)
    print('\n\n')
    parameters = []
    for cmdDoc in cmdDocs:

        # Stores (head, noun) pairs where noun is copied from head
        conj_dev_nouns = [
            (t.head, t)
            for t in cmdDoc
            if t.pos_ in ["NOUN", "PRON"] and t.dep_ == "conj" and t._.is_child_parameter == False and t._.is_condition == False 
        ]

        conj_parameter_nouns = [
            (t.head, t)
            for t in cmdDoc
            if t.pos_ == "NOUN" and t.dep_ == "conj" and t._.is_child_parameter == True and t._.is_condition == False 
        ]

        non_conj_dev_nouns = [
            t
            for t in cmdDoc
            if t.pos_ in ["NOUN", "PRON"] and t.dep_ != "conj" and t._.is_child_parameter == False and t._.is_condition == False 
        ]
        non_conj_parameter_nouns = [
            t
            for t in cmdDoc
            if t.pos_ == "NOUN" and t.dep_ != "conj" and t._.is_child_parameter == True and t._.is_condition == False 
        ]

        verb_adps = [
            t for t in cmdDoc if t.dep_ in ["prep", "prt"] and t.head.pos_ == "VERB" and t._.is_condition == False and t.text not in not_para_adps
        ]

        verbs = [t for t in cmdDoc if t.pos_ == "VERB" and t._.is_condition == False ]

        print('command: ', cmdDoc)
        print('non_conj_dev_nouns: ', non_conj_dev_nouns)
        print('non_conj_parameter_nouns: ', non_conj_parameter_nouns)
        print('conj_dev_nouns: ', conj_dev_nouns)
        print('conj_parameter_nouns: ', conj_parameter_nouns)
        print('verbs: ', verbs)
        print('verb_adps: ', verb_adps)
        print('conditions: ', cmdDoc._.condition)
        print('\n\n')

        try:
            assert len(non_conj_parameter_nouns) <= 1
        except:
            print("More than one non conjugated parameter noun: ", non_conj_parameter_nouns)
            return None
        try:
            assert len(non_conj_dev_nouns) == 1

        except:
            print("More than one non conjugated device noun: ", non_conj_dev_nouns)
            return None
        try:
            assert len(verbs) == 1
        except:
            print("Not only one verb: ", verbs)
            return None





        # Final answer dictionary --> DEVICE: [ ACTION, PARAMETER, CONDITION ]
        commands = {
            device: [verbs[0], "No parameter", cmdDoc._.condition]
            for device in non_conj_dev_nouns
        }

        # ADP possibilities
        for adp in verb_adps:
            if len(list(adp.children)) == 0:
                for device in commands.keys():
                    commands[device][1] = adp


        # Noun possibilities
        for noun in non_conj_dev_nouns + non_conj_parameter_nouns:
            if noun.dep_ in ["dobj", "nsubj", "nsubjpass"]:  # head is VERB
                commands[noun][0] = noun.head

            elif noun.dep_ == "pobj":  # head is ADP
                if noun.head._.is_child_parameter:
                    # ADP + NOUN is PARAMETER, and the DEVICE is the non conjugate device
                    action = noun.head.head
                    device = non_conj_dev_nouns[0]

                    if str(commands[device][1]) == "No parameter":
                        commands[device][1] = noun

                elif noun.head.text not in not_para_adps:
                    # head ADP is not part of parameter, and the DEVICE is the noun
                    commands[noun][1] = noun.head

        for device in commands.keys():
            parameters.append([device] + commands[device])


        # Copy first conj_parameter, then conj_dev
        for s1, s2 in conj_parameter_nouns:
            for parameter in parameters:
                if s1 == parameter[2]:
                    parameters.append([parameter[0], parameter[1], s2, parameter[3]])

        for s1, s2 in conj_dev_nouns:
            for parameter in parameters:
                if s1 == parameter[0]:
                    parameters.append([s2, parameter[1], parameter[2], parameter[3]])

    # Reorder as ACTION DEVICE PARAMETER CONDITION ( in text )
    # Remove words such as the, a
    all_commands = []
    for parameter in parameters:
        parameter[0], parameter[1] = parameter[1], parameter[0]
        command = [str(p).replace("the ", "") for p in parameter]
        command = [p.replace("a ", "") for p in command]
        all_commands.append(command)
    
    return all_commands
