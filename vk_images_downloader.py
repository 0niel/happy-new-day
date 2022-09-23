import time
import requests

access_token = "<YOUR_USER_TOKEN>"  # https://vkhost.github.io/
api_url = "https://api.vk.com/method/wall.get"

i = 0
request_num = 0
for offset in range(0, 2468, 20):
    data = {
        "owner_id": -138742149,
        "offset": offset,
        "access_token": access_token,
        "v": 5.131,
    }
    if request_num % 5 == 0:
        time.sleep(1)
    items = requests.post(api_url, data=data).json()["response"]["items"]
    request_num += 1
    for item in items:
        if "attachments" in item:
            for attachment in item["attachments"]:
                if attachment["type"] == "photo":
                    photo_url = attachment["photo"]["sizes"][-1]["url"]
                    fullname = f"{str(i)}.jpg"
                    img_data = requests.get(photo_url).content
                    request_num += 1
                    with open(f"images//{fullname}", "wb") as handler:
                        i += 1
                        print(f"Download {i}")
                        handler.write(img_data)
