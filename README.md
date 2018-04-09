# Xerox
## This is a simple Invoice Reader and Parser

Maintaining invoices is a tedious and error-prone task. So this tool can be used to parse and analyse invoices.This Piece of application takes care of maintaining the invoices.  
This parser is written in python. It will parse your invoice and store details such as Invoice Number, Invoice Date, Due date, Total amount into MySQL Database.  
As this project is still in current development, lots of features are going to be added soon.

## Dependencies
1. Tools:
    * Python 2.7 
    * Tessaract OCR Version 3.05.01
    * MySQL
    
2. Python Libraries:
    * PyMySQL
    * pytesseract
    * send2trash
    * pillow
    * PyYAML
    * fuzzywuzzy
    
### How To Run:
1. Run Extract.py using ```python Extract.py``` in command line. 
    * This command will extract text from images(jpeg,jpg and png are currently supported) and store that text in txt folder.
2. Run find_and_parse.py using ```python find_and_parse.py``` in command line.
    * This command parses the text from text files and stores the result in MySQL database.

## Future Plans for the project
1. As This application is in current development, certain features are being added from time to time.
2. Future plans includes features such as: 
    * Parsing sender and receiver details
    * Introduce Machine Learning 
    * Support for ElasticSearch.
    * Analytics
    
## Bugs and Fixes:
As Application is in current development, code enhancement and changes is currently going on. Bugs fixes is in ongoing state. The Application is stable as tested in Local Machine. Please Read Instructions before use.

## Contact
Original Author: Sarthak Vashisth  
Email: sarthakvashisth@outlook.com  
Blog: https://twikkie.wordpress.com