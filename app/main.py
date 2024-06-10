from flask import Flask, request, render_template, redirect, url_for, jsonify
import os
from utils import bulk_upload_images, create_telegraph_page, get_page_list, build_content

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'app/uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        access_token = request.form['access_token']
        title = request.form['title']
        files = request.files.getlist('images')
        image_urls = bulk_upload_images(files, access_token)

        content = build_content(image_urls)

        page = create_telegraph_page(title, content, access_token)
        if page:
            return redirect(url_for('pages', access_token=access_token))

    return render_template('index.html')

@app.route('/pages', methods=['GET'])
def pages():
    return render_template('pages.html')

@app.route('/api/pages', methods=['GET'])
def api_pages():
    access_token = request.args.get('access_token')
    draw = int(request.args.get('draw', 0))
    start = int(request.args.get('start', 0))
    length = int(request.args.get('length', 10))

    page_list = get_page_list(access_token, offset=start, limit=length)
    if page_list:
        total_count = page_list['result']['total_count']
        pages = page_list['result']['pages']
        data = [{
            'title': page['title'],
            'url': page['url'],
            'views': page.get('views', 0),
            'can_edit': page.get('can_edit', False)
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
    app.run(debug=True, host='0.0.0.0', port=7500)
