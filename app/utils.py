import requests
import logging
import json

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def upload_image_to_telegra(image_path, access_token):
    url = 'https://telegra.ph/upload'
    try:
        with open(image_path, 'rb') as image_file:
            response = requests.post(url, files={'file': image_file})
        response.raise_for_status()
        image_url = response.json()[0]['src']
        logging.info(f'Image uploaded successfully: {image_url}')
        return image_url
    except requests.RequestException as e:
        logging.error(f'Failed to upload image: {e}')
        return None

def create_telegraph_page(title, content, access_token, author_name, author_url):
    url = 'https://api.telegra.ph/createPage'
    data = {
        'access_token': access_token,
        'title': title,
        'author_name': author_name,
        'author_url': author_url,
        'content': json.dumps(content)  # Ensure the content is JSON-encoded
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        result = response.json()['result']
        logging.info(f'Page created successfully')
        return result
    except requests.RequestException as e:
        logging.error(f'Failed to create page: {e}')
        return None

def get_author_info(access_token):
    url = 'https://api.telegra.ph/getAccountInfo'
    params = {
        'access_token': access_token,
        'fields': json.dumps(["short_name", "author_name", "author_url"])
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()['result']
        logging.info(f'Author info retrieved successfully')
        return result
    except requests.RequestException as e:
        logging.error(f'Failed to get author info: {e}')
        return None

def get_author_name(info):
    return info['short_name'] if info else None

def get_author_url(info):
    return info['author_url'] if info else None

def get_page_list(access_token, offset=0, limit=10):
    url = 'https://api.telegra.ph/getPageList'
    params = {
        'access_token': access_token,
        'offset': offset,
        'limit': limit
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()['result']
        logging.info(f'Page list retrieved successfully')
        return result
    except requests.RequestException as e:
        logging.error(f'Failed to get page list: {e}')
        return None
