# SIX Automated Presence - Flask Server
Modified version of [SIX Automated Presence](https://github.com/mkamadeus/SIX-Automated-Presence)

Thank you [Matthew Kevin (MK)](https://github.com/mkamadeus/) for doing all the heavy lifting

## Prerequisites
- [Python 3.6+](https://www.python.org/downloads/)
- [geckodriver for Firefox](https://github.com/mozilla/geckodriver/releases)


## Setup
Please follow [Original SIX Automated Presence](https://github.com/mkamadeus/SIX-Automated-Presence) setup first, then continue below

1. Setup Prerequisites
- Install python and geckodriver
- [Put geckodriver on PATH](https://www.softwaretestinghelp.com/geckodriver-selenium-tutorial/)

2. Install Python Module Requirements
```bash
python -m pip install -r requirements.txt
```

3. Start server
```bash
python app.py
```

4. Do POST request to `http://localhost:5000/`
Header:
```
{
  "Content-Type": "application/json",
}
```
Payload:
```
{
	"credentials": {
		"username": "anak_imba",
		"password": "anak_imba123",
		"nim": "13520000"
	},
	"line_token": "A_VERY_SECRET_TOKEN_YOU_SHOULDVE_NOT_SHARE_TO_ME"
}
```

5. Wait for driver to complete(approx 30 seconds)
Response (JSON):
```
{
	"code": "4",
	"classname": "Fisika A",
	"message": "Presence form filled successfully"
}
```

### Other Info
- `nim` is optional
- `line_token` is optional, will send line notif in case of timeout (or success too)
- default `PORT` is 5000

### Tips
Create windows start service to [run server in background](https://stackoverflow.com/questions/32808730/running-python-script-as-a-windows-background-process):
- [NSSM](https://nssm.cc/)
- or just run on other computer/server like [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python)/[Firebase](https://medium.com/firebase-developers/hosting-flask-servers-on-firebase-from-scratch-c97cfb204579)

Use auto scheduler:
- [Google Apps Script](https://www.quora.com/How-can-I-periodically-run-a-Google-Script-on-a-Spreadsheet) -> I tried this, but should set manual and cannot set exact time to run
- [Windows Task Scheduler](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10)
