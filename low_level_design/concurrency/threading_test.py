import threading
import time

def print_letters():
    for i in range(10):
        print(chr(i+ord('a')))
        time.sleep(1)

def print_nums():
    for i in range(10):
        print(i)
        time.sleep(1)

thread_1 = threading.Thread(target=print_letters)
thread_2 = threading.Thread(target=print_nums)

thread_1.start()
thread_2.start()

thread_1.join()
thread_2.join()