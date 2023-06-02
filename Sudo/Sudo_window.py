import copy
import tkinter.filedialog
import tkinter.messagebox
from opencv.opencv import open_cv
from sudo_solve import sudo


def main():
    def package(demo_package):
        global File_Path
        text = txt.get("1.0", "end")
        if File_Path:
            demo_package = open_cv(File_Path)
            File_Path = None
        elif text != "\n":
            number = 0
            for i in text:
                if i.isnumeric():
                    demo_package[number // 9][number - 9 * (number // 9)] = int(i)
                    number += 1
                    if number == 81:
                        break
        else:
            for y_package in range(9):
                for x_package in range(9):
                    if dic[(y_package, x_package)].get("1.0", "end") != "\n":
                        demo_package[y_package][x_package] = int(dic[(y_package, x_package)].get("1.0", "end")[0])

        return demo_package

    def error(string):
        tkinter.messagebox.showinfo(message=string, type=None)
        button_start.config(state=tkinter.NORMAL)

    def output():
        txt.delete("1.0", "end")
        for y_output in range(9):
            for x_output in range(9):
                dic[(y_output, x_output)].delete("1.0", "end")
                if not demo_copy[y_output][x_output]:
                    dic[(y_output, x_output)].config(fg="lightskyblue")
                else:
                    dic[(y_output, x_output)].config(fg="slategrey")
                dic[(y_output, x_output)].insert("1.0", str(demo[y_output][x_output]))
                dic[(y_output, x_output)].tag_add("center", "1.0", "end")
                dic[(y_output, x_output)].tag_configure("center", justify='center')
                dic[(y_output, x_output)].config(state=tkinter.DISABLED)
                if not x_output and y_output:
                    txt.insert("end", "\n")
                txt.insert("end", str(demo[y_output][x_output]))

        return True

    demo = [[0 for _ in range(9)] for _ in range(9)]
    button_start.config(state=tkinter.DISABLED)
    demo = package(demo)
    demo_copy = copy.deepcopy(demo)
    try:
        demo, t = sudo(demo)
        output()
    except TypeError:
        error("输入数独错误！")
        return False
    if t < 0.1:
        time_label.config(text=str("%.1f" % (1000 * t)) + "ms")
    else:
        time_label.config(text=str("%.1f" % t) + "s")
    button_start.config(state=tkinter.NORMAL)


def change_path():
    global File_Path
    File_Path = tkinter.filedialog.askopenfilename()
    main()


def clear():
    button_start.config(state=tkinter.NORMAL)
    txt.delete("1.0", "end")
    time_label.config(text="0.0ms")
    for y_clear in range(9):
        for x_clear in range(9):
            dic[(y_clear, x_clear)].config(state=tkinter.NORMAL)
            dic[(y_clear, x_clear)].delete("1.0", "end")
            dic[(y_clear, x_clear)].config(fg="slategrey")


# 定义一个事件处理程序，用于在用户手动输入文本后将其居中对齐
def center_text(event):
    if dic[Focus].get("1.0", "end") in [str(number) + "\n" for number in range(1, 10)]:
        dic[Focus].tag_remove("center", "1.0", "end")
        dic[Focus].tag_add("center", "1.0", "end")
        dic[Focus].tag_configure("center", justify='center')
    else:
        dic[Focus].delete("end-2c")


def handle_focus(event):
    global Focus
    for dic_pair in dic.items():
        if dic_pair[1] == event.widget:
            Focus = dic_pair[0]
            break


root = tkinter.Tk()
root.geometry('%dx%d+%d+%d' % (703, 535,
                               (root.winfo_screenwidth() - 703) / 2,
                               (root.winfo_screenheight() - 535) / 2.5))
root.resizable(False, False)
root.title("Sudo")
photo = tkinter.PhotoImage(file="bg.gif")
tkinter.Label(root, image=photo).grid(row=0, column=0, rowspan=10, columnspan=10)
time_label = tkinter.Label(root, width=0, height=0, text="0.0ms", fg="sienna", font="Osaka 32", bg="#a3e4ff")
time_label.grid(row=8, column=9)
root.bind("<KeyRelease>", center_text)
root.bind("<FocusIn>", handle_focus)
button_start = tkinter.Button(root, text="开始", command=main, width=8, height=0, font="宋体 17")
button_start.grid(row=0, column=9)

button_photo = tkinter.Button(root, text="文件", command=change_path, width=8, height=0, font="宋体 17")
button_photo.grid(row=1, column=9)

button_clear = tkinter.Button(root, text="清空", command=clear, width=8, height=0, font="宋体 17")
button_clear.grid(row=2, column=9)

txt = tkinter.Text(root, width=9, height=10, font="Osaka 20", fg="slategrey", bg="white")
txt.grid(row=2, column=9, rowspan=7)

dic = dict()
Focus = (0, 0)
File_Path = str()
for y in range(9):
    for x in range(9):
        label = tkinter.Text(root, width=2, height=0, font="Osaka 32", bg="white", relief="groove", fg="slategrey")
        label.grid(row=y, column=x, padx=3, pady=3)
        dic[(y, x)] = label

root.mainloop()
