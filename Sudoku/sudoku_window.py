import copy
import tkinter.filedialog
import tkinter.messagebox

from sudoku_DFS import sudo_solve
from opencv.opencv import open_cv


def main():
    def package(demo_package):
        global File_Path
        text = txt.get("1.0", "end")[:-1]
        if File_Path:
            demo_package = open_cv(File_Path)
            File_Path = None
        elif text:
            number = 0
            for i in text:
                if i.isnumeric():
                    demo_package[number // 9][number - 9 * (number // 9)] = int(i)
                    number += 1
                    if number == 81:
                        break
        else:
            for r in range(9):
                for c in range(9):
                    if dic[(r, c)].get("1.0", "end")[:-1].isnumeric():
                        demo_package[r][c] = int(dic[(r, c)].get("1.0", "end"))

        return demo_package

    def output():
        txt.delete("1.0", "end")
        for r in range(9):
            for c in range(9):
                dic[(r, c)].delete("1.0", "end")
                if demo_copy[r][c]:
                    dic[(r, c)].config(fg="slategrey")
                else:
                    dic[(r, c)].config(fg="lightskyblue")
                dic[(r, c)].insert("end", str(demo[r][c]))
                dic[(r, c)].tag_add("center", "1.0", "end")
                dic[(r, c)].tag_configure("center", justify="center")
                dic[(r, c)].config(state=tkinter.DISABLED)
                if not c and r:
                    txt.insert("end", "\n")
                txt.insert("end", str(demo[r][c]))

    button_start.config(state=tkinter.DISABLED)
    demo = [[0 for _ in range(9)] for _ in range(9)]
    demo = package(demo)
    demo_copy = copy.deepcopy(demo)
    demo, t = sudo_solve(demo)
    if demo:
        output()
        time_label.config(text=f"{1000 * t:.1f}ms")
    else:
        tkinter.messagebox.showinfo(message="输入数独错误！", type=None)
    button_start.config(state=tkinter.NORMAL)


def change_path():
    global File_Path
    File_Path = tkinter.filedialog.askopenfilename()
    main()


def clear():
    button_start.config(state=tkinter.NORMAL)
    txt.delete("1.0", "end")
    time_label.config(text="0.0ms")
    for r in range(9):
        for c in range(9):
            dic[(r, c)].config(state=tkinter.NORMAL)
            dic[(r, c)].delete("1.0", "end")
            dic[(r, c)].config(fg="slategrey")
            dic[(r, c)].tag_add("center", "1.0", "end")
            dic[(r, c)].tag_configure("center", justify="center")


# 定义一个事件处理程序，用于在用户手动输入文本后将其居中对齐
def center_text(event):
    if dic[Focus].get("1.0", "end") not in [str(i)+"\n" for i in range(1, 10)]:
        dic[Focus].delete("end-2c")
    dic[Focus].tag_add("center", "1.0", "end")
    dic[Focus].tag_configure("center", justify="center")


def handle_focus(event):
    global Focus
    for dic_pair in dic.items():
        if dic_pair[1] == event.widget:
            Focus = dic_pair[0]
            break


root = tkinter.Tk()
root.geometry(f"{703}x{535}+{int((root.winfo_screenwidth() - 703) / 2)}+{int((root.winfo_screenheight() - 535) / 2.5)}")

root.resizable(False, False)
root.title("Sudoku")
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

dic = {}
Focus = (0, 0)
File_Path = ""
for y in range(9):
    for x in range(9):
        label = tkinter.Text(root, width=2, height=0, font="Osaka 32", bg="white", relief="groove", fg="slategrey")
        label.grid(row=y, column=x, padx=3, pady=3)
        dic[(y, x)] = label
        dic[(y, x)].tag_add("center", "1.0", "end")
        dic[(y, x)].tag_configure("center", justify="center")

root.mainloop()
