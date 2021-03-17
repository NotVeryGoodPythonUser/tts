import os
import re

all_resources = os.listdir(os.path.join(os.path.dirname(os.getcwd()), "diphone_resources/"))
for file_name in all_resources:
    if re.match(r"[A-z-áčČďéíňóřŘšťúž_]{2}-\d+\.wav", file_name):
        os.remove(file_name)
