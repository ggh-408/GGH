import csv
import time
import tkinter as tk
import tkinter.filedialog
from tkinter import ttk

import pyautogui
import pyperclip


# 定义一个事件处理程序，用于在用户手动输入文本后将其居中对齐
def center_text(*args):
    MainWindow.Point_dic[MainWindow.Focus].tag_add("center", "1.0", "end")
    MainWindow.Point_dic[MainWindow.Focus].tag_configure("center", justify="center")


def handle_focus(event):
    for dic_pair in MainWindow.Point_dic.items():
        if dic_pair[1] == event.widget and dic_pair[0][1] != 7:
            MainWindow.Focus = dic_pair[0]
            break


def sign_data(*args):
    for number in range(MainWindow.Point):
        x = MainWindow.Point_dic[(number + 1, 1)].get("1.0", "end")[:-1]
        y = MainWindow.Point_dic[(number + 1, 2)].get("1.0", "end")[:-1]
        if MainWindow.Variable[number].get() != "滚动" and not x and not y:
            MainWindow.Point_dic[(number + 1, 1)].insert("1.0", pyautogui.position().x)
            MainWindow.Point_dic[(number + 1, 2)].insert("1.0", pyautogui.position().y)
            for j in range(1, 3):
                MainWindow.Point_dic[(number + 1, j)].tag_add("center", "1.0", "end")
                MainWindow.Point_dic[(number + 1, j)].tag_configure("center", justify="center")
            break


def delete_data(*args):
    for number in range(MainWindow.Point, 0, -1):
        row = [MainWindow.Point_dic[(number, i)].get("1.0", "end")[:-1] for i in range(1, 7)]
        if not all(element == "" for element in row):
            for j in range(1, 7):
                MainWindow.Point_dic[(number, j)].delete("1.0", "end")
            break


def clear_data(*args):
    for number in range(MainWindow.Point):
        for i in range(1, 7):
            MainWindow.Point_dic[(number + 1, i)].delete("1.0", "end")


def destroy_data(*args):
    if MainWindow.Point >= 2:
        for i in range(8):
            MainWindow.Point_dic[(MainWindow.Point, i)].destroy()
        MainWindow.Variable.pop(-1)
        MainWindow.Point -= 1


def data_save(*args):
    data = [["X", "Y", "input", "key", "scroll", "delay", "option"]]
    for number in range(MainWindow.Point):
        position_x = MainWindow.Point_dic[(number + 1, 1)].get("1.0", "end")[:-1]
        position_y = MainWindow.Point_dic[(number + 1, 2)].get("1.0", "end")[:-1]
        text = MainWindow.Point_dic[(number + 1, 3)].get("1.0", "end")[:-1]
        key = MainWindow.Point_dic[(number + 1, 4)].get("1.0", "end")[:-1]
        scroll = MainWindow.Point_dic[(number + 1, 5)].get("1.0", "end")[:-1]
        delay = MainWindow.Point_dic[(number + 1, 6)].get("1.0", "end")[:-1]
        option = MainWindow.Variable[number].get()
        if "" in [position_x, position_y] and scroll == "":
            break
        data.append([position_x, position_y, text, key, scroll, delay, option])
    path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")],
                                           initialfile="data.csv")
    if path:
        with open(path, "w") as file:
            writer = csv.writer(file)
            writer.writerows(data)


class MainWindow(tk.Tk):
    Point = 0
    Width = 375
    Height = 205
    Point_dic = {}
    Focus = (0, 0)
    Variable = []
    Thread_done = True
    Font = "宋体 22"

    def __init__(self):
        super().__init__()
        self.geometry(f"{MainWindow.Width}x{MainWindow.Height}+{self.winfo_screenwidth() - MainWindow.Width}+{0}")
        self.title("Mouse")
        self.resizable(True, True)
        self.attributes("-topmost", True)
        self.position_X = tk.Label(text="", font=MainWindow.Font)
        self.position_Y = tk.Label(text="", font=MainWindow.Font)
        self.position_X.grid(row=0, column=1)
        self.position_Y.grid(row=0, column=2)

        MainWindow.Point_dic[(0, 0)] = tk.Text(width=6, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(0, 0)].grid(row=0, column=7)
        MainWindow.Point_dic[(0, 0)].insert("end", "1")
        MainWindow.Point_dic[(0, 0)].tag_add("center", "1.0", "end")
        MainWindow.Point_dic[(0, 0)].tag_configure("center", justify="center")
        # 创建菜单栏
        menubar = tk.Menu(self)
        # 创建文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="打开(⌘ T)", command=self.data_open)
        file_menu.add_command(label="保存(⌘ S)", command=data_save)
        # 创建编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="开始(⌘ 1)", command=self.start)
        edit_menu.add_command(label="删除(⌘ 2)", command=delete_data)
        edit_menu.add_command(label="清空(⌘ 3)", command=clear_data)
        edit_menu.add_command(label="添加(⌘ 4)", command=self.add_data)
        edit_menu.add_command(label="销毁(⌘ 5)", command=destroy_data)
        edit_menu.add_command(label="标记(⌘ F)", command=sign_data)
        # 创建编辑菜单
        edit_menu.add_separator()
        edit_menu.add_command(label="添加输入列", command=self.add_text)
        edit_menu.add_command(label="添加按键列", command=self.add_key)
        edit_menu.add_command(label="添加滚动列", command=self.add_scroll)
        edit_menu.add_separator()
        edit_menu.add_command(label="删除输入列", command=self.delete_text)
        edit_menu.add_command(label="删除按键列", command=self.delete_key)
        edit_menu.add_command(label="删除滚动列", command=self.delete_scroll)
        # 将文件菜单和编辑菜单添加到菜单栏
        menubar.add_cascade(label="文件", menu=file_menu)
        menubar.add_cascade(label="编辑", menu=edit_menu)

        # 将菜单栏配置到主窗口
        self.config(menu=menubar)
        self.text = tk.Label(text="输入", font=MainWindow.Font)
        self.key = tk.Label(text="按键", font=MainWindow.Font)
        self.scroll = tk.Label(text="滚动", font=MainWindow.Font, padx=13)
        self.delay = tk.Label(text="延时", font=MainWindow.Font)
        self.delay.grid(row=0, column=6)

        self.refresh_data()
        self.bind("<KeyRelease>", center_text)
        self.bind("<FocusIn>", handle_focus)
        self.bind("<Command-Key-t>", self.data_open)
        self.bind("<Command-Key-T>", self.data_open)
        self.bind("<Command-Key-s>", data_save)
        self.bind("<Command-Key-S>", data_save)
        self.bind("<Command-Key-f>", sign_data)
        self.bind("<Command-Key-F>", sign_data)
        self.bind("<Command-Key-1>", self.start)
        self.bind("<Command-Key-2>", delete_data)
        self.bind("<Command-Key-3>", clear_data)
        self.bind("<Command-Key-4>", self.add_data)
        self.bind("<Command-Key-5>", destroy_data)
        for _ in range(5):
            self.add_data()

        self.mainloop()

    def add_data(self, *args):
        MainWindow.Point += 1
        MainWindow.Point_dic[(MainWindow.Point, 0)] = tk.Label(text=MainWindow.Point - 1, width=1,
                                                               font=MainWindow.Font, padx=4)
        MainWindow.Point_dic[(MainWindow.Point, 1)] = tk.Text(width=8, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(MainWindow.Point, 2)] = tk.Text(width=8, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(MainWindow.Point, 3)] = tk.Text(width=6, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(MainWindow.Point, 4)] = tk.Text(width=6, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(MainWindow.Point, 5)] = tk.Text(width=6, height=1, font=MainWindow.Font)
        MainWindow.Point_dic[(MainWindow.Point, 6)] = tk.Text(width=6, height=1, font=MainWindow.Font)
        MainWindow.Variable.append(tk.StringVar(self))
        MainWindow.Point_dic[(MainWindow.Point, 7)] = ttk.Combobox(self, textvariable=MainWindow.Variable[-1],
                                                                   width=6, values=["左键", "右键", "移动", "滚动"],
                                                                   state="readonly", justify="center")
        MainWindow.Point_dic[(MainWindow.Point, 7)].bind("<<ComboboxSelected>>", self.combobox_changed)
        MainWindow.Point_dic[(MainWindow.Point, 7)].current(0)
        MainWindow.Point_dic[(MainWindow.Point, 7)].option_add("*TCombobox*Listbox.Justify", "center")

        for i in range(8):
            MainWindow.Point_dic[(MainWindow.Point, i)].grid(row=MainWindow.Point, column=i)
        MainWindow.Point_dic[(MainWindow.Point, 5)].grid_forget()
        if not self.text.winfo_viewable():
            MainWindow.Point_dic[(MainWindow.Point, 3)].grid_forget()
        if not self.key.winfo_viewable():
            MainWindow.Point_dic[(MainWindow.Point, 4)].grid_forget()

    def refresh_data(self):
        self.position_X.config(text="X=" + str(pyautogui.position().x))
        self.position_Y.config(text="Y=" + str(pyautogui.position().y))
        # 递归循环调用after
        self.after(100, self.refresh_data)

    def add_text(self):
        if not self.text.winfo_viewable():
            self.text.grid(row=0, column=3)
            for number in range(MainWindow.Point):
                MainWindow.Point_dic[(number + 1, 3)].grid(row=number + 1, column=3)
            MainWindow.Width += 75
            self.geometry(f"{MainWindow.Width}x{MainWindow.Height}+{self.winfo_screenwidth() - MainWindow.Width}+{0}")

    def delete_text(self):
        if self.text.winfo_viewable():
            self.text.grid_forget()
            for number in range(MainWindow.Point):
                MainWindow.Point_dic[(number + 1, 3)].delete("1.0", "end")
                MainWindow.Point_dic[(number + 1, 3)].grid_forget()
            MainWindow.Width -= 75
            self.geometry(f"{MainWindow.Width}x{MainWindow.Height}+{self.winfo_screenwidth() - MainWindow.Width}+{0}")

    def add_scroll(self):
        if not self.scroll.winfo_viewable():
            self.scroll.grid(row=0, column=5)
            MainWindow.Width += 75
            self.geometry(f"{MainWindow.Width}x{MainWindow.Height}+{self.winfo_screenwidth() - MainWindow.Width}+{0}")

    def delete_scroll(self):
        if self.scroll.winfo_viewable():
            self.scroll.grid_forget()
            for number in range(MainWindow.Point):
                if MainWindow.Point_dic[(number + 1, 5)].winfo_viewable():
                    MainWindow.Point_dic[(number + 1, 1)].grid(row=number + 1, column=1)
                    MainWindow.Point_dic[(number + 1, 2)].grid(row=number + 1, column=2)
                    if self.text.winfo_viewable():
                        MainWindow.Point_dic[(number + 1, 3)].grid(row=number + 1, column=3)
                    MainWindow.Point_dic[(number + 1, 5)].delete("1.0", "end")
                    MainWindow.Point_dic[(number + 1, 5)].grid_forget()
                    MainWindow.Point_dic[(number + 1, 7)].set("左键")
            MainWindow.Width -= 75
            self.geometry(f"{MainWindow.Width}x{MainWindow.Height}+{self.winfo_screenwidth() - MainWindow.Width}+{0}")

    def add_key(self):
        if not self.key.winfo_viewable():
            self.key.grid(row=0, column=4)
            for number in range(MainWindow.Point):
                MainWindow.Point_dic[(number + 1, 4)].grid(row=number + 1, column=4)
            MainWindow.Width += 75
            self.geometry(f"{MainWindow.Width}x{MainWindow.Height}+{self.winfo_screenwidth() - MainWindow.Width}+{0}")

    def delete_key(self):
        if self.key.winfo_viewable():
            self.key.grid_forget()
            for number in range(MainWindow.Point):
                MainWindow.Point_dic[(number + 1, 4)].delete("1.0", "end")
                MainWindow.Point_dic[(number + 1, 4)].grid_forget()
            MainWindow.Width -= 75
            self.geometry(f"{MainWindow.Width}x{MainWindow.Height}+{self.winfo_screenwidth() - MainWindow.Width}+{0}")

    def combobox_changed(self, event):
        selected_value = event.widget.get()
        grid_info = event.widget.grid_info()
        row = grid_info['row']
        if selected_value == "滚动":
            self.add_scroll()
            MainWindow.Point_dic[(row, 1)].delete("1.0", "end")
            MainWindow.Point_dic[(row, 1)].grid_forget()
            MainWindow.Point_dic[(row, 2)].delete("1.0", "end")
            MainWindow.Point_dic[(row, 2)].grid_forget()
            MainWindow.Point_dic[(row, 3)].delete("1.0", "end")
            MainWindow.Point_dic[(row, 3)].grid_forget()
            MainWindow.Point_dic[(row, 4)].delete("1.0", "end")
            MainWindow.Point_dic[(row, 4)].grid_forget()
            MainWindow.Point_dic[(row, 5)].grid(row=row, column=5)
        else:
            MainWindow.Point_dic[(row, 1)].grid(row=row, column=1)
            MainWindow.Point_dic[(row, 2)].grid(row=row, column=2)
            if self.text.winfo_viewable():
                MainWindow.Point_dic[(row, 3)].grid(row=row, column=3)
            if self.key.winfo_viewable():
                MainWindow.Point_dic[(row, 4)].grid(row=row, column=4)
            MainWindow.Point_dic[(row, 5)].delete("1.0", "end")
            MainWindow.Point_dic[(row, 5)].grid_forget()

    def data_open(self, *args):
        legal_list = [0, 1]
        path = tk.filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        with open(path, 'r') as file:
            reader = csv.reader(file)
            header = next(reader, None)
        if path and header is not None:
            clear_data()
            with open(path, 'r') as file:
                reader = csv.reader(file)
                next(reader)
                reader = list(reader)
                while len(list(reader)) > MainWindow.Point:
                    MainWindow.add_data(self)
                for row in reader:
                    if row[2].strip():
                        self.add_text()
                        legal_list.append(2)
                        break
                for row in reader:
                    if row[3].strip():
                        self.add_key()
                        legal_list.append(3)
                        break
                for row in reader:
                    if row[4].strip():
                        self.add_scroll()
                        legal_list.append(4)
                        break
                for number in range(len(reader)):
                    if reader[number][6] == "滚动":
                        MainWindow.Point_dic[(number + 1, 1)].grid_forget()
                        MainWindow.Point_dic[(number + 1, 2)].grid_forget()
                        MainWindow.Point_dic[(number + 1, 3)].grid_forget()
                        MainWindow.Point_dic[(number + 1, 5)].grid(row=number + 1, column=5)
                        MainWindow.Point_dic[(number + 1, 5)].insert("end", reader[number][4])
                        MainWindow.Point_dic[(number + 1, 5)].tag_add("center", "1.0", "end")
                        MainWindow.Point_dic[(number + 1, 5)].tag_configure("center", justify="center")
                    else:
                        for i in legal_list:
                            MainWindow.Point_dic[(number + 1, i + 1)].grid(row=number + 1, column=i + 1)
                            MainWindow.Point_dic[(number + 1, i + 1)].insert("end", reader[number][i])
                            MainWindow.Point_dic[(number + 1, i + 1)].tag_add("center", "1.0", "end")
                            MainWindow.Point_dic[(number + 1, i + 1)].tag_configure("center", justify="center")
                        MainWindow.Point_dic[(number + 1, 5)].grid_forget()
                    MainWindow.Point_dic[(number + 1, 4)].insert("end", reader[number][4])
                    MainWindow.Point_dic[(number + 1, 4)].tag_add("center", "1.0", "end")
                    MainWindow.Point_dic[(number + 1, 4)].tag_configure("center", justify="center")
                    MainWindow.Point_dic[(number + 1, 7)].set(reader[number][6])

    def start(self, *args):
        valid_rows = 0
        cycle = MainWindow.Point_dic[(0, 0)].get("1.0", "end")[:-1]
        if cycle.isnumeric():
            cycle = int(cycle)
        else:
            cycle = 1
        position_list, text_list, key_list, delay_list, scroll_list, option_list = [], [], [], [], [], []

        for number in range(MainWindow.Point):
            position_x = MainWindow.Point_dic[(number + 1, 1)].get("1.0", "end")[:-1]
            position_y = MainWindow.Point_dic[(number + 1, 2)].get("1.0", "end")[:-1]
            text = MainWindow.Point_dic[(number + 1, 3)].get("1.0", "end")[:-1]
            key = MainWindow.Point_dic[(number + 1, 4)].get("1.0", "end")[:-1]
            scroll = MainWindow.Point_dic[(number + 1, 5)].get("1.0", "end")[:-1]
            delay = MainWindow.Point_dic[(number + 1, 6)].get("1.0", "end")[:-1]
            if ("" not in [position_x, position_y] and (not position_x.isdigit() or not position_y.isdigit())) or \
                    ("" in [position_x, position_y] and not scroll.isdigit()):
                valid_rows = number
                break
            # delay
            if delay:
                try:
                    delay = float(delay)
                except ValueError:
                    valid_rows = number
                    break
            else:
                delay = 0.0
            delay_list.append(delay)
            # position
            if position_x.isdigit() and position_y.isdigit():
                position_list.append((int(position_x), int(position_y)))
                text_list.append(text)
            else:
                position_list.append((None, None))
                text_list.append("")
            # key
            if key in pyautogui.KEY_NAMES:
                key_list.append(key)
            else:
                key_list.append(None)
            # scroll
            if scroll.isdigit():
                scroll_list.append(int(scroll))
            else:
                scroll_list.append(None)
            option_list.append(MainWindow.Variable[number].get())
        if valid_rows >= 1:
            self.iconify()
            # wake up
            function_map = {
                "左键": pyautogui.click,
                "右键": pyautogui.rightClick,
                "移动": pyautogui.moveTo,
            }
            if option_list[0] in function_map:
                func = function_map[option_list[0]]
                func(position_list[0])
                if text_list[0]:
                    if text_list[0] != "copy":
                        pyperclip.copy(text_list[0])
                pyautogui.hotkey("command", "v")
            else:
                pyautogui.scroll(scroll_list[0])
            time.sleep(delay_list[0])
            # start
            for _ in range(cycle):
                for number in range(1, valid_rows):
                    if option_list[number] in function_map:
                        func = function_map[option_list[number]]
                        func(position_list[number])
                        if text_list[number]:
                            if text_list[number] != "copy":
                                pyperclip.copy(text_list[number])
                            pyautogui.hotkey("command", "v")
                        if key_list[number]:
                            pyautogui.press(key_list[number])
                    else:
                        pyautogui.scroll(scroll_list[number])
                    time.sleep(delay_list[number])


if __name__ == "__main__":
    MainWindow()
