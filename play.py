import pyautogui
import time
import sys

def replay_actions(filename):
    with open(filename, "r") as file:
        for line in file:
            if line.startswith("//") or line == "":
                continue
            action_type, event_type, *params = line.strip().split(',')
            if action_type == "keyboard":
                key = params[0]
                if event_type == "down":
                    pyautogui.keyDown(key)
                elif event_type == "up":
                    pyautogui.keyUp(key)
                    time.sleep(0.01)
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

args = sys.argv
pyautogui.keyDown("alt")
pyautogui.keyDown("tab")
pyautogui.keyUp("alt")
pyautogui.keyUp("tab")
if 2 <= len(args):
    loopCount = args[1]
    for x in range(int(loopCount)):
        replay_actions("actions.txt")
else:
    replay_actions("actions.txt")
