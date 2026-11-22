"""Add one app; its icon is traced by math from the app's own icon PNG.

  python tools/new_icon.py "App Name" com.package/com.package.MainActivity icon.png
"""
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
if len(sys.argv) not in (3, 4) or "/" not in sys.argv[2]:
    sys.exit(__doc__)
line = f"{sys.argv[1]} | {sys.argv[2]}"
if len(sys.argv) == 4:
    line += f" | img={os.path.abspath(sys.argv[3])}"
with open(os.path.join(here, "requests.txt"), "a", encoding="utf-8") as f:
    f.write(line + "\n")
subprocess.run([sys.executable, os.path.join(here, "generate.py")], check=True)
