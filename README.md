# convert-bible
## Description
A python script to create a single html file of the Afrikaans Bible from http://www.bybel.co.za

The idea is to create one big html page that contains the full bible text with index and chapter links. This html page can then be used as input for an application like [Calibre](http://calibre-ebook.com/) to convert it to an ebook format.

## Requirements
You need to run the script with Python 3.
The original script was written for Python 2, but Python 3 natively uses UTF-8 encoding which made the code much cleaner because you don't have to encode strings throughout the code.

## How to use the script
The script takes the output file name as a command line argument
For example:
```lisp
converter.py /my/path/bible.html
```


