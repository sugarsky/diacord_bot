import json
from pprint import pprint as pp
from emoji import emojize, demojize

# dict = {
    # 'name': "❤"
# }

# with open('cats.json', 'w') as f:
#     json.dump(dict, f, ensure_ascii=True, indent=2)

# with open('cats.json', 'r') as f:
#     ups = json.load(f)

# pp(ups)

# print(emoji.emojize(':red_heart:', variant="text_type"))
# print(emoji.demojize('❤'))

# x = {
#   "loved": ":red_heart:"
# }
# # del(x["loved"])
# for id in x.keys() and name in x.values():
#     print(id + name)

print(emojize(demojize(emojize(demojize("📸-photos"), variant='text_type')), variant='emoji_type'))
