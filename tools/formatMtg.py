#!/usr/bin/env python

from AdvancedHTMLParser import *
import re
import sys

BAD_IMAGES_RE = r'src="file:.*/Sets'
GOOD_IMAGES_PREFIX = r'src="images/Sets' 

# Define containers for each table column
GREEN_CREATURES = []
GREEN_SPELLS = []

BLACK_CREATURES = []
BLACK_SPELLS = []

BLUE_CREATURES = []
BLUE_SPELLS = []

WHITE_CREATURES = []
WHITE_SPELLS = []

RED_CREATURES = []
RED_SPELLS = []

MULTI_CREATURES = []
MULTI_SPELLS = []

HYBRID_CREATURES = []
HYBRID_SPELLS = []

COLORLESS_CREATURES = []
COLORLESS_SPELLS = []

LAND_BASIC = []
LAND_NONBASIC = []

# Define some constants to reference (matches input HTML code...)
class MtgConsts:
    RED='R'
    BLUE='U'
    HYBRID='/'
    BLACK='B'
    GREEN='G'
    WHITE='W'
    COLORLESS='0'

    FOREST='Forest'
    PLAINS='Plains'
    SWAMP='Swamp'
    MOUNTAIN='Mountain'
    ISLAND='Island'
    
    TABLE_FORMAT="""\
<div class="maindeck">
<table class="cardgroup" cellpadding="10">
<tbody>
<tr>
<td valign="top" width="40%">
<b>
<i class="decltotals">{LEFT_SIDE_TITLE}</i>
</b>
<hr size="1" width="50%" align="left" class="decltotals"/>
{LEFT_SIDE_ENTRIES}
<br/>
</td>
<td valign="top" width="40%">
<b>
<i class="decltotals">{RIGHT_SIDE_TITLE}</i>
</b>
<hr size="1" width="50%" align="left" class="decltotals"/>
{RIGHT_SIDE_ENTRIES}
<br/>
</td>
<td valign="top" width="185">
<img src="" id="card_pic" style="max-height: 223px; max-width: 310px; text-align: center; vertical-align: middle;" alt=""/><br/>
<br/>
</td>
</tr>
</tbody>
</table>
<br/>
</div>\
"""
    
def getColors(item):
    returnList = None

    for entry in item:
        try:
            if "img" == entry.tagName:
                altAttr = entry.getAttribute("alt")
                if altAttr is None:
                    # Skip this (it's probably the set image)
                    continue
                
                # Safe to init return list
                if returnList is None:
                    returnList = []
                
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
                #Check for Colorless mana entries.
                if (MtgConsts.COLORLESS in altAttr.replace("0", MtgConsts.COLORLESS).replace("1", MtgConsts.COLORLESS).replace("2", MtgConsts.COLORLESS).replace("3", MtgConsts.COLORLESS).replace("4", MtgConsts.COLORLESS).replace("5", MtgConsts.COLORLESS).replace("6", MtgConsts.COLORLESS).replace("7", MtgConsts.COLORLESS).replace("8", MtgConsts.COLORLESS).replace("9", MtgConsts.COLORLESS).replace("X", MtgConsts.COLORLESS)
                and MtgConsts.COLORLESS not in returnList):
                    returnList.append(MtgConsts.COLORLESS)
                    
        except AttributeError:
            # Not an element, skip.
            continue
            
    return returnList
    
def analyzeColors(colors):
    myColors = list(colors)
    
    isHybrid = False
    if MtgConsts.HYBRID in myColors:
      isHybrid = True
      myColors.remove(MtgConsts.HYBRID)
    
    isColorless = False
    hasColorless = False
    isMono = False
    isMulti = False
    
    if MtgConsts.COLORLESS in myColors:
        hasColorless = True
        myColors.remove(MtgConsts.COLORLESS)
    
    # Only have colors left 0, 1, or More
    if len(myColors) > 1:
      isMulti = True
    elif len(myColors) == 1:
      isMono = True
    
    # Note if we had colorless and not mono or multi
    if not isMulti and not isMono and hasColorless:
        isColorless = True
    
    return (isHybrid, isMulti, isMono, isColorless)

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
    
def getCardName(item):
    for entry in item:
        try:
            if "a" == entry.tagName:
                return entry.innerHTML
        except AttributeError:
            # Not an element, skip.
            continue
    return None
    
def generateTable(leftTitle, leftItems, rightTitle, rightItems):
    if not leftItems and not rightItems:
        return None

    LEFT_ENTRY = ""
    for item in leftItems:
        for entry in item:
            LEFT_ENTRY += str(entry) + '\n'
            
    RIGHT_ENTRY = ""
    for item in rightItems:
        for entry in item:
            RIGHT_ENTRY += str(entry) + '\n'
            
    format_dict = {"LEFT_SIDE_TITLE":leftTitle + " (%d)"%(len(leftItems)),
                   "LEFT_SIDE_ENTRIES":LEFT_ENTRY,
                   "RIGHT_SIDE_TITLE":rightTitle + " (%d)"%(len(rightItems)),
                   "RIGHT_SIDE_ENTRIES":RIGHT_ENTRY}
    # Now is a good time to replace that bad images path for the sets with the correct one
    return re.sub(BAD_IMAGES_RE, GOOD_IMAGES_PREFIX, MtgConsts.TABLE_FORMAT.format(**format_dict))
    
def printSplitTables():
    green = generateTable("Green Creatures", GREEN_CREATURES, "Green Spells", GREEN_SPELLS)
    black = generateTable("Black Creatures", BLACK_CREATURES, "Black Spells", BLACK_SPELLS)
    blue = generateTable("Blue Creatures", BLUE_CREATURES, "Blue Spells", BLUE_SPELLS)
    red = generateTable("Red Creatures", RED_CREATURES, "Red Spells", RED_SPELLS)
    white = generateTable("White Creatures", WHITE_CREATURES, "White Spells", WHITE_SPELLS)
    multi = generateTable("Multi-Colored Creatures", MULTI_CREATURES, "Multi-Colored Spells", MULTI_SPELLS)
    hybrid = generateTable("Hybrid Creatures", HYBRID_CREATURES, "Hybrid Spells", HYBRID_SPELLS)
    colorless = generateTable("Colorless Creatures", COLORLESS_CREATURES, "Colorless Spells", COLORLESS_SPELLS)
    land = generateTable("Basic Land", LAND_BASIC, "Non-Basic Land", LAND_NONBASIC)

    if colorless:
        print colorless
    if black:
        print black
    if blue:
        print blue
    if green:
        print green
    if red:
        print red
    if white:
        print white
    if hybrid:
        print hybrid
    if multi:
        print multi
    if land:
        print land

def getListForAppend(title, item):
    colors = getColors(item)
    
    lands = "Land" in title
    spells = "Other" in title
    creatures = "Creatures" in title
    
    if colors is not None:
        (isHybrid, isMulti, isMono, isColorless) = analyzeColors(colors)
        if isHybrid:
            #print "HYBRID", colors
            if lands:
                #print "WTF!"
                return None
            elif spells:
                return HYBRID_SPELLS
            elif creatures:
                return HYBRID_CREATURES
        elif isMulti:
            #print "MULTI", colors
            if lands:
                #print "WTF!"
                return None
            elif spells:
                return MULTI_SPELLS
            elif creatures:
                return MULTI_CREATURES
        elif isMono:
            #print "MONO", colors
            if lands:
                #print "WTF!"
                return None
            elif spells:
                if MtgConsts.RED in colors:
                    return RED_SPELLS
                if MtgConsts.BLACK in colors:
                    return BLACK_SPELLS
                if MtgConsts.WHITE in colors:
                    return WHITE_SPELLS
                if MtgConsts.GREEN in colors:
                    return GREEN_SPELLS
                if MtgConsts.BLUE in colors:
                    return BLUE_SPELLS
            elif creatures:
                if MtgConsts.RED in colors:
                    return RED_CREATURES
                if MtgConsts.BLACK in colors:
                    return BLACK_CREATURES
                if MtgConsts.WHITE in colors:
                    return WHITE_CREATURES
                if MtgConsts.GREEN in colors:
                    return GREEN_CREATURES
                if MtgConsts.BLUE in colors:
                    return BLUE_CREATURES
        elif isColorless:
            #print "COLORLESS", colors
            if lands:
                #print "WTF!"
                return None
            elif spells:
                return COLORLESS_SPELLS
            elif creatures:
                return COLORLESS_CREATURES
    else:
        # No color data, must be land?            
        if isItemBasicLand(item):
            #print "BASIC LAND"
            return LAND_BASIC
        else:
            #print "NON-BASIC LAND"
            return LAND_NONBASIC
            
def processInputHtml(fileName):    
    # BEGIN MAIN CODE
    parser = AdvancedHTMLParser(fileName)
    
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
                
                # Grab the card set image
                setImage = entry.previousSiblingElement
                # Add the quantity, stripped
                entryList.append(setImage.previousSibling.strip())
                # Add the set Image
                entryList.append(setImage)
                # Add the link tag with the card name
                entryList.append(entry)
    
                # loop and add the next sibling images until we earch a break
                nextSibling = entry.nextSiblingElement
                while not nextSibling.tagName == "br":
                    if "img" == nextSibling.tagName:
                        entryList.append(nextSibling)
                    nextSibling = nextSibling.nextSiblingElement
                # Add the <br/> after the images
                if nextSibling.tagName == "br":
                    entryList.append(nextSibling)
                # add the items as an entry.
                curList.append(entryList)


    for (title, items) in titlesToEntries.iteritems():
        #print "********************************"
        #print title
        for item in items:
            cardName = getCardName(item)
            if cardName is None:
                # No card name, not really a card!
                continue
                
            # Add to the correct list.
            getListForAppend(title, item).append(item)

    # Send all the tables to the screen
    printSplitTables()
    
    
def main():
    processInputHtml(sys.argv[1])
    
if __name__ == "__main__":
    main()