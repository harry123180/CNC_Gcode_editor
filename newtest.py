import tkinter as tk
from os import listdir
from os.path import isfile, isdir, join
from os import walk

root = tk.Tk()
from tkinter.filedialog import (askopenfilename,
                                    askopenfilenames,
                                    askdirectory,
                                    asksaveasfilename)
a = askdirectory()

print(a,type(a))
# 指定要列出所有檔案的目錄
mypath = a



# 遞迴列出所有子目錄與檔案
for root, dirs, files in walk(mypath):
  print("路徑：", root)
  print("  目錄：", dirs)
  print("  檔案：", files)
  b = root.split('/')
  print(root.replace(b[len(b)-1],""))
