import sys
import ui_mod as ui
import render_mod as render

class HEngine:
    def __init__(self, filename):
        self.filename = filename if filename.endswith(".py") else filename + ".py"
        self.buffer = []
        self.active = True

    def start(self):
        ui.clear()
        ui.header(self.filename)
        
        while self.active:
            line_num = len(self.buffer) + 1
            entry = ui.get_input(line_num)
            
            if entry.upper() == "SAVE":
                render.write_file(self.filename, self.buffer)
                ui.msg("SYSTEM: DATA_LOCKED_IN")
            elif entry.upper() == "EXIT":
                self.active = False
            else:
                self.buffer.append(entry)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "new_script.py"
    core = HEngine(target)
    core.start()

