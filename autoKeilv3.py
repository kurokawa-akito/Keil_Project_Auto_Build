import subprocess
import os
import shutil
import sys
import re
from datetime import datetime
from autoEmailv2 import gitPullFailedEmail

keil_path = r"C:\Keil_v5\UV4\UV4.exe"
project_path = (
    r"path\of\*.uvprojx"
)

if len(sys.argv) > 1:
    current_time = sys.argv[1]
else:
    current_time = datetime.now().strftime("%Y-%m-%d_%H%M")

log_directory = "D:\\buildingLog\\"

hex_file_path = r"path\of\project's\hex\file"
hex_directory = "D:\\keilHex\\"


def getVersionValue(version_define_path, variable_name):
    pattern = rf"#define\s+{re.escape(variable_name)}\s+([^\s]+)" # exmple: #define FW_VERSION 1.04
    try:
        with open(version_define_path, "r") as file:
            for line in file:
                match = re.search(pattern, line)
                if match:
                    return match.group(1)
        print(f"No #define {variable_name}")
        return None
    except FileNotFoundError:
        print(f"File not found: {version_define_path}")
        return None


def copyHexFile(hexFilePath, hexDirectory):
    version_define_dir = (
        r"path\of\version\macro\header\file"
    )
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
        "-r",
        projectPath,
        "-o",
        logFile,
    ]
    result = subprocess.run(
        keilArgs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if result.returncode == 0:
        return result.returncode
    else:
        return result.stderr


def gitPull():
    git_repository_path = r"path\of\.git\path"
    try:
        fetch_result = subprocess.run(
            ["git", "fetch", "origin"],
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
            ["git", "pull"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=git_repository_path,
        )  # cwd = os.path.dirname(git_project_path) will direct to previous level directory
        # "git fetch origin", "git reset --hard origin/main", "git pull"
        if (
            (fetch_result.returncode == 0)
            and (reset_result.returncode == 0)
            and (pull_result.returncode == 0)
        ):
            print("Git pull successful")
        else:
            error_message = "Git pull failed with "
            if fetch_result.returncode != 0:
                error_message += f"Fetch error: {fetch_result.stderr}\n"
            if reset_result.returncode != 0:
                error_message += f"Reset error: {reset_result.stderr}\n"
            if pull_result.returncode != 0:
                error_message += f"Pull error: {pull_result.stderr}\n"
            print(error_message)

            smtp_server = "email server ip or DNS" 
            smtp_port = 25
            from_addr = "sender email"
            to_addr = ["receiver email"]
            gitPullFailedEmail(smtp_server, smtp_port, from_addr, to_addr)
    except Exception as e:
        print(f"Error during git pull: {e}")
        raise


if __name__ == "__main__":
    try:
        gitPull()

        version_define_dir = (
            r"path\of\version\macro\header\file"
        )
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
