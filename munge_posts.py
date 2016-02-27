import json
import app
# from time import strftime

dat = app.post_list
for post in dat:
    datetime_obj = post['date']
    post['month'] = datetime_obj.month
    post['day'] = datetime_obj.day
    post['year'] = datetime_obj.year
    del post['date']
    del post['template']
    post['route'] = '//residentmar.io/' + post['route']

# print(dat)

with open('./static/json/post_list.json', 'w') as outfile:
    json.dump(dat, outfile, indent=4)