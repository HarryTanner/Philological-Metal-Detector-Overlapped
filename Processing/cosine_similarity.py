'''A script to run through the vocabulary common to each century, to then produce an inter-century cosine similarity with overlap.
Output will be cosine similarity for every common vocabulary entry for both real centuries and fake centuries.
Output to a CSV file for ease of portability to Google Sheets.'''

from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
import os
import csv
import time
import sys

def build_common_vocab(model_location="../Models/Overlap/"):
	print("Building vocabulary.")
	#Get all the words in the first model
	model_0=Word2Vec.load(model_location+"-800_-700.model")
	#Get all the words in the other models. These names need amending depending on the model names used
	other_models=[Word2Vec.load(model_location+"-700_-600.model"),Word2Vec.load(model_location+"-600_-400.model"),Word2Vec.load(model_location+"-400_-300.model"),Word2Vec.load(model_location+"-300_-200.model"),Word2Vec.load(model_location+"-200_-100.model"),Word2Vec.load(model_location+"-100_0.model")]
	mutual_words=[]
	for word in model_0.wv.vocab:
		keep=True
		for model in other_models:
			if word not in model.wv.vocab:
				keep=False
		if keep==True:
			mutual_words.append(word)
		else:
			pass
	return mutual_words

def write_csv():
	start_time=time.time()
	error_log=0
	common_vocab=build_common_vocab()
	check=""
	while check=="" or check=="S":
		check=input("Length of Vocabulary is "+str(len(common_vocab))+" Shall I Proceed? Y, N, or S. (Yes, No, Show vocab)")
		if check=="Y":
			total=len(common_vocab)
			counter=0
			with open("../Similarity/real_similarity_500_sg.csv","w+") as csv_writer:
				print("Calculating and Exporting Real Similarities for SG 500")
				columns=["word","-800 to -700_-600","-700 to -600_-400","-600 to -400_-300","-400 to -300_-200","-300 to -200_-100", "-200 to -100_0"]
				writer=csv.DictWriter(csv_writer, fieldnames=columns)
				writer.writeheader()
				for word in common_vocab:
					counter+=1
					real_dict, error_log=cosine_real(word, error_log)
					writer.writerow(real_dict)
					#Provide a progress count so you can head off to watch Lord of the Rings and check on it every so often to see how far through you are :-)
					print(counter/total)
			csv_writer.close()
			with open("../Similarity/shuffled_similarity.csv","w+") as csv_writer:
				print("Calculating and Exporting Shuffled Similarities.")
				columns=["word","a to b_c", "b to c_d", "c to d_e", "d to e_f", "e to f_g", "f to g_h"]
				writer=csv.DictWriter(csv_writer, fieldnames=columns)
				writer.writeheader()
				for word in common_vocab:
					counter+=1
					shuffled_dict, error_log=cosine_shuffled(word, error_log)
					writer.writerow(shuffled_dict)
					print(counter/total)
				csv_writer.close()
			end_time=time.time()
			difference=end_time-start_time
			print("Completed in "+str(difference)+" seconds.")
			print("Errors Reported: "+str(error_log))
		elif check=="N":
			print("Terminating.")
			sys.exit()
		elif check=="S":
			print(common_vocab)

def cosine_real(word, error_log, model_location="../Output/Models/Overlap/"):
	#Load each model in real
	real_models=["-800_-700.model","-700_-600.model","-600_-400.model","-400_-300.model","-300_-200.model","-200_-100.model","-100_0.model"]
	real_dict={}
	last_real=6
	real_dict["word"]=word
	for model in real_models:
		if real_models.index(model)!=last_real:
			current_model=Word2Vec.load(model_location+model)
			current_index=real_models.index(model)
			next_model=Word2Vec.load(model_location+real_models[current_index+1])
			#All words are supposed to be common, but a couple have slipped through the gaps (I suspect due to unicode problems, so the try is a failsafe)
			try:
				current_vector=current_model.wv[word]
				next_vector=next_model.wv[word]
				similarity=cosine(current_vector, next_vector)
			except:
				similarity=None
				print("Error.")
				error_log+=1
			real_dict[str(model[:-11]+" to "+real_models[real_models.index(model)+1][:-6])]=similarity
		else:
			pass
	return real_dict, error_log

def cosine_shuffled(word, error_log, model_location="../Output/Models/Overlap/"):
	shuffled_models=["a_b.model","b_c.model","c_d.model","d_e.model","e_f.model","f_g.model","g_h.model"]
	shuffled_dict={}
	shuffled_dict["word"]=word
	last_shuffled=6
	for model in shuffled_models:
		if shuffled_models.index(model)!=last_shuffled:
			current_model=Word2Vec.load(model_location+model)
			current_index=shuffled_models.index(model)
			next_model=Word2Vec.load(model_location+shuffled_models[current_index+1])
			#All words are supposed to be common, but a couple have slipped through the gaps (I suspect due to unicode problems, so the try is a failsafe)
			try:
				current_vector=current_model.wv[word]
				next_vector=next_model.wv[word]
				similarity=cosine(current_vector, next_vector)
			except:
				similarity=None
				error_log+=1
			shuffled_dict[str(model[:-8]+" to "+shuffled_models[shuffled_models.index(model)+1][:-6])]=similarity
		else:
			pass
	return shuffled_dict, error_log
