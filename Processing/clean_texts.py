'''A script to clean each text (strip of stopwords) and then concatenate into a century long nested list of sentences

This script is used to build the initial Word2Vec models on each individual century, in order to provide a good model of whether Word2Vec could reliably be used
for Greek on periods as small as a single century'''

#Initialise list of centuries to process. This study only covers BCE.
centuries=[-800,-700,-600,-500,-400,-300,-200,-100]
#Initialise list of stopwords to be disincluded from Word2Vec
stopwords=["article","particle","conjunction","preposition"]

from lxml import etree
import json

#The json_list location can be changed as appropriate
def clean_century(century, json_list="../Output/rounded_dates.json", diorisis_location="../Input/Diorisis"):
	file_list=[]
	with open(json_list, "r") as json_reader:
		date_list=json.load(json_reader)
	for file in date_list:
		if date_list[file]==century:
			file_list.append(diorisis_location+"/"+file)
	#File list of all files which contain the texts for the century has been built. Now build a nested list of sentences.
	nested_century=[]
	print("Reading Files from Diorisis and Concatenating.")
	for file in file_list:
		with open(file, "r") as xml_reader:
			xml_file=xml_reader.read()
		parser=etree.XMLParser()
		text=etree.fromstring(xml_file, parser=parser)
		sentences=text.iter("sentence")
		for sentence in sentences:
			nested_sentence=[]
			for word in sentence:
				for lemma in word:
					if lemma.get("entry")==None:
						pass
					if lemma.get("POS") not in stopwords:
						import_lemma=lemma.get("entry")
						nested_sentence.append(import_lemma)
					else:
						pass
			nested_century.append(nested_sentence)
	return nested_century

def store_json(nested_century, file_name, json_location="../Output/"):
	with open(json_location+file_name,"w+") as json_writer:
		#Preserve the Greek forms with ensure_ascii set to false
		json.dump(nested_century, json_writer, ensure_ascii=False)
	print("Stored as: "+str(file_name))

for century in centuries:
	print("Cleaning: "+str(century))
	print("Storing Nested Century as JSON in Output at ")
	nested_century=clean_century(century)
	store_json(nested_century, file_name=str(century)+"_concatenated.json")
