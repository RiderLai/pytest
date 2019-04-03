# import os
#
#
# def child_process():
#     print("We are in Child_Process")
#     print("My PID: %d" % os.getpid())
#     print("Child_Process is exiting")
#
#
# def parent_process():
#     print("-------Parent_process---------")
#     wpid = os.fork()
#     if wpid == 0:
#         print("wpid is 0 means We are in Child_process")
#         print("Child :%d" % wpid)
#         child_process()
#     else:
#         print("Execute Parent_process")
#         print("Parent_process %d" % wpid)
#         parent_process()
#
#
# parent_process()


# import os
# pid = os.fork()
# print(pid)


import os
import time

NUM_PROCESSES = 7


def timeConsumingFunction():
    x = 1
    for n in range(10000000):
        x += 1


children = []
start_time = time.time()
for process in range(NUM_PROCESSES):
    pid = os.fork()
    if pid:
        children.append(pid)
        print(pid)
    else:
        timeConsumingFunction()
        os._exit(0)
for i, child in enumerate(children):
    os.waitpid(child, 0)
print(time.time() - start_time)
