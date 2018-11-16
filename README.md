# RSS Feed Me
A command-line RSS feeder written in Python.

&nbsp;

## Table of Content

* **[What is!?](#what-is)**
* **[How to?!](#how-to)**
* **[Examples](#examples)**
  * [Create a new RSS (.xml) document](#exp1)
    * [New RSS document result](#new-rss-document-result)
  * [Add item to RSS feed](#exp2)
    * [New items document result](#new-items-document-result)
* **[Versatility](#versatility)**
  * [Invoke from PHP](#exp3)
  * [Invoke with Cron and Bash (.sh)](#exp4)

&nbsp;

## What is!? 
This is a script that makes it easy to create new rss documents. And to add new items to that new rss document. 

Distribute your web-content, up to date, to all your passionate followers! Not sure what RSS is all about? [Read up on w3schools](https://www.w3schools.com/XML/xml_rss.asp).

**This RSS feeder script allows your to create a new rss document where you;**

* define _the URL to the rss (.xml) file,_ 
* provide a _title,_ 
* and the _URL to your site,_ 
* and a _short description of your site._

**Or you can add items to your feed (rss document) by;**

* Defining a _title for your content,_
* an _URL to your new content,_
* and a _short description of the content._

This script is command-line based, so all the values will be defined as options/parameters when invoking the script. This is to make the feeder versatile, and we are able to run it both from a command-line and from our web-code (See examples below).

&nbsp;

## How to?!
```
$ python rssFeed.py --help
RSS FeedMe - An easy way to add new items to your RSS feed!

Blank RSS Document: 
  rssFeeder.py -b -u http://expl.com/rss.xml -t "Website Title" -l http://expl.com -d "Website Description" -o path/to/rss.xml
     -b --blank Creates a blank rss document with the defined variables
     -u --url URL to the rss document
     -t --title Website title
     -l --link URL to the website
     -d --description Short website description
     -o --output Where to write the .xml document

New RSS Item: 
  rssFeeder.py -i -t "Item Title" -l http://expl.com/item -d "Item Description" -o path/to/rss.xml [-p]
     -i --item Create a new RSS item
     -t --title Item title
     -l --link URL to the item/article
     -d --description Short item/article description
     -o --output Where to write the .xml document
     -p --perma (Optional) Defines if this is a PermaLink. Default is false and uses timestamp. If true (-p is set) the link will be used.
```

&nbsp;

### Examples
#### Create a new RSS (.xml) document <a name="exp1"></a>
To create a blank, new rss document, 5 parameters is required; _URL_ (for rss), _title, link_ (for web-site), _description_ and _output_ (rss file path).

include;

* -b --blank  _For a new, BLANK rss document_
* -u --url          _URL to the RSS feed (i.e. http://example.com/rss.xml)_
* -t --title        _A fitting title for your website_
* -l --link         _The URL to your website_
* -d --description  _A fitting description for your website_
* -o --output  _The output file (the rss document)_

```
$ python3 rssFeed.py -b -u http://example.com/rss.xml -t "Website titel" -l http://example.com -d "Website Description" -o ./rss.xml 
New RSS document written to ./rss.xml
```

##### New RSS document result
The new RSS file (rss.xml) will look like this;
```
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
        <channel>
          <atom:link href=http://example.com/rss.xml rel="self" type="application/rss+xml" />
          <title>Website titel</title>
          <link>http://example.com</link>
          <description>Website Description</description>

        </channel>
    </rss>
```

If you edit this file manually, there is no gurantee the RSS will be valid after adding new items to it. 

&nbsp;

#### Add item to RSS feed  <a name="exp2"></a>
To add new content to your RSS feed, there is 3 required parameters and 1 optional; A _title_ for the content, the _URL_ for the new content and a _short description_ of the content. 

A 4th optional parameter is for the `<guid>` element. You can tell the RSS reader that this is a permanent link with the guid element. By default it is set to false and a timestamp will be set as the unique id. If you include the `-p` option, this will be treated as a perma-link and the URL for the content will be used.

Include;

* -i --item  _For a new ITEM to the feed_
* -t --title  _A good title for your new content_
* -l --link  _The URL for the new content_
* -d --description  _A short description for the content_
* -o --output _The output file (the rss document)_
* -p --perma _(OPTIONAL) If this content is permanently stored at this URL_

```
$ python ./rssFeed.py -i -t "Item Title" -l http://example.com/articlle_05 -d "Item Description" -o ./rss.xml                            
Added new item to ./rss.xml
```

##### New items document result
Here's the result of our `rss.xml` document after adding a new item;

```
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
        <channel>
          <atom:link href=http://example.com/rss.xml rel="self" type="application/rss+xml" />
          <title>Website titel</title>
          <link>http://example.com</link>
          <description>Website Description</description>

    <item>
        <title>Item Title</title>
        <link>http://example.com/articlle_05</link>
        <description>Item Description</description>
        <guid isPermaLink=false>Fri, 16 Nov 2018 03:20:20</guid>
        <pubDate>Fri, 16 Nov 2018 03:20:20 -0000</pubDate>
    </item>
        </channel>
    </rss>
```

&nbsp;

### Versatility
#### Invoke from PHP  <a name="exp3"></a>
We can easily add new web content to the RSS feed via PHP;

```php
<?php
$title = "New item title";
$link = "http://example.com/article_05";
$desc = "A short description about the new content.";
$out = "path/to/rss.xml";

$rss = exec("python path/to/rssFeed.py -i -t ".$title." -l ".$link." -d ".$desc." -o ".$out." -p");
echo $rss;
?>
```

&nbsp;

#### Invoke with Cron and Bash (.sh)  <a name="exp4"></a>
Since this is just a simple command-line script, we can also easily invoke it as a Cron job - I.e. to clean/create a new rss document each week. 

We know our site details won't change, so it is simple as creating a shell script (.sh) and invoking the rssFeed.py from there. Create a shell script (`new_rss.sh`);

```
#!/bin/bash

url="http://example.com/rss.xml"
title="A fitting web-site description"
link="http://example.com"
desc="A good, short description of your web-site"
out="path/to/rss.xml"

python path/to/rssFeed.py -b -u "$url" -t "$title" -l "$link" -d "$desc" -o "$out"
```

And then add a task to our Cron job list - I.e. every Sunday at 22:05;

```
$ crontab -e
```

And add;
```
5 22 * * 0 path/to/new_rss.sh
```
