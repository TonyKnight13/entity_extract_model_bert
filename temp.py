import re
import json

# result = re.search('、','辩护人王唐成、马静、沙发').span()
# print(result.group(0))
path = '新判决书2.json'
with open(path, "rb") as f:
        text = f.read()
        json_str = json.loads(text)
        print(json_str)


