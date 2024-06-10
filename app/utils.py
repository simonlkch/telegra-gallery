import requests
import os
import time
from flask import jsonify
import json

# Load config from config.json
with open('config.json', 'r', encoding='utf-8') as config_file:
    config = json.load(config_file)

def upload_image_to_telegra(file_path, access_token):
    url = "https://telegra.ph/upload"
    with open(file_path, 'rb') as file:
        response = requests.post(url, files={'file': file})
    if response.status_code == 200:
        return response.json()[0]['src']
    else:
        return None

def create_telegraph_page(title, content, access_token):
    url = "https://api.telegra.ph/createPage"
    data = {
        'access_token': access_token,
        'title': title,
        'content': content,
        'author_name': config['author_name'],
        'author_url': config['author_url']
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_page_list(access_token, offset=0, limit=10):
    url = f"https://api.telegra.ph/getPageList?access_token={access_token}&offset={offset}&limit={limit}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def bulk_upload_images(files, access_token):
    image_urls = []
    for i, file in enumerate(files):
        file_path = os.path.join('app/uploads', file.filename)
        file.save(file_path)
        image_url = upload_image_to_telegra(file_path, access_token)
        if image_url:
            image_urls.append(image_url)
        os.remove(file_path)

        if (i + 1) % config['batch_size'] == 0:
            time.sleep(config['delay_sec'])

    return image_urls

def build_content(image_urls):
    content = []
    for link in config['links']:
        content.append({
            'tag': 'p',
            'children': [
                {'tag': 'a', 'attrs': {'href': link['url']}, 'children': [link['text']]}
            ]
        })
    content.append({
        'tag': 'a',
        'attrs': {'href': config['author_url']},
        'children': [config['author_name']]
    })
    content += [
        {'tag': 'figure', 'children': [{'tag': 'img', 'attrs': {'src': url}}, {'tag': 'figcaption', 'children': [os.path.basename(url)]}]}
        for url in image_urls
    ]
    return content