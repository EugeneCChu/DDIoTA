import spacy
import time

from flair.embeddings import *

from utils.speech_to_text import transcribe
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

    error_reading = ["Audio Intelligible",'Can not obtain results']

    while True:
        
        sentence = transcribe()

        if sentence not in error_reading:
            # Start timing
            #start = time.time()

            doc = nlp(sentence.lower())
            print_dependencies( doc )
        
            all_commands = cmd_extract( doc, nlp, embeddings )

            for single_command in all_commands:
                ap_command = final_device( single_command )
                ac_command = final_action( ap_command )

                print(ac_command)

            # End timing
            #print("\n--- %s seconds ---" % (time.time() - start))



            
            

            print('\n\n')
