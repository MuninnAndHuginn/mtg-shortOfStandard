#!/usr/bin/env python

from AdvancedHTMLParser import *

parser = AdvancedHTMLParser("test.html")

maindeck = parser.getElementsByClassName("maindeck")[0]

columns = maindeck.getChildren().getElementsByTagName("td")

titlesToEntries = {}

for c in columns:
    curTitle = None
    curList = None
    for entry in c.getChildren():
        # check for b tag, it should contain the title.
        if "b" == entry.tagName:
            # grab the i tag text.
            curTitle = entry.getChildren().getElementsByTagName("i")[0].text

            # insert into map if not there.
            if not curTitle in titlesToEntries.keys():
                titlesToEntries[curTitle] = []
            
            curList = titlesToEntries[curTitle]
        elif "hr" == entry.tagName or "br" == entry.tagName:
            curList.append([entry])
        elif "a" == entry.tagName:
            entryList = []
            # Grab the quantity, stripped
            entryList.append(entry.previousSibling.strip())
            # Grab the link tag with the card name
            entryList.append(entry)

            # loop and grab the next sibling images until we earch a break
            nextSibling = entry.nextSiblingElement
            while not nextSibling.tagName == "br":
                if "img" == nextSibling.tagName:
                    entryList.append(nextSibling)
                nextSibling = nextSibling.nextSiblingElement

            # add the items as an entry.
            curList.append(entryList)
            

#TODO: Write a function that can tell you the colors of an item based on its tag entries.
#TODO: Create tags for each color Spells and Creatures.
#TODO: Sort the items into spells/creatures per color (G, B, U, W, R, Mutli, Hybrid)
#TODO: Create table format that makes sense for display of each color.
#TODO: Print a series of tables for display of each color

# Print the output without the surrounding table and a top level image tag to be loaded with the right card
print """<img src="" id="card_pic" style="max-height: 223px; max-width: 310px; text-align: center; vertical-align: middle;" alt=""/><br/>"""
for (title, items) in titlesToEntries.iteritems():
    print title
    for item in items:
        for entry in item:
            print entry

