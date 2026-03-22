import os

# This is the EXACT absolute path for Termux
PROJECT_DIR = "/data/data/com.termux/files/home/Haxx/haxx_projects"

def write_file(name, data):
    try:
        # 1. Force create the directory if it's missing
        if not os.path.exists(PROJECT_DIR):
            os.makedirs(PROJECT_DIR, exist_ok=True)
            
        # 2. Build the full path
        full_path = os.path.join(PROJECT_DIR, name.strip())
        
        # 3. Write the file
        with open(full_path, "w") as f:
            f.write("\n".join(data))
            
        # 4. Success Message with the actual path
        print(f"\033[92m[RENDER] SUCCESS: Created {full_path}\033[0m")
        return True
        
    except Exception as e:
        print(f"\033[91m[RENDER_ERR] Critical Failure: {e}\033[0m")
        return False

