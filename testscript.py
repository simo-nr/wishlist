from flask import json


temp_new_item_json = {'id': None, 'user_id': None, 'name': None, 'image_link': None, 'url': 'qmsdjf', 'checked_off': None, 'notes': None}


print(f'in add, temp new item json: {temp_new_item_json}')
print(f'type of json thing: {type(temp_new_item_json)}')

temp_new_item_json_str = json.dumps(temp_new_item_json)

print(f'new stuff: {temp_new_item_json_str}')

temp_new_item_dict = json.loads(temp_new_item_json_str)

print(f'latest stuff: {temp_new_item_dict}')