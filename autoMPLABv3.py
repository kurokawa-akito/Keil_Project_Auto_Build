import subprocess

compiler = r"C:\Program Files\Microchip\xc32\v4.45\bin\xc32-gcc.exe"
source_file = r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\main.c"
elf_file = r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\output.elf"
hex_file = r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\spg_ta010_asymm_auth_genkey.hex"

include_dirs = [
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\config\default\definitions.h",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\config\default\library\cryptoauthlib",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\packs\ATSAMD21E18A_DFP",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\packs\CMSIS",
    r"D:\spg_ta010_asymm_auth_genkey\spg_ta010_asymm_auth\firmware\asymm_auth_firmware\src\packs\CMSIS\CMSIS\Core\Include",
]

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
    *[f'-I"{inc}"' for inc in include_dirs],
]

command = [
    compiler,
    *flags,
    "-o", elf_file,
    source_file,
]

log_file = r"D:\buildLog.txt"
with open(log_file, "w") as log:
    process = subprocess.run(command, stdout=log, stderr=log, text=True, shell = True)

if process.returncode == 0:
    print("compile success")
else:
    print("compile failed，請檢查 log 文件中的錯誤訊息。")
