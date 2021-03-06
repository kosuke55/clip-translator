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
In the terminal  

```
clip_translatate_s
```

or click desktop shortcut and then the browser starts up.  

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
clip_translatate_s -m google
```

## Trouble Shooting
If you can't translate with the shortcut.
If it was started with the command `clip_translate_s`, the following error is displayed.
```
socket.error: [Errno 98] Address already in use
```
This is not visible when launched from the desktop icon.
You can kill the process on the port being used by running
```
kill_clip_trasnlate_s
```
