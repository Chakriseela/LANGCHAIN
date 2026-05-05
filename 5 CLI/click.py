import pyautogui
# pyautogui.click(100, 200)


import pyautogui
import time

# Safety: move mouse to corner to stop script
pyautogui.FAILSAFE = True

# Delay before starting (gives you time to switch window)
print("Starting in 5 seconds... Move to target window")
time.sleep(5)

# Get screen size
screen_width, screen_height = pyautogui.size()
print(f"Screen size: {screen_width} x {screen_height}")

# Move mouse smoothly to position
target_x, target_y = 100, 200
pyautogui.moveTo(target_x, target_y, duration=1)

# Highlight action
print(f"Clicking at ({target_x}, {target_y})")

# Perform click
pyautogui.click()

# Take screenshot after action
screenshot = pyautogui.screenshot()
screenshot.save("after_click.png")

print("Done! Screenshot saved.")