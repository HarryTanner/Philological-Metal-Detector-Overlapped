'''
This script was used for the first, minimal clean on the texts required simply for the first evaluation of the Word2Vec model
A script to clean each text (strip of stopwords) and then concatenate into a century long nested list of sentences

This script is used to build the initial Word2Vec models on each individual century, in order to provide a good model of whether Word2Vec could reliably be used
for Greek on periods as small as a single century'''

#Initialise list of centuries to process. This study only covers BCE. This list does not include -500 because there is no data in Diorisis.
centuries=[-800,-700,-600,-400,-300,-200,-100,0]
#Initialise list of stopwords to be disincluded from Word2Vec
stopwords=["article","particle","conjunction","preposition"]

from lxml import etree
import json

#The json_list location can be changed as appropriate
def clean_century(century, json_list="../JSON/rounded_dates.json", diorisis_location="../Diorisis"):
	file_list=[]
	with open(json_list, "r") as json_reader:
		date_list=json.load(json_reader)
	for file in date_list:
		if date_list[file]==century:
			file_list.append(diorisis_location+"/"+file)
	#File list of all files which contain the texts for the century has been built. Now build a nested list of sentences.
	print("Reading Files from Diorisis and Concatenating.")
	corpus_string=""
	for file in file_list:
		with open(file, "r") as xml_reader:
			xml_file=xml_reader.read()
		parser=etree.XMLParser()
		text=etree.fromstring(xml_file, parser=parser)
		sentences=text.iter("sentence")
		for sentence in sentences:
			nested_sentence=""
			for word in sentence:
				for lemma in word:
					if lemma.get("POS") not in stopwords:
						if not lemma.get("entry"):
							pass
						else:
							import_lemma=lemma.get("entry")
							if not nested_sentence:
								nested_sentence=import_lemma
							else:
								nested_sentence=nested_sentence+" "+import_lemma
			corpus_string=corpus_string+"\n"+nested_sentence
	return corpus_string

def store_file(nested_century, file_name):
	with open(file_name,"w+") as file_writer:
		file_writer.write(nested_century)
		file_writer.close()

for century in centuries:
	print("Cleaning: "+str(century))
	file_name="../Texts/"+str(century)+".text"
	print("Storing Nested Century as text for training at "+file_name)
	nested_century=clean_century(century)
	store_file(nested_century, file_name)
