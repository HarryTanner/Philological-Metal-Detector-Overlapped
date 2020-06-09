'''A script to convert the 3 digit dates in Diorisis into broader century dates which makes processing easier
The script:
1) Takes Diorisis in the Input folder (this argument can be respecified) and parses it with lxml (will need installing)
2) Get the date and convert to a century
3) Insert names of file as key and century as value into JSTOR object'''

import os
from lxml import etree
import json
import time

#Initialise start time for measures
start_time=time.time()

def round_dates(directory="../Input/Diorisis"):
	print("Rounding Dates.")
	rounded_dates={}
	diorisis_files=os.listdir(directory)
	for file in diorisis_files:
		with open(directory+"/"+file) as xml_reader:
			xml_file=xml_reader.read()
			xml_reader.close()
		parser=etree.XMLParser()
		text=etree.fromstring(xml_file, parser=parser)
		creation=text.iter("creation")
		for item in creation:
			for date_tag in item:
				date=int(date_tag.text)
		#Round the date down
		rounded_date=int(date/100)*100
		rounded_dates[file]=rounded_date
	export_to_json(rounded_dates)

#Export to JSON, directory can be changed if necessary
def export_to_json(rounded_dates, directory="../Output/rounded_dates.json"):
	print("Exporting to JSON file at: "+str(directory))
	with open(directory, "w+") as json_writer:
		json.dump(rounded_dates, json_writer)
	print("Success.")

round_dates()
end_time=time.time()
different=end_time-start_time
print("Executed in: "+str(different)+" seconds.")