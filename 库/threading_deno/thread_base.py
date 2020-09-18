
import threading
import time

esit_flag = 0

class MyThread(threading.Thread):
    def __init__(self, thread_id, thread_name, counter):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.thread_name = thread_name
        self.counter = counter

    def run(self):
        print('starting the tnread: {}'.format(self.thread_name))
        print_time(self.name, self.counter, 5)
        print(f'退出线程：{self.thread_name}')

def print_time(thread_name, delay, counter):
    while counter:
        if esit_flag:
            thread_name.exit()
        time.sleep(delay)
        print(f"{thread_name}, {time.ctime(time.time())}")
        counter -= 1
'''make new threads'''
thread1 = MyThread(1, 'thread-1', 1)
thread2 = MyThread(2, 'thread-2', 2)

'''starting new threads'''
thread1.start()
'''if thread1.join is here, thread2 run after the thread1 run'''
thread2.start()
'''if have no join, the main thread is execute before my_thread stoped'''
thread1.join()
thread2.join()
print('stop the thread')