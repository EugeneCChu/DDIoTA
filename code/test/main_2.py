import spacy
import time
import numpy as np
from flair.embeddings import *

from utils.cmd_parser import cmd_extract
from utils.spacy_func import merge_compound, print_dependencies
from utils.mappings import final_device, final_action
if __name__ == "__main__":

    # Load models and word embeddings
    nlp = spacy.load( "en_core_web_lg" )
    nlp.add_pipe( nlp.create_pipe("merge_noun_chunks") )
    nlp.add_pipe( merge_compound )

    embeddings = StackedEmbeddings([BertEmbeddings(
    bert_model_or_path="bert-base-uncased", layers="-1,-2,-3,-4"
    )])

    f = open("commands.txt", "r")
    cnt = 0
    sentence = 'start'
    total_length = {}
    while sentence:
        try:
            start = time.time()
            sentence = f.readline()
            sentence.replace('\n','')
            print(sentence)
            broken_s = sentence.split(' ')
            
            cnt+=1
            # Start timing
            

            doc = nlp(sentence.lower())
            print_dependencies( doc )
        
            all_commands = cmd_extract( doc, nlp, embeddings )

            for single_command in all_commands:
                ap_command = final_device( single_command )
                ac_command = final_action( ap_command )

                print(ac_command)

            if len(broken_s) in total_length.keys():
                total_length[len(broken_s)].append(time.time() - start)
            else:
                total_length[len(broken_s)] = [time.time() - start]
            # End timing
            print("\n--- %s seconds ---" % (time.time() - start))



        except Exception as e:
            print('\nERROR for command \'{}\'\n\t{}'.format( sentence, str(e)) )
            pass
        

        print('\n\n')
    #print(total_length)
    for item in total_length.keys():
        print('%d: total of %d commands with average processing time of %.3f seconds.'%(item,len(total_length[item]),np.mean(total_length[item])))
