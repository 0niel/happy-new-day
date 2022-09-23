import base64
import time
import requests

YANDEX_API_KEY = "<SERVICE_API_KEY>"
YANDEX_FOLDER_ID = "<FOLDER_ID>"


def encode_file(file):
    with open(file, "rb") as f:
        file_content = f.read()
    return base64.b64encode(file_content).decode("utf-8")


def get_text_from_results(results):
    text_result = ""
    text_detection_results = results["results"][0]["textDetection"]
    for page in text_detection_results["pages"]:
        if "blocks" in page:
            for block in page["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        if "words" in line:
                            for word in line["words"]:
                                text_result += word["text"] + (
                                    " " if len(text_result) > 0 else ""
                                )
    return text_result


images_results = []

i = 0
while i < 2485:
    headers = {
        "Authorization": f"Api-Key {YANDEX_API_KEY}",
        "Content-Type": "application/json",
    }

    specs = []
    for _ in range(5):
        if i < 2485:
            tmp = {
                "features": [
                    {
                        "type": "TEXT_DETECTION",
                        "textDetectionConfig": {
                            "languageCodes": ["ru"],
                            "model": "page",
                        },
                    }
                ],
                "mimeType": "image/jpeg",
                "content": encode_file(f"{str(i)}.jpg"),
            }
            specs.append(tmp)
            i += 1

    payload = {
        "analyzeSpecs": specs,
        "folderId": YANDEX_FOLDER_ID,
    }

    r = requests.post(
        "https://vision.api.cloud.yandex.net/vision/v1/batchAnalyze",
        json=payload,
        headers=headers,
    )

    print(i)

    response = r.json()

    if "results" in response:
        for results in response["results"]:
            text_result = ""
            try:
                text_result = get_text_from_results(results)
            except KeyError as ex:
                time.sleep(5)
            finally:
                images_results.append(text_result.strip())

    time.sleep(1)

with open(r"results.txt", "w", encoding="utf-8") as file:
    for i in range(len(images_results)):
        file.write(f"{str(i)}. [{images_results[i]}]\n")
