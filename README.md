To start the application you will need to create a virtual environment with this code on terminal


python -m venv venv


You will need to download all the library's in the code, for this you will need to run in terminal this code


pip install -r requirements.txt


After this only run the archive named "main.py" and will show the calculator!



If you want a .exe or a .app packet you can install the library pyinstaller using the code:

pip install pyinstaller

To turn into a packet you will use this code for windows:

pyinstaller --name='Archivename' --noconfirm --noconsole --onefile --add-data='files/;files' --icon='icon directory' --log-level=WARN 'main.py'

For macOS:

pyinstaller --name='Archivename' --noconfirm --noconsole --onefile --add-data='files/:files' --icon='icon directory' --log-level=WARN 'main.py'

(in data the directory will change the ; to :.)
