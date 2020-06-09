'''A script to run through the vocabulary common to each century, to then produce an inter-century cosine similarity with overlap.
Output will be cosine similarity for every common vocabulary entry for both real centuries and fake centuries.
Output to a CSV file for ease of portability to Google Sheets.'''

from gensim.models import Word2Vec
from scipy.spatial.distance import cosine
import os
import csv
import time
import sys

def build_common_vocab(model_location="../Output/Models/Overlap/"):
	print("Building vocabulary.")
	#Get all the words in the first model
	model_0=Word2Vec.load(model_location+"500_-800_-700.model")
	model_0_words=[]
	for word in model_0.wv.vocab:
		if word!=None:
			model_0_words.append(word)
	#Get all the words in the other models
	other_models=["500_-700_-600.model","500_-600_-400.model","500_-400_-300.model","500_-300_-200.model","500_-200_-100.model","500_-100_-000.model"]
	other_words=[]
	for model in other_models:
		nested_words=[]
		loaded_model=Word2Vec.load(model_location+model)
		for word in loaded_model.wv.vocab:
			if word!=None:
				nested_words.append(word)
		other_words.append(nested_words)
	#For every nested model's words, iterate through model_0_words. If a word is not in nested_model, then delete it
	for nested in other_words:
		for word in model_0_words:
			if word not in nested:
				model_0_words.remove(word)
	return model_0_words

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
			with open("../Output/Similarity/real_similarity_500_sg.csv","w+") as csv_writer:
				print("Calculating and Exporting Real Similarities for SG 500")
				columns=["word","500_-800 to 500_-700_-600","500_-700 to 500_-600_-400","500_-600 to 500_-400_-300","500_-400 to 500_-300_-200","500_-300 to 500_-200_-100", "500_-200 to 500_-100_-000"]
				writer=csv.DictWriter(csv_writer, fieldnames=columns)
				writer.writeheader()
				for word in common_vocab:
					counter+=1
					real_dict, error_log=cosine_real(word, error_log)
					writer.writerow(real_dict)
					print(counter/total)
			csv_writer.close()
			'''with open("../Output/Similarity/shuffled_similarity.csv","w+") as csv_writer:
				print("Calculating and Exporting Shuffled Similarities.")
				columns=["word","a to b_c", "b to c_d", "c to d_e", "d to e_f", "e to f_g", "f to g_h"]
				writer=csv.DictWriter(csv_writer, fieldnames=columns)
				writer.writeheader()
				for word in common_vocab:
					counter+=1
					shuffled_dict, error_log=cosine_shuffled(word, error_log)
					writer.writerow(shuffled_dict)
					print(counter/total)
				csv_writer.close()'''
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
	real_models=["500_-800_-700.model","500_-700_-600.model","500_-600_-400.model","500_-400_-300.model","500_-300_-200.model","500_-200_-100.model","500_-100_-000.model"]
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
