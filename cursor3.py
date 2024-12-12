import pyautogui
import keyboard
import time

# Initial step size and increment for cursor movement
INITIAL_STEP_SIZE = 10
STEP_INCREMENT = 5  # Increased increment for faster acceleration
MAX_STEP_SIZE = 100  # Increased max step size

# Dictionary to map keys to cursor movement directions
movement_keys = {
    'w': (0, -1),  # Move up
    's': (0, 1),   # Move down
    'a': (-1, 0),  # Move left
    'd': (1, 0)    # Move right
}

print("Hold LEFT SHIFT to control the mouse cursor using 'W', 'A', 'S', 'D'. Press 'Q' for left-click, 'E' for right-click, 'R' for drag-and-drop, and 'F' for scrolling.")

try:
    step_size = INITIAL_STEP_SIZE
    active_key = None
    key_press_start = None
    is_dragging = False

    _x, _y = pyautogui.position()
    while True:
        cur_x, cur_y = pyautogui.position()
        if (_x!=cur_x and _y!=cur_y):
            print(cur_x, cur_y)
            _x, _y = cur_x, cur_y

        if keyboard.is_pressed('shift'):  # Check if LEFT SHIFT is held down
            for key, direction in movement_keys.items():
                if keyboard.is_pressed(key):
                    if active_key != key:
                        active_key = key
                        key_press_start = time.time()
                        step_size = INITIAL_STEP_SIZE

                    # Calculate how long the key has been held
                    duration = time.time() - key_press_start
                    step_size = min(INITIAL_STEP_SIZE + int(duration * STEP_INCREMENT), MAX_STEP_SIZE)

                    current_x, current_y = pyautogui.position()
                    new_x = current_x + direction[0] * step_size
                    new_y = current_y + direction[1] * step_size
                    pyautogui.moveTo(new_x, new_y)
                    time.sleep(0.02)  # Small delay for smoother movement
                    break
            else:
                # Reset when no movement key is pressed
                active_key = None
                key_press_start = None
                step_size = INITIAL_STEP_SIZE

            # Handle left-click
            if keyboard.is_pressed('q'):
                pyautogui.click()  # Perform left-click
                time.sleep(0.1)  # Prevent multiple rapid clicks

            # Handle right-click
            if keyboard.is_pressed('e'):
                pyautogui.click(button='right')  # Perform right-click
                time.sleep(0.1)  # Prevent multiple rapid clicks

            # Handle drag-and-drop
            if keyboard.is_pressed('r'):
                if not is_dragging:
                    pyautogui.mouseDown()  # Start dragging
                    is_dragging = True
                else:
                    pyautogui.mouseUp()  # Drop
                    is_dragging = False
                time.sleep(0.2)  # Prevent rapid toggling

            # Handle scrolling
            if keyboard.is_pressed('f'):
                pyautogui.scroll(100)  # Scroll up
                time.sleep(0.1)  # Prevent multiple rapid scrolls

except KeyboardInterrupt:
    print("Program interrupted.")

except Exception as e:
    print(f"An error occurred: {e}")
