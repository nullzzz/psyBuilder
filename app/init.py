import winreg
import ctypes, sys
from subprocess import check_call


def writeToRegistry(ico_path: str, file_suffix: str = "psy"):
    if ctypes.windll.shell32.IsUserAnAdmin():
        key = winreg.HKEY_CLASSES_ROOT
        a = winreg.CreateKey(key, f".{file_suffix}")
        print(a)
        winreg.SetValue(key, f".{file_suffix}", winreg.REG_SZ, f"{file_suffix}_file")

        file_key = winreg.CreateKey(key, f"{file_suffix}_file")
        winreg.SetValue(file_key, "DefaultIcon", winreg.REG_SZ, ico_path)
        winreg.CloseKey()
        refresh()
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)


def refresh():
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x1A

    SMTO_ABORTIFHUNG = 0x0002

    result = ctypes.c_long()
    SendMessageTimeoutW = ctypes.windll.user32.SendMessageTimeoutW
    SendMessageTimeoutW(HWND_BROADCAST, WM_SETTINGCHANGE, 0, u'Environment', SMTO_ABORTIFHUNG, 5000, ctypes.byref(result))


if __name__ == "__main__":
    writeToRegistry(r"D:\PsyDemo\image\psy.ico")