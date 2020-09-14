
# SIX Automated Presence - Flask Server
Modified version of [SIX Automated Presence](https://github.com/mkamadeus/SIX-Automated-Presence)
Thank you [Matthew Kevin (MK)](https://github.com/mkamadeus/) for doing all the heavy lifting

## Prerequisites
- Python
- selenium
- flask

## Setup
1. Install Requirements
```bash
python -m pip install -r requirements.txt
```
2. Start server
```bash
python app.py
```
3. POST
```
/POST http://localhost:5000/
{
	"credentials": {
		"username": "anak_imba",
		"password": "anak_imba123",
		"nim": "13520000"
	}
}
```
Response:
```
{
	"code": "4",
	"classname": "Fisika A",
	"message": "Presence form filled successfully"
}
```

### Other Info
nim is optional
default PORT is 5000


### Tips
Create windows start service to [run server in background](https://stackoverflow.com/questions/32808730/running-python-script-as-a-windows-background-process):
- [NSSM](https://nssm.cc/)
- or just run on other computer/server like [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)/[Firebase](https://medium.com/firebase-developers/hosting-flask-servers-on-firebase-from-scratch-c97cfb204579)

Use auto scheduler:
- [Google Apps Script](https://www.quora.com/How-can-I-periodically-run-a-Google-Script-on-a-Spreadsheet)  
- [Windows Task Scheduler](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10)
