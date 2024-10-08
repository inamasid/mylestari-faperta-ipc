import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pynput import keyboard

# Global variable to track if the exit combination is pressed
exit_program = False
ctrl_pressed = False  # To track if Ctrl is pressed

# This program make Chrome open in Full Screen | Use Ctrl + Backspace to Exit Chrome

def inject_custom_script(driver):
    # Hide the scrollbar but still allow scrolling
    hide_scroll_bar = """
    var css = 'body::-webkit-scrollbar { display: none; }';
    var style = document.createElement('style');
    style.appendChild(document.createTextNode(css));
    document.head.appendChild(style);
    """

    # Prevent zooming, disable specific keys, and disable the Windows key
    prevent_zoom_and_keys = """
    document.addEventListener('wheel', function(e) {
        if (e.ctrlKey) {
            e.preventDefault();
        }
    }, { passive: false });

    document.addEventListener('keydown', function(e) {
        // Prevent Ctrl + W, Ctrl + F4, Alt + F4, and Windows key
        if ((e.ctrlKey && e.key === 'w') || 
            (e.ctrlKey && e.key === 'F4') || 
            (e.altKey && e.key === 'F4') || 
            (e.key === 'Meta')) {
            e.preventDefault();
        }

        // Prevent other specific keys (F12, Ctrl + Shift + I, etc.)
        if ((e.ctrlKey && e.key === '+') || (e.ctrlKey && e.key === '-') || (e.ctrlKey && e.key === '0') || 
            ['Escape', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'U'].includes(e.key)) {
            e.preventDefault();
        }
        if (e.ctrlKey && (e.key === 'u' || e.key === 'shift' || e.key === 'i' || e.key === 'j' || e.key === 'c')) {
            e.preventDefault();
        }
    }, { passive: false });

    document.addEventListener('contextmenu', function(e) {
        e.preventDefault();
    });
    """

    # Execute the scripts in the browser
    driver.execute_script(hide_scroll_bar)
    driver.execute_script(prevent_zoom_and_keys)

def on_press(key):
    global exit_program, ctrl_pressed

    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True  # Set Ctrl as pressed
    elif key == keyboard.Key.backspace and ctrl_pressed:
        exit_program = True  # Exit if Ctrl + Backspace is pressed

def on_release(key):
    global ctrl_pressed

    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False  # Reset Ctrl state when released

def prevent_exit(driver):
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while not exit_program:
        time.sleep(1)

    driver.quit()

if __name__ == "__main__":
    options = Options()
    options.add_argument("--kiosk")  # Start in fullscreen mode
    options.add_argument("--disable-infobars")  # Hide "controlled by automated software" message
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    # Specify the path to your chromedriver executable
    driver = webdriver.Chrome(options=options)
    driver.get("https://dev.inamas.id")

    # Inject custom CSS and JavaScript
    inject_custom_script(driver)

    # Start the function to prevent exit
    prevent_exit(driver)
