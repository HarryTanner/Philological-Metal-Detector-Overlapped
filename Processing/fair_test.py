'''A script to randomly test word embeddings in each corpus, with human input, to give an accuracy rating to the corpus'''
import json
from gensim.models import Word2Vec
import os
from os import path
import random

def get_vocabulary(model):
	#Get the dictionary of vocabulary from the model
	model_dictionary=model.wv.vocab
	word_list=[]
	for word in model_dictionary:
		word_list.append(word)
	return word_list

def get_two_words(word_model, unique_words_shuffled, length_words, used_words):
	#Initialise the similarity rating with a high similarity 
	similarity=float(0.55)
	#Loop while the similarity is not yet different (i.e. <0)
	if similarity>-0.9:
		#Get two random numbers within the range of the shuffled words list
		random_number_a=random.randint(1, length_words-1)
		random_number_b=random.randint(1, length_words-1)
		#Get the similarity of the two words
		similarity=word_model.similarity(unique_words_shuffled[random_number_a], unique_words_shuffled[random_number_b])
	elif unique_words_shuffled[random_number_a] in used_words:
		#Get two random numbers within the range of the shuffled words list
		random_number_a=random.randint(1, length_words-1)
		random_number_b=random.randint(1, length_words-1)
		#Get the similarity of the two words
		similarity=word_model.similarity(unique_words_shuffled[random_number_a], unique_words_shuffled[random_number_b])
	elif unique_words_shuffled[random_number_b] in used_words:
		#Get two random numbers within the range of the shuffled words list
		random_number_a=random.randint(1, length_words-1)
		random_number_b=random.randint(1, length_words-1)
		#Get the similarity of the two words
		similarity=word_model.similarity(unique_words_shuffled[random_number_a], unique_words_shuffled[random_number_b])
	#Check with the user if the words are good or not (i.e they are relatives or names)
	words_good=input("If Word A "+str(unique_words_shuffled[random_number_a])+" is not good, type N; if Word B "+str(unique_words_shuffled[random_number_b])+" is not good, type N; otherwise, type Y.")
	while words_good!="Y":
		#As long as the similarity remains similar, keep iterating until two different words are found
		if similarity>0:
			random_number_a=random.randint(1, length_words-1)
			random_number_b=random.randint(1, length_words-1)
			similarity=word_model.similarity(unique_words_shuffled[random_number_a], unique_words_shuffled[random_number_b])
		elif words_good=="N":
			random_number_a=random.randint(1, length_words-1)
			random_number_b=random.randint(1, length_words-1)
			similarity=word_model.similarity(unique_words_shuffled[random_number_a], unique_words_shuffled[random_number_b])
		elif unique_words_shuffled[random_number_a] in used_words:
			#Get two random numbers within the range of the shuffled words list
			random_number_a=random.randint(1, length_words-1)
			random_number_b=random.randint(1, length_words-1)
			#Get the similarity of the two words
			similarity=word_model.similarity(unique_words_shuffled[random_number_a], unique_words_shuffled[random_number_b])
		elif unique_words_shuffled[random_number_b] in used_words:
			#Get two random numbers within the range of the shuffled words list
			random_number_a=random.randint(1, length_words-1)
			random_number_b=random.randint(1, length_words-1)
			#Get the similarity of the two words
			similarity=word_model.similarity(unique_words_shuffled[random_number_a], unique_words_shuffled[random_number_b])
		#Check with the user again and loop again if necessary
		words_good=input("If Word A: "+str(unique_words_shuffled[random_number_a])+" or Word B: "+str(unique_words_shuffled[random_number_b])+" is not a good choice, type N; otherwise, type Y.")
	#Now two words have been selected, return them
	return unique_words_shuffled[random_number_a], unique_words_shuffled[random_number_b]

def store_vocabulary(dictionary):
	with open("../Output/Vocabulary/model_vocabulary.json","w+") as json_writer:
		#Store the dictionary safely and set ensure_ascii to false to preserve the Greek letters
		json.dump(dictionary, json_writer, ensure_ascii=False)

def fair_test():
	print("Calculating Unique Words in Each Century.")
	used_words=[]
	#Get list of models
	model_list=os.listdir("../Output/Models")
	list_models=[]
	for model in model_list:
		if model.endswith(".model"):
			list_models.append(model)
	#Initialise a dictionary for the results of the test
	nested_results={}
	#Iterate through the vocabulary and select one century at a time (including fake centuries)
	for century in list_models:
		#Set the score for the century to zero, this will be used later to guage the accuracy of the embeddings
		score=0
		#Load Word2Vec Model for appropriate century
		word_model=Word2Vec.load("../Output/Models/"+century)
		#Shuffle the words in the vocabulary for that century to dislodge order and provide a fair test
		unique_words_shuffled=get_vocabulary(word_model)
		random.shuffle(unique_words_shuffled)
		#Get the length of this list to generate random numbers
		length_words=len(unique_words_shuffled)
		#Generate a pseudo-random number within the list range to be used to randomly pull a word from the vocabulary
		random_number_a=int()
		random_number_b=int()
		#If the two numbers are the same, then loop until they are different. This is to ensure we get different words for comparison
		while random_number_a==random_number_b:
			#Ggenerate the random numbers as between 1 and the length of the vocabulary, to ensure it is a member of the list
			random_number_a=random.randint(1, length_words-1)
			random_number_b=random.randint(1, length_words-1)
		#Compare vectors for the two words
		#Start with i=0, while will only be the index of the number of times we have iterated (we want 5 word comparisons for a fair test)
		i=0
		while i<3:
			#A function to get two words with sufficiently different cosine measures that they are probably not in the same semantic field
			word_a, word_b=get_two_words(word_model, unique_words_shuffled, length_words, used_words)
			#Create a list of the two words (so they can be randomly shuffled for fairness. The user already knows what the words are possibly, so it is fine)
			words=[word_a, word_b]
			#Shuffle the words, now a and b are random and the user is not sure which is which
			random.shuffle(words)
			#Initialise a counter to keep track of which word is being tested
			counter=1
			#Initialise a dictionary from which the counter may be matched up against a word (which can be matched up against the word dictionary above)
			counter_dict={}
			#Toss a coin for the random int
			coin_toss=random.randint(1,2)
			#For each of the two words in the dictionary above...
			for word in words:
				#Tell the user which option they have. The screen will now present them with the most similar words for each word (in random order)
				counter_dict[counter]=word
				print("Option "+str(counter)+":")
				#Print the most similar words for the user
				print(word_model.most_similar(counter_dict[counter]))
				#Check if this word is the word that will be tested on, if so, store this counter as correct_answer 
				if coin_toss==counter:
					correct_answer=counter
				else:
					pass
				#Add one to the counter
				counter+=1
			#Ask the user to say which of the most similar words above is closest to the random produced by the coin toss
			answer=input("Which Option is Closest to "+str(counter_dict[correct_answer])+" ? Please type 1 or 2.")
			answer=int(answer)
			#If the user inputs 1 and 1 is the value of coin toss, then it must be correct
			if correct_answer==answer:
				#Since it is correct add 1 to the score for the century
				score=score+1
				print("Correct.")
			else:
				pass
			#Add one to the iterable
			i+=1
			print(word_model.most_similar(counter_dict[correct_answer]))
		#Get the final score for the century and divide it by 5 to make a float
		final_score=float(score/3)
		#Make a percentage and store it in the results dictionary for the century. When the program outputs the results, it will give the century next to the accuracy reading.
		nested_results[century]=final_score*100
		print("Your Score for the Above was: "+str(final_score))
	print("Finished Testing, Results (in percentages) are: ")
	print(nested_results)
	output_result(nested_results)

def output_result(results):
	with open("../Output/Accuracy/word2vec_accuracy.json","w+") as json_writer:
		json.dump(results, json_writer, ensure_ascii=False)
	json_writer.close()
