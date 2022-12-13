import os
import sys
from bs4 import BeautifulSoup
import json
import re

def convert(filePath):
    header = '<html><head>\n \
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">\n \
 b   <title>{title} | Log for {year}-{month}-{day} starting at {hour}:{mins}</title>\n \
    <style>body {{ background-color: #101535; font-family: Courier New,Courier,monospace; font-weight: bold; }} h1{{ text-align: center; color: #FFFFFF; }} .memolog {{ text-align: left; background-color: #FFFFFF; border: 5px solid #3F4472; height: 500px; width: 48%; padding: 5px; margin-left: auto; overflow: scroll; margin-right: auto; float: center; }} .participants {{ text-align: left; background-color: #FFFFFF; border: 5px solid #3F4472; height: 500px; width: 22%; padding: 5px; margin-left: auto; overflow: scroll; margin-right: auto; float: right; white-space: nowrap }} .memolist {{ text-align: left; background-color: #FFFFFF; border: 5px solid #3F4472; height: 500px; width: 22%; padding: 5px; margin-left: auto; overflow: scroll; margin-right: auto; white-space: nowrap; float: left; }}</style>\n \
    <meta charset="UTF-8">\n \
    </head>\n \
    <body cz-shortcut-listen="true">\n \
    <h1>{title} | Log for {year}-{month}-{day} starting at {hour}:{mins}</h1>\n \
    <div class="memolist">\n \
    MEMOS\n \
    </div>\n'
    with open(filePath, "r") as unformattedLog:
        formattedLog = "<!-- Original Filepath: " + filePath.split("Pesterchum-logs")[1] + "-->"
        unformattedLogContents = unformattedLog.read()
        logName = os.path.basename(filePath)
        logInfo = {
            "mins": logName.split(".")[3],
            "hour": logName.split(".")[2],
            "day": logName.split(".")[1].split("-")[2],
            "month": logName.split(".")[1].split("-")[1],
            "year": logName.split(".")[1].split("-")[0],
            "title": logName.split(".")[0],
        }
        logHeader = header.format(**logInfo)
        formattedLog = formattedLog + "\n" + logHeader
        userInfo = []
        unformattedLogParser = BeautifulSoup(unformattedLogContents, 'html.parser')
        messageSpans = unformattedLogParser.find_all("span")
        for span in messageSpans:
            spanText = span.get_text()
            if len(spanText) > 3:
                if spanText[3] == ":":
                    chum = {
                            "chum": spanText[1:3],
                            "color": span["style"],
                            "tense": spanText[0],
                        }
                    if chum not in userInfo:
                        userInfo.append(chum)
        participantsDiv = '<div class="participants">'
        for user in userInfo:
            userSpan = '<span style=' + user["color"] + ">"
            searchString = "\[" + user["tense"] + user["chum"] + "\]"
            searchResult = unformattedLogParser.find(string=re.compile(searchString))
            if searchResult != None:
                userSpan = userSpan + searchResult.get_text() + "</span></br>"
            else:
                userSpan = userSpan + user["tense"] + " ?????? [" + user["tense"] + user["chum"] + "]</span></br>"
            participantsDiv = participantsDiv + userSpan
        participantsDiv = participantsDiv + "</div>"
        formattedLog = formattedLog + "\n" + participantsDiv
        formattedLog = formattedLog + "\n<div class=memolog>\n" + unformattedLogContents
        formattedLog = formattedLog + "\n</div>\n</body>\n</html>"
        formattedLogDirectory = filePath.split("Pesterchum-logs")[0] + "Pesterchum-logs\\PrettifiedAndSortedByDate\\" + logInfo["year"] + "-" + logInfo["month"] + "-" + logInfo["day"] + "\\"
        os.makedirs(formattedLogDirectory)
        formattedLogFilename = formattedLogDirectory + os.path.basename(filePath)
        with open(formattedLogFilename, "w") as output:
            output.write(formattedLog)
        # print(json.dumps(logHeader, sort_keys=True, indent=4))
        # print(json.dumps(userInfo, sort_keys=True, indent=4))



if __name__ == "__main__":
    convert(sys.argv[1])