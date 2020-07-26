import requests
import json

url = "https://api.bilibili.com/x/web-interface/search/all/v2?context=&page=1&order=&keyword=约会大作战" \
      "&duration=&tids_1=&tids_2=&__refresh__=true&__reload__=false&_extra=&highlight=1&single_column=0&jsonp" \
      "=jsonp&callback=__jp1 "

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/84.0.4147.89 Safari/537.36",
    'Referer': "https://search.bilibili.com"
}
res = requests.get(url, headers=headers)

# print(res.text)

data = json.loads(res.text[7:len(res.text)-1])
print(data)
for j,i in enumerate(data['data']['result'][8]['data']):
    print(i['title'], i['arcurl'])


