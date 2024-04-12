from bs4 import BeautifulSoup
import requests
import os
import json

with open("./config.json", "r") as coinfigs:
    data = json.load(coinfigs)
    config_bot_token = data['Bot_Token']
    config_chat_id = data['chat_id']

def send_to_telegram(
    image_path,
    api_token= config_bot_token,
    chat_id=config_chat_id,
):
    apiURL = f"https://api.telegram.org/bot{api_token}/sendDocument"
    try:
        response = requests.post(
            apiURL,
            data={"chat_id": chat_id},
            files={"document": open(image_path, "rb")},
        )
        print("Image sent to Telegram successfully!")
    except Exception as e:
        print(e)


def send_links_to_telegram(
    folder_name,
    api_token=config_bot_token,
    chat_id=config_chat_id,
):
    apiURL = f"https://api.telegram.org/bot{api_token}/sendDocument"
    try:
        with open(f"{folder_name}/links.txt", "rb") as f:
            response = requests.post(
                apiURL, data={"chat_id": chat_id}, files={"document": f}
            )
        print("Links sent to Telegram successfully!")
    except Exception as e:
        print(e)


def folder_create(
    images,
    url,
    folder_name,
    send_telegram=False,
    api_token=config_bot_token,
    chat_id=config_chat_id,
):
    try:
        os.mkdir(folder_name)
        with open(f"{folder_name}/links.txt", "w") as f:
            f.write("Website URL: " + url + "\n")
    except FileExistsError:
        print("Folder Exists!")
    except Exception as e:
        print(e)
    download_images(images, folder_name, send_telegram, api_token, chat_id)


def download_images(
    images,
    folder_name,
    send_telegram=False,
    api_token=config_bot_token,
    chat_id=config_chat_id,
):
    count = 0
    print(f"Total {len(images)} Images Found!")
    if len(images) != 0:
        for i, image in enumerate(images):
            try:
                image_link = (
                    image.get("data-srcset")
                    or image.get("data-src")
                    or image.get("data-fallback-src")
                    or image.get("src")
                )
                r = requests.get(image_link).content
                try:
                    r = str(r, "utf-8")
                except UnicodeDecodeError:
                    extension = image_link.split(".")[-1]
                    with open(f"{folder_name}/image{i + 1}.{extension}", "wb") as f:
                        f.write(r)
                    if send_telegram:
                        send_to_telegram(
                            f"{folder_name}/image{i + 1}.{extension}",
                            api_token,
                            chat_id,
                        )
                    count += 1
                    with open(f"{folder_name}/links.txt", "a") as f:
                        f.write(image_link + "\n")
            except:
                pass
        if count == len(images):
            print("All Images Downloaded!")
            if send_telegram:
                send_links_to_telegram(folder_name, api_token, chat_id)
        else:
            print(f"Total {count} Images Downloaded Out of {len(images)}")
            if send_telegram:
                send_links_to_telegram(folder_name, api_token, chat_id)
    else:
        print("No Images Found!")


def start_download(
    url,
    folder_path="Download",
    save_path="Download",
    send_telegram=False,
    api_token= config_bot_token,
    chat_id=config_chat_id,
):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    images = soup.findAll("img")
    folder_create(images, url, folder_path, send_telegram, api_token, chat_id)
