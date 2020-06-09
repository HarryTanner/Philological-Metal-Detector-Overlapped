'''This script performs the same cleaning operation as in second_clean, except it performs it on the shuffled centuries'''

centuries=[["a","b"],["b","c"],["c","d"],["d","e"],["e","f"],["f","g"],["g","h"]]

stopwords=["article","particle","conjunction","preposition","pronoun","proper"]

from lxml import etree
import json
import second_clean

for century in centuries:
	print("Cleaning now: "+str(century))
	nested_century=second_clean.clean_century(century, shuffled="y")
	print("Storing.")
	second_clean.convert_readable(nested_century, str(century[0])+"_"+str(century[1])+".text")