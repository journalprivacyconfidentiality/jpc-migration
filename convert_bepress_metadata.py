#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 17 11:40:28 2017

@author: vilhuber
"""

# csv2xml.py
# FB - 201010107
# First row of the csv file must be header!

# example CSV file: myData.csv
# id,code name,value
# 36,abc,7.6
# 40,def,3.6
# 9,ghi,6.3
# 76,def,99

import csv
import re
import os
import urllib.parse as p
import html

csvFile = 'JPC metadata.csv'
xmlbaseFile = 'metadata.xml'

csvData = csv.reader(open(csvFile))
csvDict = csv.DictReader(open(csvFile))

#%%
def quote(arg):
    # preserve <p> in text
    #myarg = re.sub(r'<p>','PPPP',arg)
    # now replace all
    #myarg = p.quote(myarg,safe=' ()')
    myarg = html.escape(arg,quote=True)
    #myarg = re.sub(r';',p.quote(";"),myarg)
    # return the <p> to the text
    #myarg = re.sub(r'PPPP','<p>',myarg)
    return myarg

#%%
def nquote(arg):
    """
    Dummy function to more easily replace text below
    """
    return arg
    
#%%
for row in csvDict:
    # we write to a specific directory
    path = re.sub(r'http://repository.cmu.edu/','',row['front_end_url'])
    xmlFile = "JPC_archive/" + path + "/" + xmlbaseFile
    xmlData = open(xmlFile, 'w')
    # now to write out the document
    xmlData.write('<documents><document>\n')
    xmlData.write('<title>' + nquote(row['title']) + '</title>\n')
    print("Processing " + row['title'] + "(" + path + ")")
    if row['publication_date_alt']:
        xmlData.write('<publication-date>' + row['publication_date_alt'] + '</publication-date>\n')
    elif row['publication_date']:
        xmlData.write('<publication-date>' + row['publication_date'] + '</publication-date>\n')
    elif row['embargo_date']:
        xmlData.write('<publication-date>' + row['embargo_date'] + '</publication-date>\n')
    xmlData.write('<state>published</state>\n')
    xmlData.write('<authors>\n')
    # we replace the 'and' with ',', then split by ','
    authors = re.sub(r' and',r',',row['authors'])
    authors = re.sub(r',,',r',',authors)
    authors = re.sub(r'Dr',r'',authors)
    authors = re.sub(r'Mr',r'',authors)
    authors = re.sub(r'Mrs',r'',authors)
    if not authors:
        authors = "Anonymous"
    #print("Debug: " + row['authors'] + "-->" + authors)
    for author in authors.split(", "):
        print("   Processing " + author)
        xmlData.write('<author>\n')
        xmlData.write('<email></email>\n')
        xmlData.write('<institution></institution>\n')
        if len(author.split(' ')) == 1:
            first = ""
            last = author.split(' ')[0]
            middle = ""
        elif len(author.split(' ')) == 2:
            first = author.split(' ')[0]
            last = author.split(' ')[1]
            middle = ""
        elif len(author.split(' ')) == 3:
            first = author.split(' ')[0]
            last = author.split(' ')[2]
            middle = author.split(' ')[1]
        # spanish?
        elif len(author.split(' ')) == 4:
            first = author.split(' ')[0]
            last = author.split(' ')[2] + " " + author.split(' ')[3]
            middle = author.split(' ')[1]
        else:
            first = ""
            last = author
            middle = ""
            print("DEBUG:" + author + " has more than 4 elements")
        xmlData.write('<lname>' + nquote(last) +  '</lname>\n')
        xmlData.write('<fname>' + nquote(first) + '</fname>\n')
        xmlData.write('<mname>' + nquote(middle) +  '</mname>\n')
        xmlData.write('</author>\n')
    xmlData.write('</authors>\n')
    if row['abstract']:
        xmlData.write('<abstract>' + quote(row['abstract']) + '</abstract>\n')
    xmlData.write('<keywords>\n')
    for keyword in row['keywords'].split(","):
        xmlData.write('<keyword>' + nquote(keyword) + '</keyword>\n')
    xmlData.write('</keywords>\n')
    xmlData.write('<coverpage-url>' + row['front_end_url'] + '</coverpage-url>\n')
    xmlData.write('<fulltext-url>' + row['download_url'] + '</fulltext-url>\n')
    xmlData.write('<label>1</label>\n')
    xmlData.write('<document-type>articles</document-type>\n')
    xmlData.write('<type>articles</type>\n')
    xmlData.write('<articleid>' + row['context_key'] + '</articleid>\n')
    xmlData.write('<submission-date></submission-date>\n')
    xmlData.write('<native-url>' + row['download_url'] + '</native-url>\n')
    xmlData.write('<publication-title>Journal of Privacy and Confidentiality</publication-title>\n')
    xmlData.write('<context-key>' + row['context_key'] + '</context-key>\n')
# some extra fields
    xmlData.write('<fields>\n')
    if row['embargo_date']:
        xmlData.write('<field name="embargo_date" type="date"><value>' + row['embargo_date'] + '</value></field>\n')
    xmlData.write('<field name="peer_reviewed" type="boolean"><value>' + row['peer_reviewed'] + '</value></field>\n')
    #xmlData.write('<field name="distribution_license" type="string">    <value>© 2018 by the authors</value></field>\n')
    xmlData.write('</fields>\n')
    xmlData.write('</document>' + "\n")
    xmlData.write('</documents>' + "\n")
    xmlData.close()
