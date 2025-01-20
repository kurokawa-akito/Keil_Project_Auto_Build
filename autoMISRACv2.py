import os

misra_script = r"D:\cppcheck\addons\misra.py"
directories = [
    r"path\of\code\you\want\to\scan",
    r"path\of\code\you\want\to\scan"
]
ruletext = r"D:\cppcheck\addons\test\misra\misra2012.txt"

for directory in directories:
    for filename in os.listdir(directory):
        if filename.endswith(".dump"):
            dump_file = os.path.join(directory, filename)
            # os.system(f"python {misra_script} --rule-texts='{ruletext}' {dump_file}")
            os.system(f"python {misra_script} {dump_file}")
