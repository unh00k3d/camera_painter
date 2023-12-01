# This is a project i am doing while i am learning about computer vision and deep learning

### this project works by first calibrating your pens with the program to detect it...

## Quick Start

### clone the repository
```
git clone https://github.com/unh00k3d/camera_painter.git
```

### run the setup script to install all requirement and activate a virtual enviroment

#### macos / linux
```
cd camera_painter
python3 setup.py
```

#### windows
```
cd camera_painter
python setup.py
```
### and you should be set to go

##

### you can run the script using 
```
streamlit run interface.py
```
### which will open a webserver and start the program on the webpage

### note that you may want to change the value in interface.py to match you expectencies


###

## adjusting values and testing

### you can test which color ranges will work for you pen by using the other script provided

```
python/3 adjustable_color_detector.py
```

### will let you run color detection for both images and videos
### though you might want to go the file and un/comment code to switch between both



### i will be updating this file whenever i do something new