import os
import sys
def convert(filePath):
    header = '<html><head>\n \
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">\n \
    <title>{title} | Log for {year}-{month}-{day} starting at {hour}:{mins}</title>\n \
    <style>body {{ background-color: #101535; font-family: Courier New,Courier,monospace; font-weight: bold; }} h1{{ text-align: center; color: #FFFFFF; }} .memolog {{ text-align: left; background-color: #FFFFFF; border: 5px solid #3F4472; height: 500px; width: 48%; padding: 5px; margin-left: auto; overflow: scroll; margin-right: auto; float: center; }} .participants {{ text-align: left; background-color: #FFFFFF; border: 5px solid #3F4472; height: 500px; width: 22%; padding: 5px; margin-left: auto; overflow: scroll; margin-right: auto; float: right; white-space: nowrap }} .memolist {{ text-align: left; background-color: #FFFFFF; border: 5px solid #3F4472; height: 500px; width: 22%; padding: 5px; margin-left: auto; overflow: scroll; margin-right: auto; white-space: nowrap; float: left; }}</style>\n \
    <meta charset="UTF-8">\n \
    </head>\n \
    <body cz-shortcut-listen="true">\n \
    <h1>{title} | Log for {year}-{month}-{day} starting at {hour}:{mins}</h1>\n \
    <div class="memolist">\n \
    MEMOS\n \
    </div>\n'
    with open(filePath, "r") as unformattedLog:
        logName = os.path.basename(filePath)
        logInfo = {
            "mins": logName.split(".")[3],
            "hour": logName.split(".")[2],
            "day": logName.split(".")[1].split("-")[2],
            "month": logName.split(".")[1].split("-")[1],
            "year": logName.split(".")[1].split("-")[0],
            "title": logName.split(".")[0]
        }
        logHeader = header.format(**logInfo)
        print(logHeader)
if __name__ == "__main__":
    convert(sys.argv[1])