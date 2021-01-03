import os
import re

for file_name in os.listdir():
    if re.match(r"[A-z-áčČďéíňóřŘšťúž_]{2}-\d+\.wav", file_name):
        os.remove(file_name)