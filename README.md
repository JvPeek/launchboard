# This is launchboard
A cute little python tool that lets you use your Novation Launchpad S as a keyboard, a soundboard, a smart home controller and many more (soon-ish)

## Installation

### Prerequisites
You'll need to have python and pip running on your machine. Venv helps but is not needed.

### Windows
```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```
### Linux
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Sometimes alsa complains about a file not found. This helped in my case (Manjaro):
```bash
sudo ln -s /usr/share/alsa/alsa.conf /usr/local/share/alsa/alsa.conf
```
### MacOS
Should be similar to Linux. Haven't tested it since my Mac has no USB port to plug the damn thing into. Good luck and let me know how it went.

## Configuration
This software is split into two parts. The GUI and the backend. Changes to the configuration are made inside the GUI tool. The backend tool is meant to be run while using the program. This is the first time i wrote anything to be used with a mouse. Be nice!

### The GUI
To open the config GUI run
```bash
cd src
python gui.py
```
If everything is installed correctly, a window should appear.

By default the launchpad is divided into eight pages. To switch to a certain page, the "page" action for the button must be enabled.

To configure the actions for a button, click the button on the grid and enable the actions.

Save your config with the "save config" button (or ctrl+s)

### The backend
To actually use the bloody thing run
```bash
cd src
python main.py
```
Your Launchpad, if connected correctly, should greet you with a short text and then display your first page. Hitting a button should execute the appropriate actions.

