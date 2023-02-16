from ctypes import windll

if __name__ == '__main__':
    # https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-messageboxa
    libc = windll.user32
    message_box = libc.MessageBoxA
    MB_OK = 0x0
    MB_OKCXL = 0x01
    MB_YESNOCXL = 0x03
    MB_YESNO = 0x04
    MB_HELP = 0x4000

    # icons
    ICON_EXCLAIM = 0x30
    ICON_INFO = 0x40
    ICON_STOP = 0x10
    message_box(None, b"Your text", b"Your title", MB_HELP | MB_YESNO | ICON_EXCLAIM)
