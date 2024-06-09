from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
import json
from utils import upload_image_to_telegra, create_telegraph_page, get_page_list

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/uploads/'

# Load configuration from file with UTF-8 encoding
with open('config.json', encoding='utf-8') as config_file:
    config = json.load(config_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form['access_token']
        title = request.form['title']
        files = request.files.getlist('images')
        image_urls = []
        file_names = []
        
        for file in files:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            image_url = upload_image_to_telegra(file_path, access_token)
            if image_url:
                image_urls.append(image_url)
                file_names.append(file.filename)
            # Delete the file after uploading
            os.remove(file_path)
        
        # Use author info from configuration
        author_url = config['author_url']
        author_name = config['author_name']

        # Generate content from configuration
        content = [
            {'tag': 'p', 'children': [
                {'tag': 'a', 'attrs': {'href': link['url']}, 'children': [link['text']]}
            ]} for link in config['links']
        ]
        content.append({'tag': 'a', 'attrs': {'href': author_url}, 'children': [f'Created by @{author_name}']})
        content.extend([
            {'tag': 'figure', 'children': [{'tag': 'img', 'attrs': {'src': image_url}}, {'tag': 'figcaption', 'children': [file_name]}]}
            for image_url, file_name in zip(image_urls, file_names)
        ])

        page = create_telegraph_page(title, content, access_token, author_name, author_url)
        if page:
            return redirect(url_for('pages', access_token=access_token))
    
    return render_template('index.html')

@app.route('/pages', methods=['GET'])
def pages():
    return render_template('pages.html')

@app.route('/api/pages', methods=['GET'])
def api_pages():
    access_token = request.args.get('access_token')
    draw = int(request.args.get('draw'))
    start = int(request.args.get('start'))
    length = int(request.args.get('length'))

    page_list = get_page_list(access_token, offset=start, limit=length)
    if page_list:
        total_count = page_list['total_count']
        pages = page_list['pages']
        data = [{
            'title': page['title'],
            'url': page['url'],
            'views': page['views'],
            'can_edit': page['can_edit']
        } for page in pages]

        response = {
            'draw': draw,
            'recordsTotal': total_count,
            'recordsFiltered': total_count,
            'data': data
        }
        return jsonify(response)
    return jsonify({
        'draw': draw,
        'recordsTotal': 0,
        'recordsFiltered': 0,
        'data': []
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
