import schedule
import time
import subprocess
from autoEmail import sendEmailWithFiles
from autoKeil import getVersionValue
from datetime import datetime

smtp_server = "email server ip or DNS"
smtp_port = 25
from_addr = "sender email"
to_addr = ["receiver email"]


def job():
    try:
        current_time = datetime.now().strftime("%Y-%m-%d_%H%M")
        result = subprocess.run(["python", "autoKeilv3.py", current_time], check=True)
        # to get the latest version
        version_define_dir = (
            r"path\of\version\macro\header\file"
        )
        variable_name = "FW_VERSION"
        value = getVersionValue(version_define_dir, variable_name)
        if result.returncode == 0:
            hex_file_path = f"D:\\keilHex\\Release_{current_time}_{value}.hex"
            log_file_path = f"D:\\buildingLog\\buildLog_{current_time}_{value}.txt"
            sendEmailWithFiles(
                smtp_server, smtp_port, from_addr, to_addr, hex_file_path, log_file_path
            )

    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running autoKeilv3.py: {e}")
    except Exception as e:
        print(f"Schedule fatal error: {e}")


if __name__ == "__main__":
    # schedule.every().day.at("08:00").do(job)
    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(10)
