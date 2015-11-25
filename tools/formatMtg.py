#!/usr/bin/env python

from AdvancedHTMLParser import *

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
    
    TABLE_FORMAT="""
<div class="maindeck">
  <table class="cardgroup" cellpadding="10">
    <tbody>
      <tr>
        <td valign="top" width="40%">
          <b>
            <i class="decltotals">%(LEFT_SIDE_TITLEs)</i>
          </b>
          <hr size="1" width="50%" align="left" class="decltotals"/>
          %(LEFT_SIDE_ENTRIES)s
          <br/>
        </td>
        <td valign="top" width="40%">
          <b>
            <i class="decltotals">%(RIGHT_SIDE_TITLE)s</i>
          </b>
          <hr size="1" width="50%" align="left" class="decltotals"/>
          %(RIGHT_SIDE_ENTRIES)s
          <br/>
        </td>
        <td valign="top" width="185">
          <br/>
        </td>
      </tr>
    </tbody>
  </table>
  <br/>
</div>
"""
    
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
    
    
    
# BEGIN MAIN CODE
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

def getListForAppend(title, colors):
    lands = "Land" in title
    spells = "Other" in title
    creatures = "Creatures" in title
    
    if colors is not None:
        (isHybrid, isMulti, isMono, isColorless) = analyzeColors(colors)
        if isHybrid:
            print "HYBRID", colors
            if lands:
                print "WTF!"
                return None
            elif spells:
                return HYBRID_SPELLS
            elif creatures:
                return HYBRID_CREATURES
        elif isMulti:
            print "MULTI", colors
            if lands:
                print "WTF!"
                return None
            elif spells:
                return MULTI_SPELLS
            elif creatures:
                return MULTI_CREATURES
        elif isMono:
            print "MONO", colors
            if lands:
                print "WTF!"
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
            print "COLORLESS", colors
            if lands:
                print "WTF!"
                return None
            elif spells:
                return COLORLESS_SPELLS
            elif creatures:
                return COLORLESS_CREATURES
    else:
        # No color data, must be land?            
        if isItemBasicLand(item):
            print "BASIC LAND"
            return LAND_BASIC
        else:
            print "NON-BASIC LAND"
            return LAND_NONBASIC
            
            
# Print the output without the surrounding table and a top level image tag to be loaded with the right card

for (title, items) in titlesToEntries.iteritems():
    print "********************************"
    print title
    for item in items:
        cardName = getCardName(item)
        if cardName is not None:
            print "---------------------------"
            print cardName
        else:
            # No card name, not really a card!
            continue
            
        # Add to the correct list.
        getListForAppend(title, getColors(item)).append(item)

print """<img src="" id="card_pic" style="max-height: 223px; max-width: 310px; text-align: center; vertical-align: middle;" alt=""/><br/>"""        

GREEN_LEFT_ENTRY = ""
for item in GREEN_CREATURES:
    for entry in item:
        try:
            GREEN_LEFT_ENTRY += entry.getHTML() + '\n'
        except AttributeError:
            GREEN_LEFT_ENTRY += entry + '\n'

GREEN_RIGHT_ENTRY = ""
for item in GREEN_SPELLS:
    for entry in item:
        try:
            GREEN_RIGHT_ENTRY += entry.getHTML() + '\n'
        except AttributeError:
            GREEN_RIGHT_ENTRY += entry + '\n'

print MtgConsts.TABLE_FORMAT.format({'LEFT_SIDE_TITLE':'Green Creatures (%d)'%(len(GREEN_CREATURES)),
                                     'LEFT_SIDE_ENTRIES':GREEN_LEFT_ENTRY,
                                     'RIGHT_SIDE_TITLE':'Green Spells (%d)'%(len(GREEN_SPELLS)),
                                     'RIGHT_SIDE_ENTRIES':GREEN_RIGHT_ENTRY})

print BLACK_CREATURES

print BLACK_SPELLS

print BLUE_CREATURES

print BLUE_SPELLS

print WHITE_CREATURES

print WHITE_SPELLS

print RED_CREATURES

print RED_SPELLS

print MULTI_CREATURES

print MULTI_SPELLS

print HYBRID_CREATURES

print HYBRID_SPELLS

print COLORLESS_CREATURES

print COLORLESS_SPELLS

print LAND_BASIC

print LAND_NONBASIC
