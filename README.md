# Flask Application

This is a Flask application that extracts the dominant color palette from a given website. There are three ways to run this application:



1. Run `start.sh` script (recommended).
    ```
    ./start.sh
    ```

2. Build a Docker image and run the container:
    ```
    docker build -t cyber .
    docker run -p 5000:5000 cyber
    ```

3. Run the Flask application manually by installing the required packages from `requirements.txt`:
    ```
    pip install -r requirements.txt
    python3 app.py
    ```

Before running the application, ensure that you have Python 3 installed on your computer. You can check if you have it installed by running the command python3 --version in your terminal. If you don't have it installed, you can download it from the official Python website at https://www.python.org/downloads/.

## Usage

Once the Flask application is up and running, you can send a GET request to the `/` endpoint with the `url` parameter to extract the dominant color palette of a website. For example, to extract the dominant color palette of the Google homepage, you can send the following request:
    ```
    http://localhost:5000/?url=<WEBSITE_URL>
    ```

example:
    ```
    http://localhost:5000/?url=https://www.google.com/
    ```

### Note

Note: If you're using option 1 or 3 and you get an error related to the libGL.so.1 library, you may need to install the `libgl1-mesa-glx` package before starting the Flask app. You can do this by running the command `sudo apt-get install -y libgl1-mesa-glx` or by including it in your Dockerfile. The Dockerfile in this project already includes this package installation.
