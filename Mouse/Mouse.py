import threading
import time
import tkinter as tk

import pyautogui


# 定义一个事件处理程序，用于在用户手动输入文本后将其居中对齐
def center_text(*args):
    if MainWindow.Point_dic[MainWindow.Focus].get("1.0", "end")[:-1].isdigit():
        MainWindow.Point_dic[MainWindow.Focus].tag_remove("center", "1.0", "end")
        MainWindow.Point_dic[MainWindow.Focus].tag_add("center", "1.0", "end")
        MainWindow.Point_dic[MainWindow.Focus].tag_configure("center", justify='center')
    else:
        MainWindow.Point_dic[MainWindow.Focus].delete("end-2c")


def handle_focus(event):
    for dic_pair in MainWindow.Point_dic.items():
        if dic_pair[1] == event.widget:
            MainWindow.Focus = dic_pair[0]
            break


def sign_data(*args):
    for number in range(MainWindow.Point):
        if not MainWindow.Point_dic[(number + 1, 1)].get("1.0", "end")[:-1] and \
                not MainWindow.Point_dic[(number + 1, 2)].get("1.0", "end")[:-1]:
            MainWindow.Point_dic[(number + 1, 1)].insert("1.0", pyautogui.position().x)
            MainWindow.Point_dic[(number + 1, 1)].tag_add("center", "1.0", "end")
            MainWindow.Point_dic[(number + 1, 1)].tag_configure("center", justify='center')

            MainWindow.Point_dic[(number + 1, 2)].insert("1.0", pyautogui.position().y)
            MainWindow.Point_dic[(number + 1, 2)].tag_add("center", "1.0", "end")
            MainWindow.Point_dic[(number + 1, 2)].tag_configure("center", justify='center')

            MainWindow.Point_dic[(number + 1, 3)].insert("end", "0")
            MainWindow.Point_dic[(number + 1, 3)].tag_add("center", "1.0", "end")
            MainWindow.Point_dic[(number + 1, 3)].tag_configure("center", justify='center')
            break


def delete_data(*args):
    for number in range(MainWindow.Point, 0, -1):
        if MainWindow.Point_dic[(number, 1)].get("1.0", "end")[:-1] or \
                MainWindow.Point_dic[(number, 2)].get("1.0", "end")[:-1]:
            MainWindow.Point_dic[(number, 1)].delete("1.0", "end")
            MainWindow.Point_dic[(number, 2)].delete("1.0", "end")
            break


def clear_data(*args):
    for number in range(MainWindow.Point):
        MainWindow.Point_dic[(number + 1, 1)].delete("1.0", "end")
        MainWindow.Point_dic[(number + 1, 2)].delete("1.0", "end")
        MainWindow.Point_dic[(number + 1, 3)].delete("1.0", "end")


def destroy_data(*args):
    if MainWindow.Point >= 2:
        for i in range(5):
            MainWindow.Point_dic[(MainWindow.Point, i)].destroy()
        MainWindow.Variable.pop(-1)
        MainWindow.Point -= 1


class MainWindow(tk.Tk):
    Point = 0
    Width = 440
    Height = 225
    Point_dic = {}
    Focus = (0, 0)
    Variable = []
    Thread_done = True
    Font = "宋体 22"

    def __init__(self):
        super().__init__()
        self.geometry('%dx%d+%d+%d' % (MainWindow.Width, MainWindow.Height,
                                       (self.winfo_screenwidth() - MainWindow.Width),
                                       0))
        self.title("Mouse")
        self.resizable(False, True)
        self.position_X = tk.Label(text='', font=MainWindow.Font)
        self.position_Y = tk.Label(text='', font=MainWindow.Font)
        self.position_X.grid(row=0, column=1)
        self.position_Y.grid(row=0, column=2)
        for _ in range(5):
            self.add_data()

        MainWindow.Point_dic[(0, 0)] = tk.Text(width=6, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(0, 0)].grid(row=0, column=5)
        MainWindow.Point_dic[(0, 0)].insert("end", "1")
        MainWindow.Point_dic[MainWindow.Focus].tag_add("center", "1.0", "end")
        MainWindow.Point_dic[MainWindow.Focus].tag_configure("center", justify='center')
        tk.Label(text="延时", font=MainWindow.Font).grid(row=0, column=3)
        tk.Button(text="开始", command=self.start, width=4, font=MainWindow.Font).grid(row=1, column=5)
        tk.Button(text="删除", command=delete_data, width=4, font=MainWindow.Font).grid(row=2, column=5)
        tk.Button(text="清空", command=clear_data, width=4, font=MainWindow.Font).grid(row=3, column=5)
        tk.Button(text="添加", command=self.add_data, width=4, font=MainWindow.Font).grid(row=4, column=5)
        tk.Button(text="销毁", command=destroy_data, width=4, font=MainWindow.Font).grid(row=5, column=5)

        self.refresh_data()
        self.bind("<KeyRelease>", center_text)
        self.bind("<FocusIn>", handle_focus)
        self.bind('<Command-Key-s>', sign_data)
        self.bind('<Command-Key-S>', sign_data)
        self.bind('<Command-Key-1>', self.start)
        self.bind('<Command-Key-2>', delete_data)
        self.bind('<Command-Key-3>', clear_data)
        self.bind('<Command-Key-4>', self.add_data)
        self.bind('<Command-Key-5>', destroy_data)

        self.mainloop()

    def add_data(self):
        MainWindow.Point += 1
        MainWindow.Point_dic[(MainWindow.Point, 0)] = tk.Label(text=MainWindow.Point, width=1, font=MainWindow.Font)
        MainWindow.Point_dic[(MainWindow.Point, 0)].grid(row=MainWindow.Point, column=0)
        MainWindow.Point_dic[(MainWindow.Point, 1)] = tk.Text(width=8, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(MainWindow.Point, 1)].grid(row=MainWindow.Point, column=1)
        MainWindow.Point_dic[(MainWindow.Point, 2)] = tk.Text(width=8, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(MainWindow.Point, 2)].grid(row=MainWindow.Point, column=2)
        MainWindow.Point_dic[(MainWindow.Point, 3)] = tk.Text(width=6, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(MainWindow.Point, 3)].grid(row=MainWindow.Point, column=3)
        MainWindow.Variable.append(tk.StringVar(self))
        MainWindow.Variable[-1].set("左键")
        MainWindow.Point_dic[(MainWindow.Point, 4)] = tk.OptionMenu(self, MainWindow.Variable[-1], "左键", "右键", "移动")
        MainWindow.Point_dic[(MainWindow.Point, 4)].grid(row=MainWindow.Point, column=4)

    def refresh_data(self):
        self.position_X.config(text='X=' + str(pyautogui.position().x))
        self.position_Y.config(text='Y=' + str(pyautogui.position().y))
        # 递归循环调用after
        self.after(100, self.refresh_data)

    def running_operation(self):
        self.iconify()
        # 循环次数
        cycle = int(MainWindow.Point_dic[(0, 0)].get("1.0", "end")[:-1])
        valid_rows = MainWindow.Point
        position_list, delay_list, option_list = [], [], []

        for number in range(MainWindow.Point):
            position_x = MainWindow.Point_dic[(number + 1, 1)].get("1.0", "end")[:-1]
            position_y = MainWindow.Point_dic[(number + 1, 2)].get("1.0", "end")[:-1]
            delay = MainWindow.Point_dic[(number + 1, 3)].get("1.0", "end")[:-1]
            if not position_x or not position_y:
                valid_rows = number
                break
            position_list.append((float(position_x), float(position_y)))
            if delay:
                delay_list.append(float(delay))
            else:
                delay_list.append(0.0)
            option_list.append(MainWindow.Variable[number].get())

        for _ in range(cycle):
            for number in range(valid_rows):
                if option_list[number] == "左键":
                    pyautogui.click(position_list[number])
                elif option_list[number] == "右键":
                    pyautogui.rightClick(position_list[number])
                elif option_list[number] == "移动":
                    pyautogui.moveTo(position_list[number])
                time.sleep(delay_list[number])
        MainWindow.Thread_done = True

    def start(self, *args):
        if MainWindow.Thread_done:
            MainWindow.Thread_done = False
            thread = threading.Thread(target=self.running_operation)
            thread.start()


if __name__ == '__main__':
    MainWindow()
