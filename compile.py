from os import system

files =  [
    "src/main.py",
]

files_list = ""
for file in files:
    files_list += " " + file

system("pip install pyinstaller")
system("pyinstaller" + files_list + " --name pbrain-gomoku-ai.exe --onefile")
system('copy .\\dist\\pbrain-gomoku-ai.exe .')