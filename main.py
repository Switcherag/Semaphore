from semaphore import Semaphore
import time
import matplotlib.pyplot as plt
import numpy as np
import _thread


def sampling(Semaphore,bufferSize = 256, sampling_period = 0.0016):
    
    #create a sine wave using time as the x-axis
    Y = bufferSize*[0]
    for i in range(bufferSize):
        #fill X with time in microseconds between 0 and 1_000_000
        time.sleep(sampling_period)
        usec = time.time()
        y = (usec - int(usec)) * 2 * 3.14159
        Y[i] = np.sin(y)
        
    Semaphore.Proberen(filtering,Semaphore, Y)
    Semaphore.Proberen(sampling,Semaphore, bufferSize, sampling_period)
    
    return None

def filtering(Semaphore, buffer):
    #emulate a diode
    for i in range(len(buffer)):
        if buffer[i] < 0:
            buffer[i] = 0
    
    Semaphore.Proberen(display_update,Semaphore,  buffer)
    
    return None

      
    
def display_update(Semaphore, buffer):
    
    plt.title("Thread count : " + str(_thread._count()) +" | Semaphore count : " + str(Semaphore.value) + " | Main thread active: " + str(active))
    global data
    #shift the data by the current buffer
    data = np.roll(data, -len(buffer))
    #add the new buffer to the end of the data
    data[-len(buffer):] = buffer
    line.set_ydata(data)

    plt.draw()
         
if __name__ == "__main__":

    MySemaphore = Semaphore(3)
    active = True
    MyBufferSize = 64
    MySamplingPeriod = 0.0016
    MyFrameNumber = 10
    display_init = False

    plt.ion()
    maxT = MySamplingPeriod * MyBufferSize * MyFrameNumber
    SamplesNumber = MyBufferSize * MyFrameNumber
    x = np.linspace(0, maxT, SamplesNumber)
    data = np.zeros(SamplesNumber)
    line, = plt.plot(x, data)
    plt.ylim(-1.5, 1.5)
    plt.show()


    #start the sampling thread
    MySemaphore.Proberen(sampling, MySemaphore, MyBufferSize, MySamplingPeriod)
    active = False

    plt.pause(40)
    plt.close()
