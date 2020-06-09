'''A script to convert each JSON file in Output into a text file where each sentence is separated by a new line'''
import json
import os

def convert():
	file_list=os.listdir("../Output")
	corpora=[]
	for file in file_list:
		if file.endswith(".json"):
			corpora.append(file)
		else:
			pass
	for corpus in corpora:
		print("Processing Corpus "+str(corpus))
		corpus_string=""
		with open("../Output/"+corpus,"r") as file_reader:
			json_object=json.load(file_reader)
		for sentence in json_object:
			sentence_string=""
			for word in sentence:
				if word==None:
					pass
				else:
					if not sentence_string:
						sentence_string=sentence_string+word
					else:
						sentence_string=sentence_string+" "+word
			corpus_string=corpus_string+"\n"+sentence_string
		with open("../Input/Sentences/"+corpus+".text","w+") as file_writer:
			file_writer.write(corpus_string)
			file_writer.close()
		print("Corpus Processed.")