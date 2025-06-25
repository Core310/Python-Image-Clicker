# | Made by 2cz5 | https://github.com/2cz5 | Discord:2cz5 (for questions etc..)

import cv2
import numpy as np
import pyautogui
import threading
import time
import win32gui
import win32con
import keyboard
import os
import logging

killswitch_activated = False


def minimize_cmd_window():
    try:
        hwnd = win32gui.FindWindow("ConsoleWindowClass", None)
        if hwnd != 0:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
    except Exception as e:
        logging.error(f"Error minimizing command prompt window: {e}")


def monitor_killswitch(killswitch_key):
    global killswitch_activated
    while True:
        if keyboard.is_pressed(killswitch_key):
            logging.info("Killswitch activated.")
            killswitch_activated = True
            break
        time.sleep(0.1)


def search_and_click(images, threshold=0.8, click_delay=0.01, killswitch_key='q'):
    method = cv2.TM_CCOEFF_NORMED

    killswitch_thread = threading.Thread(target=monitor_killswitch, args=(killswitch_key,))
    killswitch_thread.start()


while not killswitch_activated:
    minimize_cmd_window()

    screenshot = pyautogui.screenshot()
    screen_np = np.array(screenshot)
    screen_gray = cv2.cvtColor(screen_np, cv2.COLOR_RGB2GRAY)

    for image_path in images:
        if not os.path.exists(image_path):
            logging.error(f"Image not found at '{image_path}'")
            continue  # Skip to the next image if the file doesn't exist

        # Load the image from the database
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        # Perform template matching
        result = cv2.matchTemplate(screen_gray, template, method)

        loc = np.where(result >= threshold)

        if loc[0].size > 0:
            for pt in zip(*loc[::-1]):
                x, y = pt[0] + template.shape[1] // 2, pt[1] + template.shape[0] // 2

                pyautogui.click(x, y)
                #                    logging.info(f"Clicked on {image_path} at ({x}, {y})")
                time.sleep(click_delay)  # Delay between clicks

                if killswitch_activated:
                    break

        if killswitch_activated:
            break

    break  # Run only once

logging.info("Exiting the loop.")


#    logging.info("Exiting the loop.")

def main():
    image_paths = [
        r"res/img.png"  # ,
        # r"",
        # Add more image paths as needed..
    ]

    search_and_click(image_paths)


if __name__ == "__main__":
    main()
