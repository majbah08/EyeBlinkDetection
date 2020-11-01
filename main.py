# This is a sample Python script.
import subprocess
import sys
import eye2
import cv2


# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
     # Press Ctrl+F8 to toggle the breakpoint.
    totalcount=eye2.blink_count("gg.mp4")
   # s2_out = subprocess.check_output([sys.executable, "script2.py", "34"])
    print(f'Hi, {name}',totalcount)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
