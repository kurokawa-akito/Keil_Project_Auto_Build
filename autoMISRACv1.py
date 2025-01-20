import os

misra_script = r"D:\cppcheck\addons\misra.py"
Framework_directory = r"path\of\code\you\want\to\scan"
ModesAndConfig_directory = r"path\of\code\you\want\to\scan"
ruletext = r"D:\cppcheck\addons\test\misra\misra2012.txt"

for filename in os.listdir(Framework_directory):
    if filename.endswith(".dump"):
        dump_file = os.path.join(Framework_directory, filename)
        os.system(f"python {misra_script} --rule-texts='{ruletext}' {dump_file}")

for filename in os.listdir(ModesAndConfig_directory):
    if filename.endswith(".dump"):
        dump_file = os.path.join(ModesAndConfig_directory, filename)
        os.system(f"python {misra_script} --rule-texts='{ruletext}' {dump_file}")