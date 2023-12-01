import os
import platform



# create a virtual enviroment named painter
if platform.system() == "Windows":
    os.system("python -m venv painter")
    os.system("painter\\Scripts\\activate")
else:
    os.system("python3 -m venv painter")
    os.system("source ./painter/bin/activate")

# install requirements inside that virtual enviroment
os.system(os.path.join(os.getcwd(),"painter","bin","pip") + " install -r requirements.txt")

