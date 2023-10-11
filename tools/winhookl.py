import ctypes
import sys
import win32con
import win32gui
import ctypes.wintypes

# Define necessary Win32 API structures and constants
WH_MOUSE_LL = 14

class MSLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long), ("data", ctypes.c_long), ("flags", ctypes.c_long), ("time", ctypes.c_long), ("extra", ctypes.POINTER(ctypes.c_ulong))]

# Specify the window you want to listen to
target_window_title = "桃花源记2"
target_window = win32gui.FindWindow(None, target_window_title)

if not target_window:
    print(f"Window '{target_window_title}' not found.")
    sys.exit()

print(f"Listening to window '{target_window_title}'...")

# Mouse event constants
mouse_events = {
    0x0201: 'WM_LBUTTONDOWN',
    0x0202: 'WM_LBUTTONUP',
    0x0200: 'WM_MOUSEMOVE',
    0x020A: 'WM_MOUSEWHEEL',
    0x0204: 'WM_RBUTTONDOWN',
    0x0205: 'WM_RBUTTONUP',
    0x0207: 'WM_MBUTTONDOWN',
    0x0208: 'WM_MBUTTONUP'
}

# Define the low-level hook procedure for mouse
def low_level_mouse_proc(n_code, w_param, l_param):
    if n_code == win32con.HC_ACTION:
        mouse_data = ctypes.cast(l_param, ctypes.POINTER(MSLLHOOKSTRUCT)).contents
        hwnd = win32gui.WindowFromPoint((mouse_data.x, mouse_data.y))
        if hwnd == target_window:
            event_type = mouse_events.get(w_param, "Unknown")
            print(f"Mouse event '{event_type}' in target window at ({mouse_data.x}, {mouse_data.y})")

    return ctypes.windll.user32.CallNextHookEx(None, n_code, w_param, l_param)

# Convert Python function to C function pointer (callback)
HOOKPROC = ctypes.WINFUNCTYPE(ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(MSLLHOOKSTRUCT))
mouse_callback = HOOKPROC(low_level_mouse_proc)

# Set the low-level mouse hook
mouse_hook = ctypes.windll.user32.SetWindowsHookExW(WH_MOUSE_LL, mouse_callback, None, 0)

# Message loop to keep the script running
msg = ctypes.wintypes.MSG()
while ctypes.windll.user32.GetMessageW(ctypes.byref(msg), None, 0, 0) != 0:
    ctypes.windll.user32.TranslateMessage(ctypes.byref(msg))
    ctypes.windll.user32.DispatchMessageW(ctypes.byref(msg))

ctypes.windll.user32.UnhookWindowsHookEx(mouse_hook)
