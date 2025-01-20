import subprocess

# 編譯器與目標設定
compiler = r"C:\Program Files\Microchip\xc32\v4.45\bin\xc32-gcc.exe"
source_file = r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\main.c"
elf_file = r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\output.elf"
hex_file = r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\spg_ta010_asymm_auth_genkey.hex"

# 包含路徑
include_dirs = [
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\config\default\definitions.h",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\config\default\library\cryptoauthlib",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\packs\ATSAMD21E18A_DFP",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\packs\CMSIS",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\packs\CMSIS\CMSIS\Core\Include",
]

# 生成編譯標誌
flags = [
    "-g",
    "-x", "c",
    "-c",
    "-mprocessor=ATSAMD21E18A",
    "-ffunction-sections",
    "-fdata-sections",
    "-O1",
    "-fno-common",
    "-Werror",
    "-Wall",
    *[f'-I"{inc}"' for inc in include_dirs],  # 添加包含路徑
]

# 執行編譯命令
command = [
    compiler,
    *flags,
    "-o", elf_file,
    source_file,
]

# 記錄到log檔案
log_file = r"D:\buildLog.txt"
with open(log_file, "w") as log:
    process = subprocess.run(command, stdout=log, stderr=log, text=True, shell = True)

# 檢查是否成功
if process.returncode == 0:
    print("編譯成功！")
else:
    print("編譯失敗，請檢查 log 文件中的錯誤訊息。")
