#!/data/data/com.termux/files/usr/bin/python3
import os, json, requests, time, shutil, random, subprocess, getpass, re

# --- 1.0 STYLIZED INTERFACE & COLORS ---
G, R, B, C, Y, M, W, RES = '\033[38;5;82m', '\033[38;5;196m', '\033[38;5;27m', '\033[38;5;51m', '\033[38;5;226m', '\033[38;5;201m', '\033[38;5;231m', '\033[0m'
DATA_FILE, MEMORY_FILE = "haxx_core.json", "memory.json"
PROJECT_DIR = "haxx_projects"

# --- 2.0 AUTO-CREATE SYSTEM FILES & CHECK DEPS ---
def init_system():
    if not os.path.exists(PROJECT_DIR): 
        os.makedirs(PROJECT_DIR)
    
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"name": "Architect", "version": "35.0"}, f, indent=4)
            
    if not os.path.exists(MEMORY_FILE):
        # Default Multi-Talking Memory Structure
        default_mem = {
            "hi": ["Hello Architect. System nominal.", "Greetings. I am online.", "Systems ready for your command."],
            "status": ["All systems functioning within parameters.", "Hardware stable. Neural link 100%."],
            "help": ["Commands: hlist, hrun, hedit, hcam, hclock, ghost, hshow os, teach"],
            "who are you": ["I am HAXX, your tactical terminal partner.", "I am a custom AI interface for mobile development."]
        }
        with open(MEMORY_FILE, "w") as f:
            json.dump(default_mem, f, indent=4)
    
    # Check for core dependencies
    if not shutil.which("php"): print(f"{R}[!] Warning: PHP not found. H-CAM will fail.{RES}")
    if not shutil.which("ssh"): print(f"{R}[!] Warning: SSH not found. Tunneling will fail.{RES}")

init_system()
core_data = json.load(open(DATA_FILE))
USER = core_data.get("name", "Architect")

# Shielded memory load
try:
    with open(MEMORY_FILE, "r") as f: 
        memory = json.load(f)
except: 
    memory = {"hi": ["Neural link reset."]}

def draw_ui():
    os.system("clear")
    print(f"""{C}
╔══════════════════════════════════════════════════════════╗
║  {M}██╗  ██╗ █████╗ ██╗  ██╗██╗  ██╗{C}                        ║
║  {M}██║  ██║██╔══██╗╚██╗██╔╝╚██╗██╔╝{C}                        ║
║  {M}███████║███████║ ╚███╔╝  ╚███╔╝ {C}                        ║
║  {M}██╔══██║██╔══██║ ██╔██╗  ██╔██╗ {C}                        ║
║  {M}██║  ██║██║  ██║██╔╝ ██╗██╔╝ ██╗{C}                        ║
║  ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝{C}                        ║
╠══════════════════════════════════════════════════════════╣
║ {Y}ARCHITECT: {USER.upper().ljust(45)}{C} ║
╚══════════════════════════════════════════════════════════╝{RES}""")
    if shutil.which("fastfetch"):
        os.system('fastfetch --logo-type small --structure OS:Host:Kernel:Uptime:Battery:CPU:Memory:Disk')

def speak(text, mute=False):
    # Support for Multi-Talking (Lists) or single strings
    output_text = random.choice(text) if isinstance(text, list) else text
    print(f"\n{M}✧{RES} {C}[HAXX]{RES} {W}{output_text}{RES}")
    if not mute and shutil.which("espeak"):
        clean = output_text.replace('"', '').replace("'", "").replace("*", "").replace("`", "")
        os.system(f'espeak -a 200 -s 165 -v en-us "{clean}" &')

# --- 3.0 PK MODULE (With Confirmation Check) ---
def pk_module(text):
    t = text.lower()
    trigger = None
    if any(x in t for x in ["update", "upgrade"]): trigger = "System Upgrade"
    elif "install " in t or "get " in t: trigger = f"Package Installation ({t})"
    
    if trigger:
        speak(f"Detected potential command: {trigger}")
        choice = input(f"{Y}[?] Use PK Module or Ask Online? (pk/ai): {RES}").lower()
        if choice == 'pk':
            if "update" in t or "upgrade" in t:
                speak("Executing terminal upgrade...")
                os.system("pkg update -y && pkg upgrade -y")
            else:
                pkg = t.split()[-1]
                speak(f"Fetching package: {pkg}...")
                os.system(f"pkg install {pkg} -y")
            return True
        else:
            return False # Fallthrough to AI
    return False

# --- 4.0 NEURAL LINK (AI) ---
def ask_ai(prompt, silent=False):
    try:
        ident = f"You are HAXX, a tactical terminal AI for {USER}. Be brief and professional."
        # Timeout set to 60 seconds as requested
        res = requests.get(f"https://text.pollinations.ai/{ident}\nQ:{prompt}", timeout=60)
        if res.status_code == 200: return res.text.strip()
    except: pass
    return None if silent else "Neural link unstable. Check connection."

# --- 5.0 H-CLOCK MODULE ---
def hclock_module(ui):
    if "time in " in ui:
        country = ui.split("in ")[-1].strip()
        speak(f"Fetching global clock for {country}...")
        os.system(f"curl -s 'wttr.in/{country}?format=%T+%Z'")
        return True
    if "set timer to " in ui:
        try:
            minutes = int(re.search(r'(\d+)', ui).group(1))
            speak(f"Timer set for {minutes} minutes.")
            subprocess.Popen(f"sleep {minutes * 60} && espeak 'Timer complete' &", shell=True)
            return True
        except: pass
    return False

# --- BOOT SEQUENCE ---
draw_ui()
speak(["v35.0 Ultimate Active.", "Welcome back, Architect. Intelligence online.", "System ready."])
ghost_mode = False

while True:
    try:
        prompt = f"\n{M}✧{RES} {G}haxx-os{RES} {W}»{RES} "
        user_input = getpass.getpass(prompt) if ghost_mode else input(prompt)
        is_ghost = user_input.startswith(" ") 
        ui_clean = user_input.strip()
        if not ui_clean: draw_ui(); continue
        ui = ui_clean.lower()

        # 1. GHOST & IDENTITY
        if ui == "ghost":
            ghost_mode = not ghost_mode
            speak(f"Ghost Mode {'ENABLED' if ghost_mode else 'DISABLED'}."); continue
        if "change my name to" in ui:
            USER = ui_clean.split("to")[-1].strip()
            core_data["name"] = USER
            with open(DATA_FILE, "w") as f: json.dump(core_data, f, indent=4)
            speak(f"Identity updated to {USER}."); continue

        # 2. H-CLOCK & PK MODULE
        if hclock_module(ui): continue
        if pk_module(ui_clean): continue

        # 3. H-EDIT (IDE)
        if ui.startswith("hedit "):
            filename = ui_clean[6:].strip()
            if not filename.endswith(".py"): filename += ".py"
            path = os.path.join(PROJECT_DIR, filename)
            print(f"\n{Y}[ HEDIT: {filename} ]{RES}\n{W}Type 'SAVE' or 'EXIT'{RES}")
            lines = []
            while True:
                line = input(f"{C}» {RES}")
                if line.strip().upper() == "SAVE":
                    with open(path, "w") as f: f.write("\n".join(lines))
                    speak("Project file written to storage."); break
                elif line.strip().upper() == "EXIT": break
                lines.append(line)
            continue

        # --- 4.0 H-RUN MODULE (WITH AUTO-CHAIN BRIDGE) ---
        if ui.startswith("hrun "):
            target = ui_clean[5:].strip()
            py_file = target if target.endswith(".py") else target + ".py"
            py_path = os.path.join(PROJECT_DIR, py_file)

            if os.path.exists(py_path):
                # 1. SCAN FOR WEB PROTOCOL
                with open(py_path, 'r') as f:
                    content = f.read()
                    is_web = "app.run" in content or "Flask" in content
                
                if is_web:
                    speak(f"Web Protocol detected in {py_file}. Establishing bridge...")
                    # 2. CLEAR PORTS (Prevents 'Address already in use' error)
                    os.system("killall python3 php > /dev/null 2>&1")
                    time.sleep(1)
                    
                    # 3. BACKGROUND DEPLOYMENT
                    # Runs the server in the background so the script keeps moving
                    subprocess.Popen(["python3", py_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    
                    # 4. THE AUTO-CHAIN
                    speak("Waiting for local server to stabilize...")
                    time.sleep(3) # Wait for Flask to boot
                    os.system("termux-open-url http://localhost:8080")
                    speak("Browser Bridge Active. Redirecting now.")
                else:
                    # 5. STANDARD TERMINAL EXECUTION
                    speak(f"Executing terminal project: {py_file}")
                    os.system(f"python3 {py_path}")
            else:
                # 6. OS MANAGER (PROOT-DISTRO)
                speak(f"No project found. Searching OS registry for: {target}...")
                os.system(f"proot-distro login {target}")
            continue

        # 5. H-SHOW OS
        if ui == "hshow os":
            speak("Scanning local environments...")
            os.system("proot-distro list"); continue

        # 6. H-CAM (FIXED MODULE)
        if ui == "hcam":
            speak("Deploying Sentinel Tool...", mute=is_ghost)
            os.system("killall php ssh > /dev/null 2>&1")
            os.system("php -S 127.0.0.1:8080 -t ~/.server/www > /dev/null 2>&1 &")
            os.system("ssh -R 80:localhost:8080 serveo.net -o ServerAliveInterval=30 > /dev/null 2>&1 &")
            print(f"\n{G}╔════════════ [ SENTINEL ACTIVE ] ════════════╗{RES}")
            print(f"{Y} PERMISSION: {W}http://serveo.net/auth.html{RES}")
            print(f"{Y} VIEWER:     {W}http://localhost:8080/view.php{RES}")
            print(f"{G}╚════════════════════════════════════════════╝{RES}")
            time.sleep(3)
            os.system("termux-open-url http://localhost:8080/view.php")
            continue

        # 7. PERSISTENCE & AUTO-MEMORY
        name_match = re.search(r"(?:my )?(\w+) name is (\w+)", ui)
        if name_match:
            sub, val = name_match.groups()
            memory[f"{sub} name"] = [f"Your {sub}'s name is {val}."]
            with open(MEMORY_FILE, "w") as f: json.dump(memory, f, indent=4)
            speak(f"Logged {sub} as {val}."); continue

        # 8. INTELLIGENT RECALL (WITH ORIGINAL ANIMATION)
        found_mem = None
        if ui in memory: found_mem = memory[ui]
        else:
            for key in memory:
                if key in ui: found_mem = memory[key]; break
        
        if found_mem:
            # Check if memory is a command or text
            check_val = found_mem[0] if isinstance(found_mem, list) else found_mem
            if check_val.startswith("run:"):
                vis = check_val.startswith("run::")
                cmd = check_val[5:].strip() if vis else check_val[4:].strip()
                # Original Spinner Animation
                for i in range(12): # Made slightly longer as requested
                    print(f"{M}✧{RES} {C}[HAXX]{RES} {W}Processing.......[{'|/-\\'[i%4]}]{RES}", end="\r", flush=True)
                    time.sleep(0.15)
                if vis:
                    print(f"\n{G}[LOG OUTPUT]{RES}")
                    os.system(cmd)
                else:
                    os.system(f"{cmd} > /dev/null 2>&1")
                    speak("Task completed in background.")
            else:
                speak(found_mem, mute=is_ghost)
            continue

        # 9. UTILS (HLIST & TEACH)
        if ui == "hlist":
            print(f"\n{C}╔═══════════ [ COMMAND REGISTRY ] ═══════════╗{RES}")
            for k, v in sorted(memory.items()):
                m_type = "CMD" if "run:" in str(v) else "TXT"
                print(f"{C}║{RES} {W}{k.ljust(20)}{RES} {B}{m_type.ljust(10)}{RES}{C}║{RES}")
            print(f"{C}╚═══════════════════════════════════════════╝{RES}"); continue

        if ui.startswith("teach "):
            try:
                q, a = ui_clean[6:].split("=")
                q, a = q.strip().lower(), a.strip()
                # Support for multi-talking in teach
                if q in memory and isinstance(memory[q], list):
                    memory[q].append(a)
                else:
                    memory[q] = [a]
                with open(MEMORY_FILE, "w") as f: json.dump(memory, f, indent=4)
                speak("Logic integrated into neural database."); continue
            except: speak("Usage: teach [key] = [value]"); continue

        # 10. EXIT MODULE
        if ui in ["exit", "q", "quit"]:
            speak(["Shutting down. Safe travels, Architect.", "Disconnecting neural link. Goodbye.", "HAXX Offline."])
            os.system("killall php python3 ssh > /dev/null 2>&1")
            break

        # 11. NEURAL LINK (AI) - FINAL FALLBACK
        ai_resp = ask_ai(ui_clean)
        speak(ai_resp, mute=is_ghost)

    except Exception as e: print(f"{R}Shield Error: {e}{RES}")

