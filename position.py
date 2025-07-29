import tkinter as tk
import pyautogui
# 切换到另一个窗口
pyautogui.keyDown("alt")
pyautogui.keyDown("tab")
pyautogui.keyUp("alt")
pyautogui.keyUp("tab")

# 创建一个透明窗口
root = tk.Tk()
root.attributes("-alpha", 0.5)  # 设置窗口透明度，0.0表示完全透明，1.0表示完全不透明

# 获取屏幕宽度和高度
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# 设置窗口大小为整个屏幕
root.geometry(f"{screen_width}x{screen_height}+0+0")

def record_mouse_click(event):
    # 获取鼠标点击的坐标
    x, y = pyautogui.position()
    print(f"鼠标点击坐标：({x}, {y})")
    # 这里你可以保存坐标到文件或进行其他操作

# 绑定鼠标点击事件
root.bind("<Button-1>", record_mouse_click)

# 运行GUI主循环
root.mainloop()
