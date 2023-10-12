#class Semaphore
import _thread

class Semaphore:
    def __init__(self, initial):
        self.lock = _thread.allocate_lock()
        self.value = initial
        self.queue = []

    def Proberen(self, process, *args):
        self.lock.acquire()
        if (self.value <= 0):
            self.lock.release()
            self.queue.append((process, *args))
            if len(self.queue) > 20:
                print("Le programme court derrière")
        else:
            self.value -= 1
            self.lock.release()
            
            try:
                _thread.start_new_thread(self._wrapper, (process, args))           
            except Exception as e:
                print("Error: unable to start thread")
                print(e)
                self.Verhogen()
    def Verhogen(self):
        self.lock.acquire()
        if (len(self.queue) > 0):
            process, *args = self.queue.pop(0)
            self.value -= 1
            self.lock.release()
            _thread.start_new_thread(self._wrapper, (process, args))

        else:
            self.value += 1
            self.lock.release()
    
    def _wrapper(self, process, args):
        
        process(*args)
        self.Verhogen()
