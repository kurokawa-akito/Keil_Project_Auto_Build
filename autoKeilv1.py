import subprocess

keil_path = r"C:\Keil_v5\UV4\UV4.exe"
project_path = r"path\of\*.uvprojx"
log_file = r"D:\buildLog.txt"

keil_args = [
    keil_path,
    "-r", project_path,  
    "-o", log_file,      
]

try:
    print("compiling...")
    process = subprocess.run(keil_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    if process.returncode == 0:
        print("compiling success!")
    else:
        print("compiling failed.")
        print("output:", process.stdout)
        print("error:", process.stderr)
except Exception as e:
    print(f"fatal error: {e}")
