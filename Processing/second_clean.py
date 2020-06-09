'''Having established a test on a single century, this script cleans for a second time and formats the texts for the real centuries in a format
ready to be read from the disk for training in Word2Vec. In order to make the cosine similarities faster, it was necessary to strip out pronouns and 
proper nouns at this stage (which will also aid modelling).

'''

centuries=[[-800,-700],[-700,-600],[-600,-400],[-400,-300],[-300,-200],[-200,-100],[-100, 0]]
stopwords=["article","particle","conjunction","preposition","pronoun","proper"]

from lxml import etree
import json

#The json_list location can be changed as appropriate
def clean_century(century, shuffled, json_list="../Output/rounded_dates.json", diorisis_location="../Input/Diorisis"):
	#Takes the overlapping centuries and combines them
	if shuffled=="y":
		file_list=[]
		with open("../Output/shuffled_files.json", "r") as json_reader:
			print("Reading Shuffled list.")
			date_dictionary=json.load(json_reader)
		date_list={}
		for shuffled_century in date_dictionary:
			for item in date_dictionary[shuffled_century]:
				date_list[item]=shuffled_century
		for file in date_list:
			if date_list[file] in century:
				file_list.append(diorisis_location+"/"+file)
	elif shuffled=="n":
		file_list=[]
		with open(json_list, "r") as json_reader:
			date_list=json.load(json_reader)
		for file in date_list:
			if date_list[file] in century:
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

def convert_readable(nested_century, file_name, location="../Input/Overlap"):
	full_nested=""
	for sentence in nested_century:
		nested_sentence=""
		for word in sentence:
			if not nested_sentence:
				nested_sentence=word
			elif not word:
				pass
			else:
				nested_sentence=nested_sentence+" "+word
		if not nested_sentence:
			pass
		elif not full_nested:
			full_nested=nested_sentence
		else:
			full_nested=full_nested+"\n"+nested_sentence
	with open("../Input/Overlap/"+file_name,"w+") as file_writer:
		file_writer.write(full_nested)
	file_writer.close()
	print("Written to File.")

def start():
	for century in centuries:
		overlap_century=clean_century(century, shuffled="n")
		convert_readable(overlap_century, str(century[0])+"_"+str(century[1])+".text")