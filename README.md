Run the command below from the main folder in order to run the application on Linux:
```bash
cd project_files/ && python main.py
```
For building the apk package for android run the command below in the terminal:
```bash
buildozer -v android debug:
```
To sign app:
```bash
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore your_keystore.keystore your_app_nameg.apk your_alias_name
```