#!/usr/bin/env python

from AdvancedHTMLParser import *

class MtgConsts:
    RED='R'
    BLUE='U'
    HYBRID='/'
    BLACK='B'
    GREEN='G'
    WHITE='W'

    FOREST='Forest'
    PLAINS='Plains'
    SWAMP='Swamp'
    MOUNTAIN='Mountain'
    ISLAND='Island'
    
def getColors(item):
    returnList = None

    for entry in item:
        try:
            if "img" == entry.tagName:
                if returnList is None:
                    returnList = []
                    
                altAttr = entry.getAttribute("alt")
                if MtgConsts.GREEN in altAttr and MtgConsts.GREEN not in returnList:
                    returnList.append(MtgConsts.GREEN)
                if MtgConsts.BLUE in altAttr and MtgConsts.BLUE not in returnList:
                    returnList.append(MtgConsts.BLUE)
                if MtgConsts.BLACK in altAttr and MtgConsts.BLACK not in returnList:
                    returnList.append(MtgConsts.BLACK)
                if MtgConsts.WHITE in altAttr and MtgConsts.WHITE not in returnList:
                    returnList.append(MtgConsts.WHITE)
                if MtgConsts.RED in altAttr and MtgConsts.RED not in returnList:
                    returnList.append(MtgConsts.RED)
                if MtgConsts.HYBRID in altAttr and MtgConsts.HYBRID not in returnList:
                    returnList.append(MtgConsts.HYBRID)
        except AttributeError:
            # Not an element, skip.
            continue
            
    return returnList

def isItemBasicLand(item):
    for entry in item:
        try:
            if "a" == entry.tagName:
                linkText = entry.innerHTML
                
                if (MtgConsts.ISLAND in linkText or
                MtgConsts.SWAMP in linkText or
                MtgConsts.MOUNTAIN in linkText or
                MtgConsts.PLAINS in linkText or
                MtgConsts.FOREST in linkText):
                    return True
        except AttributeError:
            # Not an element, skip.
            continue
    return False
    
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
        colors = getColors(item)
        if colors is not None:
            print colors
        else:
            print "Colorless"
            
        if isItemBasicLand(item):
            print "BASIC LAND"
            
