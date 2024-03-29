# clip-translator
In the DeepL apps available for window and mac, you can easily translate with ctrl-c ctrl-c. I would like to get something similar on linux.  
![clip-translator](https://user-images.githubusercontent.com/39142679/85319755-f695eb80-b4fc-11ea-86a7-d5ab394b6818.gif)

## Install
Please check your google chrome version.  
```
google-chrome --version
Google Chrome 81.0.4044.113
```
Install the closest version of chromedriver_binary.
```
pip install chromedriver_binary==81.0.4044.138.0
```
To check the available version
```
pip install chromedriver_binary==
```

Install this package
```
git clone https://github.com/kosuke55/clip-translator.git  
cd clip-translator  
pip install -e .  
```

## Setting
Set keyboard shortcut by running script.  
```
python set_keyboard_shortcut.py 'clip-translate' 'clip_translate_c' '<Primary><Alt>c'
```

(or manually...)  
Search for "keyboard" and start it up, then select "shortcuts" and "custom shortcuts" field.  
<img src="https://user-images.githubusercontent.com/39142679/85297416-aeb39c00-b4dd-11ea-8cce-74452bb11eb9.png" width="500">  
Press the + button to add a shortcut as shown in the following image.  
<img src="https://user-images.githubusercontent.com/39142679/85297176-66947980-b4dd-11ea-8350-b298da51c8c2.png" width="500">  
<img src="https://user-images.githubusercontent.com/39142679/85297169-64cab600-b4dd-11ea-82c7-e4749ce30069.png" width="500">  

If you want to use the server's desktop shortcut, 

```
python create_desktop_shortcut.py
```

## Run

click desktop shortcut and then the browser starts up.  
<img src="https://camo.qiitausercontent.com/794807e27e694f32f3b6439f6146431592d02b47/68747470733a2f2f71696974612d696d6167652d73746f72652e73332e61702d6e6f727468656173742d312e616d617a6f6e6177732e636f6d2f302f3331353233322f31333132336634652d306361312d663035362d663839312d6336653337336436363266662e706e67" width="100">  
or in the terminal  

```
clip_translate_s
```

If you cannot launch with the shortcut, right-click the icon and select "Allow Launch".

After launching browser you can translate the text by pressing the shortcut key (ctrl-alt-c) after copying (ctrl-c).  

### Options

```
clip_translate_s -h
usage: clip_translate_s [-h] [--source SOURCE] [--target TARGET] [--mode MODE]
                        [--split SPLIT] [--remove-hyphen REMOVE_HYPHEN]
                        [--remove-newline REMOVE_NEWLINE]

optional arguments:
  -h, --help            show this help message and exit
  --source SOURCE, -s SOURCE
                        source language (default: en)
  --target TARGET, -t TARGET
                        target language (default: ja)
  --mode MODE, -m MODE  Translation site (deepl or google) (default: deepl)
  --split SPLIT, -sp SPLIT
                        Use wordninja split (default: 0)
  --remove-hyphen REMOVE_HYPHEN, -rh REMOVE_HYPHEN
                        Remove hypen (default: 0)
  --remove-newline REMOVE_NEWLINE, -rn REMOVE_NEWLINE
                        Remove newline (default: 0)
```

To use google translate instead of deepl, run like
```
clip_translate_s -m google
```

## Trouble Shooting
- Can't translate with the shortcut.
If it was started with the command `clip_translate_s`, the following error is displayed.
```
socket.error: [Errno 98] Address already in use
```
This is not visible when launched from the desktop icon.
You can kill the process on the port being used by running
```
kill_clip_trasnlate_s
```

- Can't launch an application from its icon.
Launch from command line and check the error.
```
~
$ clip_translate_s
source: en
target: ja
mode: deepl
split: 0
remove_hyphen: 2
Traceback (most recent call last):
  File "/home/kosuke55/.local/bin/clip_translate_s", line 33, in <module>
    sys.exit(load_entry_point('clip-translator', 'console_scripts', 'clip_translate_s')())
  File "/home/kosuke55/clip-translator/clip_translator/translate.py", line 162, in run_server
    translator = Translator(args.source, args.target,
  File "/home/kosuke55/clip-translator/clip_translator/translate.py", line 48, in __init__
    self.driver = webdriver.Chrome(options=options)
  File "/usr/local/lib/python3.8/dist-packages/selenium/webdriver/chrome/webdriver.py", line 76, in __init__
    RemoteWebDriver.__init__(
  File "/usr/local/lib/python3.8/dist-packages/selenium/webdriver/remote/webdriver.py", line 157, in __init__
    self.start_session(capabilities, browser_profile)
  File "/usr/local/lib/python3.8/dist-packages/selenium/webdriver/remote/webdriver.py", line 252, in start_session
    response = self.execute(Command.NEW_SESSION, parameters)
  File "/usr/local/lib/python3.8/dist-packages/selenium/webdriver/remote/webdriver.py", line 321, in execute
    self.error_handler.check_response(response)
  File "/usr/local/lib/python3.8/dist-packages/selenium/webdriver/remote/errorhandler.py", line 242, in check_response
    raise exception_class(message, screen, stacktrace)
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: This version of ChromeDriver only supports Chrome version 92
Current browser version is 94.0.4606.71 with binary path /usr/bin/google-chrome
```

If the version of google chrome is not correct, install chromedriver_binaray again.
```
# check version list
$ pip install chromedriver_binary==
# Install the closest version of chromedriver_binary
$ pip install chromedriver_binary==94.0.4606.61.0
```
