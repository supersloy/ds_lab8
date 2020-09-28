#Copypasted from provided in assgnment article
from multiprocessing import Process, Pipe
from os import getpid
from datetime import datetime
from time import sleep

def local_time(counter):
    return ' (LAMPORT_TIME={}, LOCAL_TIME={})'.format(counter,
                                                     datetime.now())
def event(pid, counter):
    counter[pid] += 1
    print('Something happened in {} !'.\
          format(pid) + local_time(counter))
    return counter

def send_message(pipe, pid, counter):
    counter[pid] += 1
    pipe.send(('Empty shell', counter))
    print('Message sent from ' + str(pid) + local_time(counter))
    return counter

def recv_message(pipe, pid, counter):
    message, timestamp = pipe.recv()
    counter = calc_recv_timestamp(timestamp, counter)
    print('Message received at ' + str(pid)  + local_time(counter))
    return counter

def calc_recv_timestamp(recv_time_stamp, counter):
    for id  in range(len(counter)):
        counter[id] = max(recv_time_stamp[id], counter[id])
    return counter

def process_a(pipe12):
    pid = 0
    counter = [0,0,0]
    #Make situation based on lab image
    counter = send_message(pipe12, pid, counter)#a0 - corresponding to image
    counter = send_message(pipe12, pid, counter)#a1
    counter = event(pid, counter)				#a2
    counter = recv_message(pipe12, pid, counter)#a3
    counter = event(pid, counter)				#a4
    counter = event(pid, counter)				#a5
    counter = recv_message(pipe12, pid, counter)#a6

    sleep(0.5)
    print(f"Process a: {counter}")

def process_b(pipe21, pipe23):
    pid = 1
    counter = [0,0,0]

    counter = recv_message(pipe21, pid, counter)#b0
    counter = recv_message(pipe21, pid, counter)#b1
    counter = send_message(pipe21, pid, counter)#b2
    counter = recv_message(pipe23, pid, counter)#b3
    counter = event(pid, counter)				#b4
    counter = send_message(pipe21, pid, counter)#b5
    counter = send_message(pipe23, pid, counter)#b6
    counter = send_message(pipe23, pid, counter)#b7

    sleep(0.75)
    print(f"Process b: {counter}")

def process_c(pipe32):
    pid = 2
    counter = [0,0,0]

    counter = send_message(pipe32, pid, counter)#c0
    counter = recv_message(pipe32, pid, counter)#c1
    counter = event(pid, counter)				#c2
    counter = recv_message(pipe32, pid, counter)#c3

    sleep(1)
    print(f"Process c: {counter}")


if __name__ == '__main__':
    oneandtwo, twoandone = Pipe()
    twoandthree, threeandtwo = Pipe()

    process1 = Process(target=process_a, 
                       args=(oneandtwo,))
    process2 = Process(target=process_b, 
                       args=(twoandone, twoandthree))
    process3 = Process(target=process_c, 
                       args=(threeandtwo,))

    process1.start()
    process2.start()
    process3.start()

    process1.join()
    process2.join()
    process3.join()