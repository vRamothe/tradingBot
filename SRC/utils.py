import threading

def threaded(fn):
    def wrapper(*args, **kwargs):
        threading.Thread(target=fn, args=args, kwargs=kwargs).start()
    return wrapper

if __name__ == "__main__":
    print("This is a utility module and is not meant to be run directly.")
    