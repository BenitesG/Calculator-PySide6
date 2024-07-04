To a better experience with the application, use a virtual environment.

You will need to download all the library's in the code, for this you will need to run in terminal this command:

pip install -r requirements.txt


After this only run the archive named "main.py" and will show the calculator!



If you want a .exe or a .app packet you can install the library pyinstaller using the command:

pip install pyinstaller

To turn into a packet you will use this command for windows:

pyinstaller --name='Archivename' --noconfirm --noconsole --onefile --add-data='files/;files' --icon='icon directory' --log-level=WARN 'main.py'

For macOS:

pyinstaller --name='Archivename' --noconfirm --noconsole --onefile --add-data='files/:files' --icon='icon directory' --log-level=WARN 'main.py'

(in data the directory will change the ; to :.)
