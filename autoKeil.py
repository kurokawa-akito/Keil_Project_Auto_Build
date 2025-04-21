import subprocess
import os
import shutil
import sys
import re
from datetime import datetime
from autoEmail import gitPullFailedEmail

keil_path = r"C:\MDK\UV4\UV4.exe"
project_path = r"path\to\your\file\or\project\*.uvprojx"

if len(sys.argv) > 1:
    current_time = sys.argv[1]
    # git_tag = sys.argv[1]
    # current_time = datetime.now().strftime("%Y-%m-%d_%H%M")
else:
    current_time = datetime.now().strftime("%Y-%m-%d_%H%M")
    git_tag = None

log_directory = "C:\\buildingLog\\"

hex_file_path = r"path\to\your\file\or\project"
hex_directory = "C:\\keilHex\\"


def getVersionValue(version_define_path, variable_name):
    pattern = rf"#define\s+{re.escape(variable_name)}\s+([^\s]+)"
    try:
        with open(version_define_path, 'r') as file:
            for line in file:
                match = re.search(pattern, line)
                if match:
                    return match.group(1)  # 回傳找到的變數值
        print(f"No #define {variable_name}")
        return None
    except FileNotFoundError:
        print(f"File not found: {version_define_path}")
        return None

def copyHexFile(hexFilePath, hexDirectory):
    version_define_dir = r"path\to\your\file\or\project\main.h"
    variable_name = "FW_VERSION"
    value = getVersionValue(version_define_dir, variable_name)

    newFileName = f"Release_{current_time}_{value}.hex"
    newFilePath = os.path.join(hexDirectory, newFileName)

    if os.path.exists(hexFilePath):
        shutil.copy(hexFilePath, newFilePath)
    else:
        print(f"Hex file not found: {hexFilePath}")

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
    

def gitPull():
    git_repository_path = r"path\to\your\file\or\project"
    try:
        fetch_result = subprocess.run(
            ["git", "fetch", "--all", "--tags"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=git_repository_path,
        )
        checkout_result = subprocess.run(
            ["git", "checkout", "main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=git_repository_path,
        )
        reset_result = subprocess.run(
            ["git", "reset", "--hard", "origin/main"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=git_repository_path,
        )
        pull_result = subprocess.run(
            ["git", "pull", "--ff-only"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=git_repository_path,
        )
        # cwd = os.path.dirname(git_project_path) will direct to previous level directory
        if git_tag != None:
            checkout_result = subprocess.run(
                ["git", "checkout", git_tag],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=git_repository_path,
            )

        if (
            (fetch_result.returncode == 0)
            and (reset_result.returncode == 0)
            and (pull_result.returncode == 0)
            and (checkout_result.returncode == 0)
        ):
            print("git pull successful")
            status = 0
        else:
            error_message = "git "
            if fetch_result.returncode != 0:
                error_message += f"fetch {fetch_result.stderr}\n"
            if reset_result.returncode != 0:
                error_message += f"reset {reset_result.stderr}\n"
            if pull_result.returncode != 0:
                error_message += f"pull {pull_result.stderr}\n"
            if checkout_result.returncode != 0:
                error_message += f"checkout {checkout_result.stderr}\n"
            print(error_message)
            status = 1

            smtp_server = "email server"
            smtp_port = 25
            from_addr = "email sender"
            to_addr = ["email receiver"]
            gitPullFailedEmail(smtp_server, smtp_port, from_addr, to_addr, error_message)
        return status
    except Exception as e:
        print(f"Error during git pull: {e}")
        raise


if __name__ == "__main__":
    try:
        git_result = gitPull()
        if git_result == 1:
            sys.exit(1)

        version_define_dir = r"path\to\your\file\or\project\main.h"
        variable_name = "FW_VERSION"
        value = getVersionValue(version_define_dir, variable_name)
        log_file = f"buildLog_{current_time}_{value}.txt"
        log_file_path = os.path.join(log_directory, log_file)

        with open(log_file_path, "w") as file:
            print("compiling...")
            compileResult = keilCompile(keil_path, project_path, log_file_path)
        
        if compileResult == 0:
            print("compiling success")
            copyHexFile(hex_file_path, hex_directory)
        else:
            print(f"compiling failed: {compileResult}")
    except Exception as e:
        print(f"fatal error: {e}")
