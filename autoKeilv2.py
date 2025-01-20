import subprocess

keil_path = r"C:\Keil_v5\UV4\UV4.exe"
project_path = r"path\of\*.uvprojx"
log_file = r"D:\buildLog.txt"

def keilCompile(keilExePath, projectPath, logFile):
    keilArgs = [
        keilExePath,
        "-r", projectPath,  
        "-o", logFile,      
    ]
    result = subprocess.run(keilArgs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode == 0:
        return result.returncode
    else:
        return result.stderr

if __name__ == "__main__":
    try:
        print("compiling...")
        compileResult = keilCompile(keil_path, project_path, log_file)
        
        if compileResult == 0:
            print("compiling success!")
        else:
            print(f"compiling failed: {compileResult}")
    except Exception as e:
        print(f"fatal error: {e}")
