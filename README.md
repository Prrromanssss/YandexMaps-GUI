# YandexMaps-GUI

![flake8 test](https://github.com/Prrromanssss/YandexMaps-GUI/actions/workflows/python-package.yml/badge.svg)

![Image of the app](https://github.com/Prrromanssss/YandexMaps-GUI/raw/main/media-for-README/main-image.png)

## About

This project presents work with the Yandex Maps API implemented using a graphical interface


## Deployment instructions


### 1. Cloning project from GitHub

1.1 Run this command
```commandline
git clone https://github.com/Prrromanssss/YandexMaps-GUI
```

### 2. Creation and activation venv

2.1 First of all, from root directory run this command
```commandline
python -m venv venv
```
2.2 Then run this command to activate venv
#### Mac OS / Linux
```commandline
source venv/bin/activate
```
#### Windows
```commandline
.\venv\Scripts\activate
```

### 3. Installation all requirements

3.3 Run this command 
```commandline
pip install -r requirements.txt
```
### 4. Generate file with virtual environment variables (.env)

4.1 Generate file '.env' in root directory with such structure
```text
APIKEY=YOUR-API-KEY-TO-MAPS
GEOCODE_APIKEY=YOUR-GEOCODE-API-KEY-TO-MAPS
```

### 5. Running project

5.1 Run this command
```commandline
python main.py
```

***