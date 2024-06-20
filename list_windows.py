import win32gui

def list_windows():
    def callback(hwnd, hwnd_list):
        if win32gui.IsWindowVisible(hwnd):
            hwnd_list.append((hwnd, win32gui.GetWindowText(hwnd)))
        return True

    hwnd_list = []
    win32gui.EnumWindows(callback, hwnd_list)
    return hwnd_list

# Example usage to list all visible windows
if __name__ == "__main__":
    windows = list_windows()
    for hwnd, title in windows:
        print(f"HWND: {hwnd}, Title: {title}")
