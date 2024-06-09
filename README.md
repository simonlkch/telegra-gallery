# Telegra.ph Image Uploader

This project provides a web application to bulk upload images to Telegra.ph and create pages including those images. It also allows the user to view all created pages.

## Features
- Bulk upload images to Telegra.ph
- Create pages including the uploaded images
- Display all created pages

## Requirements
- Docker
- Python 3.9
- Flask
- Requests

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Build the Docker image:
    ```
    docker build -t telegraph-image-uploader .
    ```
4. Run the Docker container:
    ```
    docker run -p 3000:3000 telegraph-image-uploader
    ```

## Usage

1. Access the application at `http://localhost`
2. Provide your Telegra.ph access token, page title, and select images to upload
3. View the created pages at `http://localhost/pages`

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
