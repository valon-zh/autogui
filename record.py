import keyboard

actions = []
recording = False  # 标志，表示是否正在记录

def start_recording(e):
    global recording
    if e.event_type == keyboard.KEY_DOWN and e.name == 'c' and keyboard.is_pressed('alt') and keyboard.is_pressed('ctrl'):
        recording = not recording
        if recording:
            print("开始记录")
        else:
            print("停止记录")

def record_action(e):
    if recording:
        global mouse_event
        if isinstance(e, keyboard.KeyboardEvent):
            actions.append(f"keyboard,{e.event_type},{e.name}")
        elif isinstance(e, keyboard.MouseEvent):
            if mouse_event is not None and e.event_type == 'up':
                actions.append(f"mouse,{mouse_event.event_type},{e.event_type},{mouse_event.x},{mouse_event.y}")
                mouse_event = None
            else:
                mouse_event = e

keyboard.on_press_key('c', start_recording)

keyboard.hook(record_action)
keyboard.wait('esc')  # 停止录制（按ESC键）

# 将动作保存到文件
with open("actions.txt", "w") as file:
    for action in actions:
        file.write(action + '\n')
