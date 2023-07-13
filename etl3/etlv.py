# server.py
from flask import Flask
import myscript

app = Flask(__name__)

@app.route('/run-script', methods=['GET'])
def run_script():
    result = myscript.main()
    return result

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050)
