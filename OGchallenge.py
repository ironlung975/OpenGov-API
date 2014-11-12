from flask import Flask, jsonify, request
import csv
import json
#import functions from own file for code cleanliness
from transformation import parse_num, aggregate

app = Flask(__name__)

#allow for the returned values to be in the correct order
app.config["JSON_SORT_KEYS"] = False

#storage objects for returning
key_indices = {}
rows_parsed = []
aggregations = {}

@app.route('/scrub', methods=['POST'])
def read_rows():
	header = True
	#Open the file as a string in order to read Mac csv line endings
	''' Code with windows line endings, since Mac line endings are unrecognizable from windows without a workaround, commented out this code
	f = StringIO.StringIO(request.files['file'].read())
	csv_f = csv.reader(f, delimiter=',')
	#Use splitlines function in order to recognize universal line endings
	for row in csv_f:
	'''
	#Code for dealing with universal line endings in windows
	csv_f = request.files['file'].read()
	for row in csv_f.splitlines():
		#store the header values
		if(header):
			i = 0
			for category in row.split(","): #because of the limits of mac line endings on windows, values that have commas in their field (e.g. 'Awards, Meetings & Misc') will be break the code without adding flexibility
				key_indices[category] = i
				i+=1
			header = False
			continue
		#check to make sure we do not print blank lines
		if not row.split(",")[0].strip() and row.split(",")[1].strip():
			continue
		else:
			#In each row, split the values by commas
			str_list = row.split(",")
			#put row list in json so that flask's jsonify does not break apart the list
			new_row = json.dumps(parse_num(str_list, key_indices))
			rows_parsed.append(new_row)

			#Create aggregations
			#get category values from row
			#Assuming that department names are unique so that they serve as correct keys instead of using the IDs
			year = str_list[key_indices["Year"]]
			#fund_id = str_list[key_indices["Fund ID"]]
			fund_name = str_list[key_indices["Fund Name"]]
			#dep_id = str_list[key_indices["Department ID"]]
			dep_name = str_list[key_indices["Department Name"]]
			amount = float(str_list[key_indices["Amount"]])
			if(aggregations.get(year)==None):
				#create new layers, API assumes that each entry will have both revenue and expenses for each year
				aggregations[year] = {"revenues": {"funds": {}, "departments": {}}, "expenses": {"funds": {}, "departments": {}}}
			aggregations[year] = aggregate(aggregations[year], amount, fund_name, dep_name)

	return jsonify({'rows_parsed' : rows_parsed, 'aggregations': aggregations}), 201


if __name__ == '__main__':
    app.run(debug=True)