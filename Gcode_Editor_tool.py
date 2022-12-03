from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from os import walk
import os
from PIL import ImageTk, Image
filename = ''
mulit_filename = []
batch_state = False
filepath = ''#批量處理存的數據資料夾
def browseFiles():#檔案瀏覽器
    global filename,batch_state
    batch_state = False
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("Text files",
                                                      "*.anc*"),
                                                     ("all files",
                                                      "*.*")))

    # Change label contents
    label_file_explorer.configure(text="File Opened: " + filename)
def batchbrowseFiles():#批量處理檔案
    global mulit_filename,batch_state,filepath
    batch_state = True
    filepath = filedialog.askdirectory()
    for root, dirs, files in walk(filepath):
        mulit_filename = files
        filepath = root
    label_file_explorer.configure(text="batch File Opened: " + filepath)
def validate(P):#限制只能輸入數字
    if str.isdigit(P) or P == '':
        return True
    else:
        return False
def export():
    global filename,mulit_filename,batch_state,filepath
    print(batch_state)
    data=[]
    if(batch_state):#批量處理
        if(filepath!= ''):
            for filename_ in mulit_filename:
                target=0#目標行
                count =0
                print(filepath+'/'+filename_)
                f = open(filepath+'/'+filename_, 'r')
                for i in f.readlines():
                    data.append(i)  # 將文件內容填入data
                    count+=1
                    if (i == "N17 (TCP)\n"):  # 如果找到目標更改行數
                        target = count  # 使得目標行等於計數器數字
                path_split = filename.split('/')
                filepath.replace(path_split[len(path_split) - 1], "")#把路徑切到最後一個資料夾
                if not os.path.isdir(filepath.replace(path_split[len(path_split) - 1], "")+path_split[len(path_split) - 1]+"_prossed"):#如果該路徑沒有這個資料夾
                    os.mkdir(filepath.replace(path_split[len(path_split) - 1], "")+path_split[len(path_split) - 1]+"_prossed")#則創一個新資料夾
                new_file_path = filepath.replace(path_split[len(path_split) - 1], "")+path_split[len(path_split) - 1]+"_prossed\\"+filename_#建立路徑與檔名
                Z_value = myentry.get()
                #處理要插入的Gcode
                up_tool_gcode = data[target].replace("N18","   ")#把N18替換成三個空格
                if (Z_value != ''):
                    up_tool_gcode = up_tool_gcode.replace(up_tool_gcode[up_tool_gcode.find("Z") + 1:up_tool_gcode.find("C") - 1],str(Z_value))#換成自己的Z Value
                    data.insert(target,up_tool_gcode)
                    add_code_infinal = 'G0 Z' + str(Z_value) + '\n'
                elif (Z_value == ''):
                    up_tool_gcode = up_tool_gcode.replace(up_tool_gcode[up_tool_gcode.find("Z") + 1:up_tool_gcode.find("C") - 1],"200")  # 換成自己的Z Value
                    data.insert(target,up_tool_gcode)
                    add_code_infinal = 'G0 Z200\n'
                data.append(add_code_infinal)
                with open(new_file_path, 'w') as f_ed:
                    for i in data:
                        f_ed.write(i)
                    f_ed.close()
                print("exporting ")
                data =[]
            filepath=''#清空 以免誤處理
            label_file_explorer.configure(text="File unselect ")
            mulit_filename=[]
            messagebox.showinfo('提示', '導出完成！\n祝您撞機')
        else:
            messagebox.showinfo('提示', '欸！\n你沒選檔案我是要處理個毛')
    elif(batch_state==False):
        if(filename!=''):
            f = open(filename, 'r')
            target = 0  # 目標行
            count = 0
            for i in f.readlines():
                data.append(i)  # 將文件內容填入data
                count += 1
                if (i == "N17 (TCP)\n"):  # 如果找到目標更改行數
                    target = count  # 使得目標行等於計數器數字
            splt_file = filename.split(".")
            new_file_path = splt_file[0]+"edited."+splt_file[1]
            Z_value = myentry.get()
            # 處理要插入的Gcode
            up_tool_gcode = data[target].replace("N18", "   ")  # 把N18替換成三個空格
            if(Z_value!=''):
                up_tool_gcode = up_tool_gcode.replace(
                    up_tool_gcode[up_tool_gcode.find("Z") + 1:up_tool_gcode.find("C") - 1],
                    str(Z_value))  # 換成自己的Z Value
                data.insert(target, up_tool_gcode)
                add_code_infinal = 'G0 Z'+str(Z_value)+'\n'
            elif(Z_value ==''):
                up_tool_gcode = up_tool_gcode.replace(
                up_tool_gcode[up_tool_gcode.find("Z") + 1:up_tool_gcode.find("C") - 1], "200")  # 換成自己的Z Value
                data.insert(target, up_tool_gcode)
                add_code_infinal = 'G0 Z200\n'
            data.append(add_code_infinal)
            with open(new_file_path, 'w') as f_ed:
                for i in data:
                    print(i)
                    f_ed.write(i)
                f_ed.close()
            print("exporting ")
            label_file_explorer.configure(text="File unselect ")
            messagebox.showinfo('提示', '導出完成！\n祝您撞機')
            filename=''
        else:
            messagebox.showinfo('提示', '欸！\n你沒選檔案我是要處理個毛')
def exit():
    window.destroy()
window = Tk()# Create the root window
window.title('Gcode editor ')# 設定視窗標題
window.geometry("700x500")# 設定視窗大小
window.iconphoto(False, PhotoImage(file='icon.ico'))
canvas = Canvas(window, width=586,height=442,bd=0, highlightthickness=0)

imgpath = '2YOYOdi.gif'
img = Image.open(imgpath)
photo = ImageTk.PhotoImage(img)
canvas.create_image(586/2, 442/2, image=photo)
canvas.pack()#.grid(ipadx = 0,ipady = 0)
# Set window background color
window.config(background="white")
mylabel = Label(window, text='Z軸數值:')
vcmd = (window.register(validate), '%P')
myentry = Entry(window,validate='key', validatecommand=vcmd)
# Create a File Explorer label
label_file_explorer = Label(window,
                            text="File Explorer using Tkinter",
                            width=30, height=4,
                            fg="blue")
label_KeyInBox = Label(window,
                            text="請輸入Z值 預設是200",
                            width=30, height=4,
                            fg="blue")
button_explore = Button(window,
                        text="選anc檔案",
                        command=browseFiles)
button_exit = Button(window,
                     text="離開",
                     command=exit)
button_export = Button(window,
                     text="導出",
                     command=export)
button_batch_explore = Button(window,
                        text="選資料夾(批量處理)",
                        command=batchbrowseFiles)
mylabel.place(x=20,y=70)#
myentry.place(x=20,y=90)#.pack()#.grid(row=7, column=1)
label_file_explorer.place(x=0,y=0)#.pack()#grid(column=1, row=1)
label_KeyInBox.place(x=0,y=110)#.pack()#.grid(row=6, column=1)
button_explore.place(x=0,y=180)#.pack()#.grid(column=1, row=2)
button_batch_explore.place(x=0,y=210)#.pack()#.grid(column=1, row=5)
button_export.pack()#place(x=0,y=240)#.grid(column=1, row=4)
button_exit.pack()
# Let the window wait for any events
window.mainloop()