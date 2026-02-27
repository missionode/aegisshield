import os
import sys

# Hack to import slm_av
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from slm_av import quarantine_file

file_path = "quarantine_test.php"
with open(file_path, "w") as f:
    f.write("<?php system($_GET['cmd']); ?>")

print("Testing quarantine_file...")
res = quarantine_file("/Users/syamnath/Desktop/Projects/Plantdoctor/aegisshield", file_path, "MALICIOUS")
print("Result:", res)
