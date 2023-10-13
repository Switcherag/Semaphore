#class Semaphore
import _thread

class Semaphore:
    def __init__(self, initial):
        self.lock = _thread.allocate_lock()
        self.value = initial
        self.queue = []
        self.value_sum = 0
        self.thread_sum = 0
        self.pass_count = 0

    def Proberen(self, process, *args):
        self.lock.acquire()
        self.value_sum += self.value
        self.thread_sum += _thread._count()
        self.pass_count += 1

        if (self.value <= 0):
            self.lock.release()
            self.queue.append((process, *args))
            if len(self.queue) > 20:
                print("Le programme court derrière")
        else:            
            self.value -= 1
            self.lock.release()  
            _thread.start_new_thread(self._wrapper, (process, args))           

    def Verhogen(self):
        self.lock.acquire()

        self.value_sum += self.value
        self.thread_sum += _thread._count()
        self.pass_count += 1
        
        if (len(self.queue) > 0):
            process, *args = self.queue.pop(0)
            self.lock.release()
            _thread.start_new_thread(self._wrapper, (process, args))
        else:       
            self.value += 1
            self.lock.release()
    
    def _wrapper(self, process, args):
        process(*args)        
        self.Verhogen()
        _thread.exit()
        
