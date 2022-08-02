## Server for synchronization of Google SpreadSheets and PostgreSQL




## How to start?
* Usage Python 3.9

* Edit the config located here:
ConfigManager/config.py


* Add Apps Script:

In Google sheets open "Extensions > Apps Script"

```
function sendMessage(e, text){
  const range = e.range;
  const token = "TOKEN-VK";
  const peer_id = "2000000001";

  try{
    UrlFetchApp.fetch('https://api.vk.com/method/messages.send?peer_id=' + peer_id + '&message=' + text + '&random_id=0&&v=5.131&access_token=' + token);
  }catch(e){
      range.setNote('[EditEvent] Error in requests: ' + e);
  }

}


function atEdit(e) {
  var range = e.range;
  sendMessage(e, 'Changed value: ' + range.getA1Notation());
}
```

We also need to open the triggers tab on the left and add our atEdit Select event type function: When editing

* Add two bots to one conversation
1 - Bot from google spreadsheets
2 - bot our server

* start main.py!
----

## How to package in docker?


Download and install DockerDesktop
Go to the project folder

#### run:

```docker build . -t app:latest
docker run app:latest
```


----

### requirements
```vk_api
requests~=2.28.1
psycopg2~=2.9.3
google-api-python-client~=1.7.11
httplib2~=0.20.4
oauth2client~=4.1.3
```
