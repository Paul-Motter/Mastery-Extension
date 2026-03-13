from pynput.keyboard import Key
import time;

class keyboardRecorder:

    def __init__(self):
        self.inputStr: list[str] = []
        self.record: list[dict[str]] = []
        self.done = False

    def on_press(self, key: Key):
        try:
            # add key to record
            if (key == Key.backspace):
                if (len(self.record) > 0):
                    self.record.pop()
                if (len(self.record) > 0):
                    self.record[-1]["press"] = float(time.perf_counter_ns())/1.0e9
            elif (key != Key.shift):
                self.record.append({
                    "key": key,
                    "press": float(time.perf_counter_ns())/1.0e9,
                })    
            # add key to resultant string
            if (key == Key.space):
                self.inputStr.append(" ")
            elif (key == Key.enter):
                self.inputStr.append("\n")
            elif (key == Key.backspace):
                if (len(self.inputStr)>0):
                    self.inputStr.pop()
            elif(key != Key.shift and key != Key.enter):
                self.inputStr.append(key.char)
            print("\r"+" "*50, end="", flush=True)
            print("\r" + "".join(self.inputStr), end="", flush=True)

        except AttributeError:
            pass

    def on_release(self, key):
        # find last time the key was pressed and add when it was released. 
        match = False
        for i in range(len(self.record)-1, -1, -1):
            try:
            # checks specific key for specials like enter, tab, backspace.
            # if the exact entry doesn't exist it tries to match for lowercase (press "L", release shift, release "L" gives key "l")
            # raises AttributeError for keys whose record is not kept.
                if (self.record[i]["key"] == key or
                    self.record[i]["key"].char.lower() == key.char.lower()
                    ):
                    self.record[i]["release"] = float(time.perf_counter_ns())/1.0e9
                    match = True
                    break
            except AttributeError:
                pass
        if (key == Key.enter and match == True):
            self.done = True
        