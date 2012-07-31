This is a python script I made for Appboy that pulls information from Crunch Base using their API and scrapes it to find companies of a specific type (in this case its mobile app startups). From there it goes back into the API to find more information on the company, like their phone number, email address, and company type. The information is then converted into a CSV file located in the data folder. The file's name depends on the search terms and the time the code was executed

Programming Language: Python

APIs Used: CrunchBase API

Important Sections
==========================================

Terms
-------

`term_list = ["mobile","app", "startup"]`

List of search terms. You can add or remove any number of terms and the script will return different results and will have a new filename


File Name
-------------

`
date = strftime("%d %b %Y %H:%M:%S", gmtime())
filename ="data/DATA" # file located in data folder
for i in term_list:
    filename+= i
filename+= date #File name depends on search terms and the current time
info_file = open(filename + '.csv', 'w')
`
Each file will be generated in a data folder and will start with the word 'DATA'. Next, python iterates through the array and adds each search term to the file name. Finally the date is appended to the end. Python then creates the file by 'opening' it as a .csv file with write permissions ('w'). If you would like to change the filename to just be 'results', for example, you could just remove this code and insert:
`
info_file = open('results.csv', 'w')
`

Pages
-------------

The CrunchBase API returns 10 results per page.
`
def get_info(p = 1)
`
This line means that the function get_info() will take 1 optional parameter: 'p' which stands for 'pages'. The default value is 1.
`
max_range = p + 1 # I added 1 because in range function the max value is not counted
    for i in range (1, max_range):
        page = str(i)
        search_url = 'http://api.crunchbase.com/v/1/search.js?query=' + query + '&page=' + page
`
In this section, the script goes through a loop and each time gets the next page, returning 10 new results. Thus, get_info(5) tells the script to search 5 pages each with 10 results, returning 50 companies.


Obtaining The Company's Info
-------------------------------

The main search through CrunchBase only provides a small amount of information, so I had to do another lookup for their detailed info

`
max_range = p + 1 # I added 1 because in range function the max value is not counted
for i in range (0, 10):
            permalink = json_response['results'][i]["permalink"]
            namespace = json_response['results'][i]["namespace"] 
            company_url="http://api.crunchbase.com/v/1/" + namespace + "/" + permalink + ".js"
            company_response = urllib2.urlopen(company_url)
            json_company_info = simplejson.load(company_response)
`
The for loop goes from results 0 to 10 (because each page has 10 results). It should probably only go from 0 to 9 so I will fix that later (because 0-10 gives 11 results). The company's url is then constructed using their namespace, like 'company' or 'individual', and their permalink. CrunchBase then serves up a JSON file with all the necessary information



Catching Errors
-----------------

`
try:
...
except
                category = ""
...
except
                description = "none"
except KeyError:
                homepage="none"
...
except KeyError:
                email_address = "none"
...
except:
                phone_number = ""
`
Not every company provides all their information so this section tests to see if they have an email address or homepage etc and provides a value if it is missing
