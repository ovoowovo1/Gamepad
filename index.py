import vgamepad as vg
import time
import keyboard  

gamepad = vg.VX360Gamepad()

def get_left_joystick_values():
    x = 0.0
    y = 0.0
    speed = 1.0  # 調整速度（範圍：-1.0 到 1.0）

    if keyboard.is_pressed('s'):
        y -= speed  # 向下移動，減少 Y 值
    if keyboard.is_pressed('w'):
        y += speed  # 向上移動，增加 Y 值
    if keyboard.is_pressed('a'):
        x -= speed  # 向左移動，減少 X 值
    if keyboard.is_pressed('d'):
        x += speed  # 向右移動，增加 X 值

    # 將值限制在 [-1.0, 1.0] 範圍內
    x = max(min(x, 1.0), -1.0)
    y = max(min(y, 1.0), -1.0)

    return x, y

def get_right_joystick_values():
    x = 0.0
    y = 0.0
    speed = 1.0  # 調整速度（範圍：-1.0 到 1.0）

    if keyboard.is_pressed('down'):
        y -= speed  # 向下移動，減少 Y 值
    if keyboard.is_pressed('up'):
        y += speed  # 向上移動，增加 Y 值
    if keyboard.is_pressed('left'):
        x -= speed  # 向左移動，減少 X 值
    if keyboard.is_pressed('right'):
        x += speed  # 向右移動，增加 X 值

    # 將值限制在 [-1.0, 1.0] 範圍內
    x = max(min(x, 1.0), -1.0)
    y = max(min(y, 1.0), -1.0)

    return x, y

try:
    print("控制左搖桿使用 WASD 鍵，控制右搖桿使用方向鍵。按 'p' 完全退出，按 'z' 暫停，按 'x' 繼續。")

    paused = False  # 標記是否暫停

    while True:
        # 檢查是否按下 'p' 鍵以完全退出
        if keyboard.is_pressed('p'):
            print("檢測到 'p' 鍵，正在退出程序並重置手柄...")
            break

        # 檢查是否按下 'z' 鍵以暫停
        if keyboard.is_pressed('z'):
            if not paused:
                paused = True
                print("程序已暫停。按 'x' 繼續。")
                # 在暫停時，可以選擇將搖桿重置為中立位置
                gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.right_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.update()

        # 檢查是否按下 'x' 鍵以繼續
        if keyboard.is_pressed('x'):
            if paused:
                paused = False
                print("程序已繼續。")

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



except KeyboardInterrupt:
    print("用戶通過鍵盤中斷了程序。")

finally:
    # 在退出前重置手柄到默認狀態
    gamepad.reset()
    gamepad.update()
    print("手柄已重置。再見！")
