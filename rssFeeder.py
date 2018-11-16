#!/usr/bin/python3

from email.utils import formatdate
import getopt
import sys

url         = ""
link        = ""
title       = ""
description = ""
output      = ""
createBlank = False
createItem  = False
isPermaLink = False
time        = formatdate()


# Show this scripts options and usage examples.
#   This can be evoked by using -h, --help or having no parameters at all.
def usage():
    print("RSS FeedMe - An easy way to add new items to your RSS feed!")
    print()
    print("Blank RSS Document: ")
    print("  rssFeeder.py -b -u http://expl.com/rss.xml -t \"Website Title\" -l http://expl.com -d \"Website Description\" -o path/to/rss.xml")
    print("     -b --blank Creates a blank rss document with the defined variables")
    print("     -u --url URL to the rss document")
    print("     -t --title Website title")
    print("     -l --link URL to the website")
    print("     -d --description Short website description")
    print("     -o --output Where to write the .xml document")
    print()
    print("New RSS Item: ")
    print("  rssFeeder.py -i -t \"Item Title\" -l http://expl.com/item -d \"Item Description\" -o path/to/rss.xml [-p]")
    print("     -i --item Create a new RSS item")
    print("     -t --title Item title")
    print("     -l --link URL to the item/article")
    print("     -d --description Short item/article description")
    print("     -o --output Where to write the .xml document")
    print("     -p --perma (Optional) Defines if this is a PermaLink. Default is false and uses timestamp. If true (-p is set) the link will be used.")
    print()


# Checks whether the script is satisfied with the given options.
#   Will return an error and exit the script if it's not satisfied.
#   If everything checks out, the main() function will continue to
#   write to the rss file.
def isOptionsSet():
    global url
    global link
    global title
    global description
    global output
    global createItem

    val = "Item/Article"
    uVal = "/item"
    if not createItem:
        uVal = ""
        val = "Website"

    if not createBlank and not createItem:
        assert False, "Use -b for blank RSS document, and -i for new item."
    if title == "":
        assert False, "Define the " + val + " Title with -t \"Example Title\""
    if link == "":
        assert False, "Define the " + val + " URL with -u http://example.com" + uVal
    if description == "":
        assert False, "Define the " + val + " Description with -d \"" + val + " Description\""
    if output == "":
        assert False, "Define the Path where to write the RSS document with -o ./rss.xml (i.e)"
    if createBlank and url == "":
        assert False, "Define the URL to the RSS document with -u http://example.com/rss.xml (i.e)"


# Write to the rss document.
#   This will be run when everything has checked out.
#   This will handle both creating blank rss documents
#   and creating new items to an existing rss document.
def writeRss():
    global url
    global link
    global title
    global description
    global output
    global createItem

    combined = []

    # Create a new blank RSS document
    if not createItem:
        rssFile = open(output, 'w')
        for line in getDefaultRssDoc():
            rssFile.write(line)
        print("New RSS document written to " + output)


    # Create item
    else:
        rssFile = open(output, 'r')
        rLines  = rssFile.readlines()


        for i, line in enumerate(rLines):
            combined.append(line)

            # Insert the new item at line 8
            if i != 7:
                continue

            # Add item lines to the 'combined' array
            for iLine in getRssItem():
                combined.append(iLine)

        # ** Kinda silly,
        # The file is already opened,
        # for lines to be read into an array,
        # so we have to close that instance,
        # so that we can open it again with the write parameter.
        rssFile.close()
        rssFile = open(output, 'w')
        # ***/

        for c in combined:
            rssFile.write(c)
        print("Added new item to " + output)

    rssFile.close()


# Get the default RSS document content
#   Returns an array of lines
#   Requires: -u -t -l -d
def getDefaultRssDoc():
    rss = """
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
        <channel>
          <atom:link href="""+ url +""" rel="self" type="application/rss+xml" />
          <title>"""+ title +"""</title>
          <link>"""+ link +"""</link>
          <description>"""+ description +"""</description>

        </channel>
    </rss>"""

    rss = rss.split('\r\n')
    return rss


# Get the default RSS item content
#   Returns an array of lines
#   Requires: -t -l -d
#   Optional: -p
def getRssItem():
    global time
    global isPermaLink

    #time = str(time)

    permaLink  = link
    permaState = 'true'
    if not isPermaLink:
        permaLink  = time[:-6]
        permaState = 'false'

    item = """
    <item>
        <title>"""+ title +"""</title>
        <link>"""+ link +"""</link>
        <description>"""+ description +"""</description>
        <guid isPermaLink="""+ permaState +""">"""+ permaLink +"""</guid>
        <pubDate>"""+ time +"""</pubDate>
    </item>"""

    item = item.split('\r\n')
    return item


# Will be run when the script is invoked
#   Will loop through the options and get/set the values.
#   Then invoke the function to either create new RSS document,
#   or insert a new item to the existing RSS document.
def main():
    global url
    global link
    global title
    global description
    global output
    global isPermaLink
    global createBlank
    global createItem

    if not len(sys.argv[1:]):
        usage();
        return

    try:
        opts, args = getopt.getopt(sys.argv[1:], "biu:t:l:d:p:o:", ["blank", "item", "url=", "title=", "link=", "description=", "perma=", "output="])
    except getopt.GetoptError as eRR:
        print(str(eRR))
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()

        if o in ("-u", "--url"):
            url = a
        if o in ("-t", "--title"):
            title = a
        if o in ("-l", "--link"):
            link = a
        if o in ("-d", "--description"):
            description = a
        if o in ("-o", "--output"):
            output = a
        if o in ("-p", "--perma"):
            isPermaLink = True

        if o in ("-b", "--blank"):
            createBlank = True
        if o in ("-i", "--item"):
            createItem = True

    try:
        isOptionsSet()
    except AssertionError as err:
        print(str(err))
        sys.exit()

    writeRss()

main()