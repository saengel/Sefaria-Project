import pdfkit
import requests
import json

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


def loop_through_book(ref, text):
    name = ref + ".html"

    while ref:
        url = 'http://www.sefaria.org/api/texts/'+ref
        params = dict(
            commentary=0,
            context=0
            )

        resp = requests.get(url=url, params=params)

        data = json.loads(resp.text)
        print("Now retrieving " + data["sectionRef"] + " and adding to pdf")

        en = data["text"]
        he = data["he"]

        # Make an <h2> data["sectionRef"] to be the Chapter title
        text = text + "<h2 style='text-align:center; font-size:30px;'>" +\
            data["sectionRef"] + "</h2><hr><br> <table style=\"width:100%\">"

        # For each pasuk, add the verse
        for i in range(0, len(he)):

            # Hebrew and English Text - i+1 is the verse
            num = str(i+1)
            text = text +\
                "<tr><th></th><th> ." + num + ". </th><th></th>" +\
                "<tr><th> <p style='text-align: right; direction: rtl; font-size:20px;'>"+\
                 he[i]+ "</th>" +\
                "<th></th><th><p style='text-align: left;'>"+\
                en[i] + "</p></th></tr><tr><th> </th><th> </th><th> </th></tr>"

        text = text + "</table><br>"

        if data["next"]:
            ref = data["next"]
        else:
            ref = None

    # Appending the Sefaria API image
    text = text + "<div style='text-align:center'>"+\
        "<img src='http://www.sefaria.org/static/img/samekh.png' height=100>"+\
        "<div>Made with the Sefaria API</div></div></body></html>"
        
    return text









# code that runs

print("Buy your own book!")
print("Name of book: "),
var = raw_input()

if var in validBook:
    print("Now pdf'ing " + var)

    bookRefList = [var]

    for book in bookRefList:

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
            "<i>Powered by the Sefaria API</i></div>"

    	wholeBookText = loop_through_book(book, a_text)
        #print(wholeBookText)
        pdfkit.from_string(wholeBookText, "pdf_samples/" +var+'.pdf', options=pdf_options)

    print("Your PDF is ready")

else:
    print("Not a valid book choice. Please try again.")
