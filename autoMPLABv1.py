import subprocess
import os

def compile_and_generate_hex(compiler_path, bin2hex_path, source_file, elf_file, hex_file, include_dirs, command_line, log_file):
    # 編譯命令
    gcc_command = [compiler_path]
    gcc_command += command_line
    gcc_command += [f'-I"{inc}"' for inc in include_dirs]
    gcc_command += ["-o", elf_file]
    gcc_command.append(source_file)

    # 執行編譯
    with open(log_file, "w") as log:
        process = subprocess.run(gcc_command, stdout=log, stderr=subprocess.STDOUT, text=True, shell=True)
    
    if process.returncode != 0:
        print(f"編譯失敗，請檢查日誌文件: {log_file}")
        return
    
    print("編譯成功，生成 ELF 文件！")
    
    # 轉換為 HEX 文件
    bin2hex_command = [bin2hex_path, elf_file]
    with open(log_file, "a") as log:  # 將轉換過程的輸出附加到同一日誌文件
        process = subprocess.run(bin2hex_command, stdout=log, stderr=subprocess.STDOUT, text=True)
    
    if process.returncode == 0:
        # 確保 HEX 文件生成在正確位置
        if os.path.exists(hex_file):
            os.rename(elf_file.replace(".elf", ".hex"), hex_file)
        print(f"HEX 文件生成成功！路徑: {hex_file}")
    else:
        print(f"轉換 HEX 文件失敗，請檢查日誌文件: {log_file}")

# 配置
compiler = r"C:\Program Files\Microchip\xc32\v4.45\bin\xc32-gcc"
bin2hex = r"C:\Program Files\Microchip\xc32\v4.45\bin\xc32-bin2hex"
source_file = r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\main.c"
elf_file = r"D:\spg_ta010_asymm_auth_genkey.elf"
hex_file = r"D:\spg_ta010_asymm_auth_genkey.hex"
include_dirs = [
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\config\default"
]
command_line = [
    "-g", 
    "-x", "c",
    "-c",
    "-mprocessor=ATSAMD21E18A",
    "-ffunction-sections", "-fdata-sections", "-O1", "-fno-common",
    '-I"../src"',
    '-I"../src/config/default"',
    '-I"../src/config/default/library/cryptoauthlib"',
    '-I"../src/config/default/library/cryptoauthlib/crypto"',
    '-I"../src/config/default/library/cryptoauthlib/pkcs11"',
    '-I"../src/config/default/library/cryptoauthlib/tng"',
    '-I"../src/packs/ATSAMD21E18A_DFP"',
    '-I"../src/packs/CMSIS/"',
    '-I"../src/packs/CMSIS/CMSIS/Core/Include"', 
    "-Werror", "-Wall",
]

log_file = r"D:\buildLog.txt"

# 執行
compile_and_generate_hex(compiler, bin2hex, source_file, elf_file, hex_file, include_dirs, command_line, log_file)
