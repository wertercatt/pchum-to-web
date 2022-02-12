// consts

const header = '<html><head>\n \
<meta http-equiv="content-type" content="text/html; charset=UTF-8">\n \
<title>#%TITLE% | Log for %YEAR%-%MONTH%-%DAY%</title>\n \
<link rel="stylesheet" href="https://jingloria.wertercatt.com/lostpawns/logs2/pesterlog-viewer.css">\n \
<meta charset="UTF-8">\n \
</head>\n \
<body cz-shortcut-listen="true">\n \
<h1>#%TITLE% | Log for %YEAR%-%MONTH%-%DAY%</h1>\n \
<div class="memolist">\n \
MEMOS\n \
</div>\n'


// Init File Reader
var fileReader = new FileReader();
fileReader.onload = event => {
  console.log(logName)
  formatPesterlog(event.target.result)
}

//Load file
var logName = ""
let loadFile = () => {
  var fileToLoad = document.getElementById("input").files[0]
  fileReader.readAsText(fileToLoad, "UTF-8"); 
  logName = fileToLoad.name
}

// Format HTML
let formatPesterlog = plog => {
  var outputDiv = document.getElementById("output")
  var tempformat = document.getElementById("formatter")

  // Get date and time from file name
  var fileInfo = {
    mins: logName.substring(logName.length - 6, logName.length - 4),
    hour: logName.substring(logName.length - 9, logName.length - 7),
    day: logName.substring(logName.length - 12, logName.length - 10),
    month: logName.substring(logName.length - 15, logName.length - 13),
    year: logName.substring(logName.length - 20, logName.length - 16),
    title: logName.substring(0, logName.length - 21)
  }

  // Create header
  var logHeader = header
  for (const [key, value] of Object.entries(fileInfo)) {
    logHeader = logHeader.replaceAll("%" + key.toUpperCase() + "%", value)
  }

  // Create head
  console.log(logHeader)

  // Get user list
  tempformat.innerHTML = plog
  var messageSpans = document.querySelectorAll("#formatter > span")
  var userList = []
  var userInfo = []

  // Get all Abbreviated chumhandles
  messageSpans.forEach(span => {
    if (span.innerText[3] == ":") {
      var chum = span.innerText.substring(1, 3)
      if (!userList.includes(chum)) {
        userInfo.push({
          chum: chum,
          color: span.style.color,
          tense: span.innerText[0]
        })
        userList.push(chum)
      }
    }
  })

  // Format userdivs
  var particiDiv = document.createElement("div")
  particiDiv.classList = "participants"
  userInfo.forEach(obj => {

    // Look for if full chumhandles exist
    var notiPos = tempformat.innerHTML.indexOf("[" + obj.tense + obj.chum + "]")
    if (notiPos !== -1) {
      obj.handle = tempformat.innerHTML.substring(tempformat.innerHTML.lastIndexOf(" ", notiPos - 2) + 1, notiPos - 1)
    }

    // Create userSpans
    var userSpan = document.createElement("span")
    userSpan.style.color = obj.color
    userSpan.innerText = obj.tense + " " + (obj.handle ? obj.handle : "??????") + " [" + obj.tense + obj.chum + "]"
    particiDiv.append(userSpan)
    particiDiv.append(document.createElement("br"))
  })

  console.log(userList, userInfo)

  // TODO: Replace MEMOO with memo div

  var userOuput =  particiDiv.outerHTML.replaceAll("br>", "br>\n").replaceAll('pants">', 'pants">\n')
  var output = logHeader + userOuput + " <div class=memolog>" + plog + "</div></body></html>"


  outputDiv.innerText = output

  download(fileInfo.title + fileInfo.year + "-" + fileInfo.month + "-" + fileInfo.day + ".html", output)
}


// Stolen download function

function download(filename, text) {
  var element = document.createElement('a');
  element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(text));
  element.setAttribute('download', filename);

  element.style.display = 'none';
  document.body.appendChild(element);

  element.click();

  document.body.removeChild(element);
}
