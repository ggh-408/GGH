import threading
import time
import tkinter as tk

from revChatGPT.V1 import Chatbot


def running_operation():
    global root, gpt, user, thread_done
    text = user.get("1.0", "end-1c")
    gpt.delete("1.0", "end")
    user.delete("1.0", "end")
    prev_text = ""
    for data in chatbot.ask(text):
        message = data["message"][len(prev_text):]
        gpt.insert("end", message)
        prev_text = data["message"]
    with open(log, mode='a') as file:
        file.write("User:" + text)
        file.write("ChatGPT:" + gpt.get("1.0", "end-1c") + "\n")
    thread_done = True


def get_answer(event):
    global focus, thread_done
    if focus and thread_done:
        thread_done = False
        thread = threading.Thread(target=running_operation)
        thread.start()


def handle_focus(event):
    global focus
    if event.widget == user:
        focus = True
    elif event.widget == gpt:
        focus = False


def on_close():
    global root
    root.destroy()
    with open(log, mode='a') as file:
        file.write(time.strftime("%Y-%m-%d %H:%M", time.localtime()))


if __name__ == '__main__':
    with open("/Users/ggh/Desktop/python/ChatGPT/access_token.txt", mode="r") as f:
        access_token = f.read()
    chatbot = Chatbot(config={
        "access_token": access_token,
        "paid": False,
    })

    font = "宋体 13"
    focus, thread_done = True, True
    log = "/Users/ggh/Desktop/python/ChatGPT/log/" + time.strftime("%Y-%m-%d_%H-%M", time.localtime()) + ".txt"
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.geometry('%dx%d+%d+%d' % (300, 450, (root.winfo_screenwidth() - 300), 0))
    root.title("ChatGPT")
    gpt = tk.Text(root, font=font)
    gpt.pack(fill=tk.BOTH, expand=True)
    user = tk.Text(root, font=font)
    user.pack(fill=tk.BOTH, expand=True)
    root.bind("<Command-Return>", get_answer)
    root.protocol("WM_DELETE_WINDOW", on_close)
    root.bind("<FocusIn>", handle_focus)
    root.mainloop()
