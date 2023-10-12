import _thread
import time

# Function for the thread
def my_thread_function():
    print("Thread is starting...")
    time.sleep(3)
    print("Thread is exiting...")

# Start a new thread
_thread.start_new_thread(my_thread_function, ())

# Main thread continues its execution
for i in range(5):
    print(f"Main thread: Count {i}")
    time.sleep(1)

print("Main thread is done.")
