import sys
import time
import threading
import pyautogui

from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QFileDialog
)
from PyQt6.QtCore import QEvent, Qt

running = False  # 控制执行状态
actions_filename = "actions.txt"

def replay_actions(loop_count, status_label):
    global running
    global actions_filename
    running = True
    pyautogui.keyDown("alt")
    pyautogui.keyDown("tab")
    pyautogui.keyUp("alt")
    pyautogui.keyUp("tab")
    for loop in range(loop_count):
        if not running:
            status_label.setText("已停止")
            return
        status_label.setText(f"状态：已切至后台，执行中, 第{loop+1}回")
        with open(actions_filename, "r", encoding="utf-8") as file:
            for line in file:
                if not running:
                    status_label.setText("已停止")
                    return
                if line.startswith("//") or line.strip() == "":
                    continue
                parts = line.strip().split(',')
                action_type, event_type, *params = parts
                if action_type == "keyboard":
                    key = params[0]
                    if event_type == "down":
                        pyautogui.keyDown(key)
                    elif event_type == "up":
                        pyautogui.keyUp(key)
                        time.sleep(0.02)
                elif action_type == "mouse":
                    x, y = map(int, params)
                    if event_type == "move":
                        pyautogui.moveTo(x, y)
                        time.sleep(0.2)
                    elif event_type == "click":
                        pyautogui.click(x, y)
                        time.sleep(0.2)
                elif action_type == "sleep":
                    time.sleep(float(event_type))
                elif action_type == "scroll":
                    pyautogui.scroll(int(event_type))
    running = False
    status_label.setText("执行完毕")


class AutoRunner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("自动操作执行器")
        self.setGeometry(200, 200, 300, 200)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)

        self.was_in_background = False

        # file path
        self.path_input = QLineEdit(self)
        self.path_input.setReadOnly(True)
        self.path_input.setText("actions.txt")
        self.browse_button = QPushButton("选择脚本", self)
        self.browse_button.clicked.connect(self.choose_script_file)
        file_path_layout = QHBoxLayout()
        file_path_layout.addWidget(self.path_input)
        file_path_layout.addWidget(self.browse_button)

        # loop editer
        self.loop_text = QLabel("循环次数:")
        self.loop_input = QLineEdit("1")
        self.loop_input.setPlaceholderText("输入循环次数")
        loop_editer_layout = QHBoxLayout()
        loop_editer_layout.addWidget(self.loop_text)
        loop_editer_layout.addWidget(self.loop_input)

        # Start Stop
        self.start_button = QPushButton("开始执行")
        self.stop_button = QPushButton("停止执行")
        self.start_button.clicked.connect(self.start_execution)
        self.stop_button.clicked.connect(self.stop_execution)
        start_stop_layout = QHBoxLayout()
        start_stop_layout.addWidget(self.start_button)
        start_stop_layout.addWidget(self.stop_button)

        self.status_label = QLabel("等待开始...")

        layout = QVBoxLayout()
        layout.addLayout(file_path_layout)
        layout.addLayout(loop_editer_layout)
        layout.addLayout(start_stop_layout)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def changeEvent(self, event):
        global running
        if event.type() == QEvent.Type.ActivationChange:
            if self.isActiveWindow():
                if running:
                    running = False
                    self.status_label.setText("状态：已切回前台，停止执行")
                else:
                    self.status_label.setText("状态：已切回前台, 未执行")
                self.was_in_background = False
            else:
                if running:
                    self.status_label.setText("状态：已切至后台，执行中")
                else:
                    self.status_label.setText("状态：已切至后台，未执行")
                self.was_in_background = True
        super().changeEvent(event)

    def choose_script_file(self):
        global actions_filename
        file_path, _ = QFileDialog.getOpenFileName(self, "选择脚本文件", "", "Text Files (*.txt);;All Files (*)")
        if file_path:
            actions_filename = file_path
            self.path_input.setText(file_path)

    def start_execution(self):
        try:
            loop_count = int(self.loop_input.text())
        except ValueError:
            self.status_label.setText("请输入有效的数字")
            return

        self.status_label.setText("正在执行...")
        threading.Thread(target=replay_actions, args=(loop_count, self.status_label), daemon=True).start()

    def stop_execution(self):
        global running
        running = False
        self.status_label.setText("已请求停止")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoRunner()
    window.show()
    sys.exit(app.exec())
