import sys
import threading
import time
import pyautogui
from pynput import keyboard
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSpinBox
)

# 记录器全局变量
recording = False
actions = []
stop_flag = False

def record_mouse():
    global recording, actions
    actions.clear()
    recording = True
    print("开始录制: 按 F11 停止录制")
    while recording:
        x, y = pyautogui.position()
        actions.append(("mouse", "move", x, y))
        time.sleep(0.5)

def save_actions(file):
    with open(file, "w", encoding="utf-8") as f:
        for action in actions:
            f.write(",".join(map(str, action)) + "\n")

def replay_actions(file, loop_count):
    global stop_flag
    with open(file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for _ in range(loop_count):
        for line in lines:
            if stop_flag:
                return
            parts = line.strip().split(',')
            if len(parts) < 3:
                continue
            action_type, event_type, *params = parts
            if action_type == "mouse":
                x, y = map(int, params)
                if event_type == "move":
                    pyautogui.moveTo(x, y)
                    time.sleep(0.2)
                elif event_type == "click":
                    pyautogui.click(x, y)
                    time.sleep(0.2)
            elif action_type == "sleep":
                time.sleep(float(event_type))

def on_press(key):
    global recording, stop_flag
    if key == keyboard.Key.f11:
        print("F11 被按下，终止录制或执行")
        recording = False
        stop_flag = True
        return False

class AutoClickerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自动执行脚本工具")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.record_btn = QPushButton("开始录制")
        self.record_btn.clicked.connect(self.start_recording)

        self.replay_btn = QPushButton("选择文件并开始执行")
        self.replay_btn.clicked.connect(self.select_and_replay)

        self.label = QLabel("循环次数:")
        self.spin_box = QSpinBox()
        self.spin_box.setMinimum(1)
        self.spin_box.setValue(1)

        layout.addWidget(self.record_btn)
        layout.addWidget(self.replay_btn)
        layout.addWidget(self.label)
        layout.addWidget(self.spin_box)
        self.setLayout(layout)

    def start_recording(self):
        save_path, _ = QFileDialog.getSaveFileName(self, "保存录制", "actions.txt", "Text Files (*.txt)")
        if save_path:
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            threading.Thread(target=self._record_and_save, args=(save_path,), daemon=True).start()

    def _record_and_save(self, save_path):
        record_mouse()
        save_actions(save_path)
        print("录制完成，已保存")

    def select_and_replay(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择脚本文件", "", "Text Files (*.txt)")
        if file_path:
            global stop_flag
            stop_flag = False
            listener = keyboard.Listener(on_press=on_press)
            listener.start()
            loop_count = self.spin_box.value()
            threading.Thread(target=replay_actions, args=(file_path, loop_count), daemon=True).start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoClickerApp()
    window.show()
    sys.exit(app.exec())
