# server.py
from flask import Flask
import main  # importar main en lugar de myscript




app = Flask(__name__)

@app.route('/run-script', methods=['GET'])
def run_script():
    result = main.main()  # llamar a main.main() en lugar de myscript.main()
    return result

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
