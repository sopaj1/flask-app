from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return '''
        <html>
            <head>
                <title>Welcome to MSOE!</title>
                <style>
                    body { text-align: center; font-family: Arial, sans-serif; background-color: #f0f0f0; }
                    h1 { color: #007bff; }
                    p { font-size: 20px; color: #555; }
                </style>
            </head>
            <body>
                <h1>Hello MSOE!</h1>
                <p>Welcome to the coolest Flask app around! 🎉</p>
            </body>
        </html>
    '''

if __name__ == "__main__":
    app.run()
