import urllib2
import urllib
import json
from time import gmtime, strftime
import simplejson
import sys

term_list = ["mobile","app", "startup"] #Add or change this list and url will update

header = "Company name, Category, Description, Homepage, Email Address, Phone #,"

date = strftime("%d %b %Y %H:%M:%S", gmtime())
filename ="data/DATA" # located in data folder
for i in term_list:
    filename+= i
filename+= date
info_file = open(filename + '.csv', 'w')

def get_info(p = 1):
    global term_list
    global header
    global writer
    global info_file
    info_file.write(header + "\n ")
    query = "" #maybe just chnage it to be unicoded instead of this for loop
    last = len(term_list) - 1
    for i in term_list:
        if i == term_list[last]:
            query += i
        else:
            query += i + "%20"
    max_range = p + 1 # I added 1 because in range function the max value is not counted
    for i in range (1, max_range):
        page = str(i)
        search_url = 'http://api.crunchbase.com/v/1/search.js?query=' + query + '&page=' + page
        print search_url
        search_response = urllib2.urlopen(search_url)
        json_response = simplejson.load(search_response)
        for i in range (0, 10):
            permalink = json_response['results'][i]["permalink"]
            namespace = json_response['results'][i]["namespace"] 
            company_url="http://api.crunchbase.com/v/1/" + namespace + "/" + permalink + ".js"
            company_response = urllib2.urlopen(company_url)
            json_company_info = simplejson.load(company_response)
            if namespace == "person":
                first_name = json_company_info["first_name"]
                last_name = json_company_info["last_name"]
                company_name = first_name + " " + last_name
            else:
                company_name = json_company_info["name"]
            try:
                category = json_company_info["category_code"]
            except:
                category = ""
            try:
                description = json_company_info["description"]
            except:
                description = "none"
            try:
                homepage =json_company_info["homepage_url"]
            except KeyError:
                homepage="none"
            try:
                email_address = json_company_info["email_address"]
            except KeyError:
                email_address = "none"
            try:
                phone_number = json_company_info["phone_number"]
            except:
                phone_number = ""
            total_info = company_name.replace(",","") + "," + str(category) + "," + str(description).replace(",","") + "," + str(homepage) + "," + str(email_address) + "," + str(phone_number) + ","
            info_file.write(total_info + "\n")
    info_file.close()
