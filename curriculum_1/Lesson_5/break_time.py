import time
import webbrowser

print("This program started on : " + time.ctime())
i = 0
for i in range(3):
    time.sleep(10)
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    i = i + 1
