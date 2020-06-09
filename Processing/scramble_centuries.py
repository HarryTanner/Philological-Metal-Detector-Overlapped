'''This script scrambles each century to provide a fair comparison (as per Dubossarsky) to check word meaning shift'''

import json
import random

def scramble(json_location="../JSON/rounded_dates.json"):
	#Get the files for each century, count them, and create a list of all files
	with open(json_location, "r") as json_reader:
		rounded_json=json.load(json_reader)
		json_reader.close()
	file_count=0
	all_files=[]
	for text in rounded_json:
		all_files.append(text)
		file_count+=1
	#Shuffle the list to make it fair
	random.shuffle(all_files)
	#There are 8 centuries in this study, and we need to compute an average number of files per century. If this average becomes a floating point, minus to the nearest multiple of 8. 
	division=int(file_count/8)
	while division*8!=file_count:
		print(division)
		file_count=file_count-1
		division=int(file_count/8)
		all_files.remove(all_files[0])
	random.shuffle(all_files)
	summation=len(all_files)
	#Allocate each file to a random century (fake centuries are given letters, not numbers)
	centuries=["a","b","c","d","e","f","g","h"]
	century_counter=0
	shuffled_dictionary={}
	divider=division
	for century in centuries:
		nested_century_list=[]
		while century_counter<divider:
			print(century_counter)
			nested_century_list.append(all_files[century_counter])
			century_counter+=1
		if divider!=summation:
			divider=divider+division
		else:
			pass
		shuffled_dictionary[century]=nested_century_list
	return shuffled_dictionary

def store_scrambles(shuffled_dictionary, json_location="../JSON/shuffled_files.json"):
	with open(json_location,"w+") as json_writer:
		json.dump(shuffled_dictionary, json_writer, ensure_ascii=False)

shuffled_dictionary=scramble()
store_scrambles(shuffled_dictionary)
print("Success!")