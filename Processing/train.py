'''A script to train Word2Vec in 300 dimensions for each corpus (including the shuffled and the diachronic)'''
from gensim.models import Word2Vec
import os
import time

def initialise_model(model_location="../Models/Overlap", corpus_location="../Texts/Second_Clean"):
	start_time=time.time()
	corpora=os.listdir(corpus_location)
	for corpus in corpora:
		if corpus.endswith(".text"):
			#Initialise model
			#Remove the ending .text from each corpus file
			model_corpus=corpus[:-5]
			#Train model in 300 dimensions, with skip-gram, read from text file to increase speed. Minimum count set at 1.
			print("Training Model for "+str(model_corpus))
			model=Word2Vec(corpus_file=corpus_location+"/"+corpus, size=500, min_count=1)
			model.save(model_location+"/"+"500_cbow"+model_corpus+".model")
			print("Finished Training.")
		else:
			pass
	end_time=time.time()
	difference=end_time-start_time
	print("Training Completed in "+str(int(difference))+" seconds")