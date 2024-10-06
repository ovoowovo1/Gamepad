import vgamepad as vg
import time
import keyboard  


gamepad = vg.VDS4Gamepad()


def get_joystick_values():
    x = 0.0
    y = 0.0
    speed = 1.0  # 調整速度（範圍：-1.0 到 1.0）

    if keyboard.is_pressed('w'):
        y -= speed  # 向上移動，減少 Y 值
    if keyboard.is_pressed('s'):
        y += speed  # 向下移動，增加 Y 值
    if keyboard.is_pressed('a'):
        x -= speed  # 向左移動，減少 X 值
    if keyboard.is_pressed('d'):
        x += speed  # 向右移動，增加 X 值

    # 將值限制在 [-1.0, 1.0] 範圍內
    x = max(min(x, 1.0), -1.0)
    y = max(min(y, 1.0), -1.0)

    return x, y

try:
    print("按下 WASD 鍵控制 DS4 左搖桿。按 'p' 完全退出，按 'o' 暫停，按 'i' 繼續。")

    paused = False  # 標記是否暫停

    while True:
        # 檢查是否按下 'p' 鍵以完全退出
        if keyboard.is_pressed('p'):
            print("檢測到 'p' 鍵，正在退出程序並重置手柄...")
            break

        # 檢查是否按下 'o' 鍵以暫停
        if keyboard.is_pressed('o'):
            if not paused:
                paused = True
                print("程序已暫停。按 'i' 繼續。")
                # 在暫停時，可以選擇將搖桿重置為中立位置
                gamepad.left_joystick_float(x_value_float=0.0, y_value_float=0.0)
                gamepad.update()
                time.sleep(0.5)  # 防止多次觸發

        # 檢查是否按下 'i' 鍵以繼續
        if keyboard.is_pressed('i'):
            if paused:
                paused = False
                print("程序已繼續。")
                time.sleep(0.5)  # 防止多次觸發

        if not paused:
            # 根據鍵盤輸入獲取搖桿值
            left_x, left_y = get_joystick_values()

            # 設置左搖桿位置
            gamepad.left_joystick_float(x_value_float=left_x, y_value_float=left_y)
        else:
            # 如果暫停，可以選擇不更新搖桿或保持中立
            pass

        # 更新手柄狀態
        gamepad.update()

        # 添加小延遲以減少 CPU 使用率
        time.sleep(0.05)

except KeyboardInterrupt:
    print("用戶通過鍵盤中斷了程序。")

finally:
    # 在退出前重置手柄到默認狀態
    gamepad.reset()
    gamepad.update()
    print("手柄已重置。再見！")
