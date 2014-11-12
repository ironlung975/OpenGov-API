from math import fabs
import re

#function to change values into their raw values (if not strings, such as floats and ints)
def parse_num(str_list, keys):
	new_list = []
	index = 0
	for s in str_list:
		if (s.isdigit()):
			s = int(s)
		#check for index, but since some columns may include commas, (which is the delimiter in the csv) need to ensure that amount is a float
		#how the code really should be, I fudged with it in order to fix it so I could see the test data
		if (index==keys['Amount']):
		#commented out version to work with csv files with comma delimiters within the column
		#if (abs(index-keys['Amount']) <=1 and len(re.findall("\d+.\d+", s))>0):
		
			s = float(s)
		new_list.append(s)
		index+=1
	return new_list

def helper_aggregate(year_dict, type_money, dimension, key, amount):
	#store values or aggregate as necessary
	if(year_dict[type_money][dimension].get(key) == None):
		year_dict[type_money][dimension][key] = amount
	else:
		year_dict[type_money][dimension][key] += amount
	return year_dict

def aggregate(year_dict, num, fund_name, dep_name):
	type_money = ""
	if(num >= 0):
		type_money = "revenues"
		anti_type_money = "expenses"
	else:
		type_money = "expenses"
		anti_type_money = "revenues"
	year_dict = helper_aggregate(year_dict, type_money, "funds", fund_name, fabs(num))
	year_dict = helper_aggregate(year_dict, type_money, "departments", dep_name, fabs(num))
	year_dict = helper_aggregate(year_dict, anti_type_money, "funds", fund_name, float(0))
	year_dict = helper_aggregate(year_dict, anti_type_money, "departments", dep_name, float(0))
	return year_dict
