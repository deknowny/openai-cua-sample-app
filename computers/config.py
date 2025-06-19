from .default import *
from .contrib import *


from .computer import Computer



import pyautogui
import time
from typing import List, Dict, Literal
from Quartz import CGWindowListCopyWindowInfo, kCGWindowListOptionOnScreenOnly, kCGNullWindowID
import subprocess
import base64
from io import BytesIO
from PIL import ImageGrab


class MacComputer:
    def get_environment(self) -> Literal["windows", "mac", "linux", "browser"]:
        return "mac"

    def get_dimensions(self) -> tuple[int, int]:
        width, height = pyautogui.size()
        return width, height

    def screenshot(self) -> str:
        screenshot = ImageGrab.grab()
        buffer = BytesIO()
        screenshot.save(buffer, format="PNG")
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode("utf-8")

    def click(self, x: int, y: int, button: str = "left") -> None:
        pyautogui.click(x, y, button=button)

    def double_click(self, x: int, y: int) -> None:
        pyautogui.doubleClick(x, y)

    def scroll(self, x: int, y: int, scroll_x: int, scroll_y: int) -> None:
        pyautogui.moveTo(x, y)
        pyautogui.scroll(scroll_y)

    def type(self, text: str) -> None:
        pyautogui.write(text)

    def wait(self, ms: int = 1000) -> None:
        time.sleep(ms / 1000)

    def move(self, x: int, y: int) -> None:
        pyautogui.moveTo(x, y)

    def keypress(self, keys: List[str]) -> None:
        for key in keys:
            pyautogui.press(key)

    def drag(self, path: List[Dict[str, int]]) -> None:
        if not path:
            return
        pyautogui.moveTo(path[0]["x"], path[0]["y"])
        pyautogui.mouseDown()
        for point in path[1:]:
            pyautogui.moveTo(point["x"], point["y"])
        pyautogui.mouseUp()

    def get_current_url(self) -> str:
        # Use AppleScript to get frontmost Safari or Chrome tab URL
        try:
            script = '''
            tell application "System Events"
                set frontApp to name of first application process whose frontmost is true
            end tell

            if frontApp is "Safari" then
                tell application "Safari"
                    return URL of front document
                end tell
            else if frontApp is "Google Chrome" then
                tell application "Google Chrome"
                    return URL of active tab of front window
                end tell
            end if
            '''
            return subprocess.check_output(["osascript", "-e", script]).decode().strip()
        except Exception as e:
            return "unknown"


computers_config = {
    "local-playwright": LocalPlaywrightBrowser,
    "docker": DockerComputer,
    "browserbase": BrowserbaseBrowser,
    "scrapybara-browser": ScrapybaraBrowser,
    "scrapybara-ubuntu": ScrapybaraUbuntu,
}
