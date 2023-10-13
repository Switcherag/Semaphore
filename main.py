from semaphore import Semaphore
import time
import matplotlib.pyplot as plt
import numpy as np


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

def filtering(Semaphore, buffer, v = 0.006):
    #emulate a diode
    for i in range(len(buffer)):
        if buffer[i] < 0:
            buffer[i] = 0
    
    #emulate capacitor to load the compute time
    for j in range(1,len(buffer)):
        diff = buffer[j] - buffer[j-1]
        abs = np.abs(diff)
        if - diff > v:
            buffer[j] = buffer[j-1] - v

    Semaphore.Proberen(display_update,Semaphore,  buffer)
    
    return None

      
    
def display_update(Semaphore, buffer):
    
    plt.title("Thread mean : " + str(round(Semaphore.thread_sum/Semaphore.pass_count,3)) +" | Semaphore mean count : " + str(round(process_number - Semaphore.value_sum/Semaphore.pass_count,3)) + " | Main thread active: " + str(active))

    global data
    #shift the data by the current buffer
    data = np.roll(data, -len(buffer))
    #add the new buffer to the end of the data
    data[-len(buffer):] = buffer
    line.set_ydata(data)

    plt.draw()

         
if __name__ == "__main__":

    process_number = 2 #number of max processes to run
    MySemaphore = Semaphore(process_number)
    active = True #main thread active
    MyBufferSize = 128 #number of samples to take
    MySamplingPeriod = 0.0016 #sampling period in seconds
    MyFrameNumber = 10 #number of frames to display
    display_init = False #display has been initialized

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
