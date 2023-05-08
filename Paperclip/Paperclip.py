import os
import time
import threading
import pyperclip


def running_operation():
    global copy
    if pyperclip.paste() != copy:
        copy = pyperclip.paste()
        with open("/Users/ggh/Desktop/python/pyperclip/Paperclip.txt", "a+") as f:
            f.write(copy + "\n")


def get_answer():
    thread = threading.Thread(target=running_operation)
    # 启动线程
    thread.start()


if __name__ == '__main__':
    copy = str()
    if os.path.exists("/Users/ggh/Desktop/python/pyperclip/Paperclip.txt"):
        os.remove("/Users/ggh/Desktop/python/pyperclip/Paperclip.txt")
    while copy != ":wq":
        time.sleep(1)
        get_answer()
