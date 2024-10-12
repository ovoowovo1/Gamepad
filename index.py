import vgamepad as vg
import time
import keyboard
import pyautogui
import json
import os

# 讀取配置文件
CONFIG_FILE = 'config.json'

if not os.path.exists(CONFIG_FILE):
    print(f"配置文件 {CONFIG_FILE} 不存在。請確保在同一目錄下存在該文件。")
    exit(1)

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    try:
        config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"讀取配置文件時出錯：{e}")
        exit(1)

# 初始化 Xbox 360 控制器
gamepad = vg.VX360Gamepad()

# 初始化滑鼠點擊間隔（以秒為單位）
CLICK_INTERVAL = 0.1  # 每 0.1 秒點擊一次

# 初始化鍵盤按鍵狀態
single_left_click_last = False
auto_left_click_last = False
auto_left_click_last_time = time.time()


# 從配置文件中獲取按鍵映射
joysticks = config.get("joysticks", {})
left_joystick = joysticks.get("left", {})
right_joystick = joysticks.get("right", {})

mouse_clicks = config.get("mouse_clicks", {})
single_left_click_key = mouse_clicks.get("single_left_click", "o")
auto_left_click_key = mouse_clicks.get("auto_left_click", "p")

program_controls = config.get("program_controls", {})
exit_key = program_controls.get("exit", "b")
pause_key = program_controls.get("pause", "z")
resume_key = program_controls.get("resume", "x")

def get_left_joystick_values():
    x = 0.0
    y = 0.0
    speed = 1.0  # 調整速度（範圍：-1.0 到 1.0）

    if keyboard.is_pressed(left_joystick.get('down', 's')):
        y -= speed  # 向下移動，減少 Y 值
    if keyboard.is_pressed(left_joystick.get('up', 'w')):
        y += speed  # 向上移動，增加 Y 值
    if keyboard.is_pressed(left_joystick.get('left', 'a')):
        x -= speed  # 向左移動，減少 X 值
    if keyboard.is_pressed(left_joystick.get('right', 'd')):
        x += speed  # 向右移動，增加 X 值

    # 將值限制在 [-1.0, 1.0] 範圍內
    x = max(min(x, 1.0), -1.0)
    y = max(min(y, 1.0), -1.0)

    return x, y

def get_right_joystick_values():
    x = 0.0
    y = 0.0
    speed = 1.0  # 調整速度（範圍：-1.0 到 1.0）

    if keyboard.is_pressed(right_joystick.get('down', 'k')):
        y -= speed  # 向下移動，減少 Y 值
    if keyboard.is_pressed(right_joystick.get('up', 'i')):
        y += speed  # 向上移動，增加 Y 值
    if keyboard.is_pressed(right_joystick.get('left', 'j')):
        x -= speed  # 向左移動，減少 X 值
    if keyboard.is_pressed(right_joystick.get('right', 'l')):
        x += speed  # 向右移動，增加 X 值

    # 將值限制在 [-1.0, 1.0] 範圍內
    x = max(min(x, 1.0), -1.0)
    y = max(min(y, 1.0), -1.0)

    return x, y

try:
    print("控制左搖桿使用 WASD 鍵，控制右搖桿使用 IJKL 鍵。")
    print(f"按 '{single_left_click_key}' 鍵進行一次左鍵點擊，按住 '{auto_left_click_key}' 鍵無限點擊左鍵。")
    print(f"按 '{pause_key}' 鍵暫停，按 '{resume_key}' 鍵繼續，按 '{exit_key}' 鍵完全退出。")

    paused = False  # 標記是否暫停

    while True:
        # 檢查是否按下退出鍵以完全退出
        if keyboard.is_pressed(exit_key):
            print(f"檢測到 '{exit_key}' 鍵，正在退出程序並重置手柄...")
            break

        # 檢查是否按下暫停鍵以暫停
        if keyboard.is_pressed(pause_key):
            if not paused:
                paused = True
                print("程序已暫停。按繼續鍵以繼續。")
                # 在暫停時，可以選擇將搖桿重置為中立位置
                gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.update()
                time.sleep(0.5)  # 防止重複觸發暫停

        # 檢查是否按下繼續鍵以繼續
        if keyboard.is_pressed(resume_key):
            if paused:
                paused = False
                print("程序已繼續。")
                time.sleep(0.5)  # 防止重複觸發繼續

        # 處理單次左鍵點擊
        if keyboard.is_pressed(single_left_click_key):
            if not single_left_click_last:
                pyautogui.click()  # 左鍵點擊
                print("模擬左鍵點擊。")
                single_left_click_last = True
        else:
            single_left_click_last = False

        # 處理無限左鍵點擊
        if keyboard.is_pressed(auto_left_click_key):
            current_time = time.time()
            if current_time - auto_left_click_last_time >= CLICK_INTERVAL:
                pyautogui.click()  # 左鍵點擊
                auto_left_click_last_time = current_time
                print("模擬左鍵點擊（無限模式）。")



        if not paused:
            # 根據鍵盤輸入獲取左搖桿值
            left_x, left_y = get_left_joystick_values()

            # 設置左搖桿位置
            gamepad.left_joystick_float(x_value_float=left_x, y_value_float=left_y)

            # 根據鍵盤輸入獲取右搖桿值
            right_x, right_y = get_right_joystick_values()

            # 設置右搖桿位置
            gamepad.right_joystick_float(x_value_float=right_x, y_value_float=right_y)

            # 更新手柄狀態
            gamepad.update()

        # 為避免過高的 CPU 使用率，添加短暫的延遲
        time.sleep(0.01)

except KeyboardInterrupt:
    print("用戶通過鍵盤中斷了程序。")

finally:
    # 在退出前重置手柄到默認狀態
    gamepad.reset()
    gamepad.update()
    print("手柄已重置。再見！")
