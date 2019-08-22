# Import statements
import pdfkit
import requests
import json

# Import and set-up of pretty PrettyPrinter
# for debugging the json
import pprint
pp = pprint.PrettyPrinter(indent=4)

# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# PDF option variables set for the pdfkit
# module
pdf_options = {
    'page-size': 'Letter',
    'margin-top': '0.5in',
    'margin-right': '0.75in',
    'margin-bottom': '0.5in',
    'margin-left': '0.75in',
    'encoding': "UTF-8",
    }

# Limit the user (for now) only to the books of Tanach
validBook = ["Genesis", "Bereshit", "Shemot", "Exodus", "Vayikra", "Leviticus"
             "Bamidbar", "Numbers", "Devarim", "Deuteronomy", "Yehoshua",
             "Joshua", "Shoftim", "Judges", "Shmuel Aleph", "Shmuel I",
             "I Samuel", "Samuel I", "Shmuel Bet", "Shmuel II", "Samuel II",
             "II Samuel", "Melachim Aleph", "Melachim I", "Kings I", "I Kings",
             "Melachim Bet", "Melachim II", "Kings II", "II Kings", "Isaiah",
             "Jeremiah", "Yeshayahu", "Ezekiel", "Yermiyahu", "Yechezkel",
             "Hoshea", "Hosea", "Joel", "Yoel", "Amos", "Ovadiah", "Obadiah",
             "Yonah", "Jonah", "Micha", "Micah", "Nahum", "Nachum", "Habakkuk",
             "Chabakkuk", "Zephaniah", "Tzephaniah", "Chaggai", "Haggai",
             "Zechariah", "Malachi", "Psalms", "Tehilim", "Proverbs", "Mishlei",
             "Iyov", "Job", "Shir haShirim", "Song of Songs", "Rut", "Ruth",
             "Eicha", "Lamentations", "Kohelet", "Ecclesiastes", "Esther",
             "Daniel", "Ezra", "Nehemiah", "Nechemiah",
             ]


# This function takes a chapter reference, as well as
# string called "text". It uses the reference to make
# an API call for the chapter's text and commentary
# and then appends it to text using HTML tags. The "text"
# string is ultimately rendered from html to pdf.
def loop_through_book(ref, text):

    # Name of the html file
    name = ref + ".html"

    # As long as the ref is valid, make the following series
    # of API calls and append Hebrew and English texts to the
    # "text" string
    while ref:

        # API call for the chapter
        text_url = 'http://www.sefaria.org/api/texts/'+ref
        params = dict(
            commentary=0,
            context=0
            )
        resp = requests.get(url=text_url, params=params)

        # Loading the response into a JSON dictionary
        text_data = json.loads(resp.text)

        # Print statement to the console for the user
        print("Now retrieving " + text_data["sectionRef"] + " and adding to pdf")

        # Saving Hebrew and English text
        en = text_data["text"]
        he = text_data["he"]

        # Appending and styling a chapter title
        text = text + "<h2 style='text-align:center; font-size:30px;'>" +\
            text_data["sectionRef"] + "</h2><hr><br> <table style=\"width:100%\">"


        # API call for the commentary
        com_url = 'http://www.sefaria.org/api/links/'+ref
        params = dict(
            with_text=1
            )
        resp = requests.get(url=com_url, params=params)

        # Loading the response into a JSON dictionary
        com_data = json.loads(resp.text)

        # list of commentary dictionaries
        rashi_dict = {}

        # Filtering out all of the links by Rashi
        # adding just the Rashi links to a new rashi_dict
        for each in com_data:
            title = each["collectiveTitle"]
            if title["en"] == "Rashi":
                anchorRef = each["ref"]
                rashi_dict[anchorRef] = each

        # Print statement to the console for the user
        print("Now retrieving " + text_data["sectionRef"] + " commentaries and adding to pdf")

        # Iterates through the resulting list of pesukim
        # in the chapter
        for i in range(0, len(he)):

            he_com = " "
            en_com = " "


            for each in rashi_dict:
                if rashi_dict[each]["anchorVerse"] == (i+1):

                    if rashi_dict[each]["he"]:
                        he_com += str(rashi_dict[each]["he"]) + "<br><br>"

                    if rashi_dict[each]["text"]:
                        en_com += str(rashi_dict[each]["text"]) + "<br><br>"

            print("Uploading Rashi on Pasuk: " + str(i+1))
            # Create and append verse number
            num = str(i+1)

            # Append with HTML tags to text
            # uses a table to style Hebrew and English across
            # from each other.
            text = text +\
                "<tr><th></th><th> ." + num + ". </th><th></th>" +\
                "<tr><th> <p style='text-align: right; direction: rtl; font-size:20px;'>"+\
                 he[i]+ "</th>" +\
                "<th></th><th><p style='text-align: left;'>"+\
                en[i] + "</p></th></tr><tr><th> </th><th> </th><th> </th></tr>"+\
                "<tr><th> <p style='text-align: right; direction: rtl; font-size:10px;'><i>" +\
                he_com + "</i></p></th><th></th><th><p style='text-align: left;font-size:10px;'><i>" +\
                en_com + "</i></p></th></tr>"

        # Append the end of the table
        text = text + "</table><br>"

        # If there's another chapter, assign ref to that next chapter
        # and repeat the while loop
        if text_data["next"]:
            ref = text_data["next"]

        # Else, if we reached the end of the book, set ref to None
        # and break out of the while loop
        else:
            ref = None

    # Appending the end of the HTML tags
    text = text + "</body></html>"

    # Return the text string, full of HTML tags and text,
    # ready to be rendered into a pdf below...
    return text

# CODE THAT INVOKES THE METHOD

# Prompt for the user
print("Buy your own book!")
print("Name of book: "),
var = raw_input()

# TODO: Load the possible commentaries given the book selected
# prompt the user to select one of those commentaries
# Pass that commentary as a third parameter for the function above
# determining the API call

# If the variable is a valid book of Tanach
if var in validBook:

    # Tell the user beginning to work
    print("Now pdf'ing " + var)

    # Setting the header for the HTML from_string
    # this variable will be passed through the function,
    # and the text resulting from the API call will be appended
    # to this document
    # Hypothetically, the pdfkit CSS would be put here as well
    # but when tested, due to issues with wkhtmltopdf, it never
    # really worked.
    a_text = """
    	<!DOCTYPE html>
    	<html>
    	<head>
    	<meta charset="utf-8">
    	</head>
        <style>
            h1, h2, h3, h4, h5 {
                page-break-after: avoid;
                page-break-before: always;
            }

            @page:right{
                @bottom-left {
                    margin: 10pt 0 30pt 0;
                    border-top: .25pt solid #666;
                    content: """+ var + """";
                    font-size: 9pt;
                    color: #333;
                }
            }

        </style>
    	<body>
    	<h1 style='text-align:center; font-size:60px;'><hr><br>
    	""" +  var + "</h1><br><hr><br> <div style='text-align:center; font-size:15px;'>" +\
        "<i>Powered by the Sefaria API</i></div><div style='text-align:center'>"+\
        "<img src='http://www.sefaria.org/static/img/samekh.png' height=400></div>"

    # Calling the function on the book
    # returns a String with HTML tags
    wholeBookText = loop_through_book(var, a_text)

    # Takes the resulting HTML string and turns it into a PDF in
    # the Sefaria-Project/pdf_samples directory.
    pdfkit.from_string(wholeBookText, "pdf_samples/" +var+'.pdf', options=pdf_options)

    # Prints a response to the user
    print("Your PDF is ready")

# Not a valid book choice
else:
    print("Not a valid book choice. Please try again.")
