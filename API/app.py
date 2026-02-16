import sys
from flask import Flask, request, jsonify
from flask_cors import CORS

# Agregar la raíz del proyecto al path
root = Path(__file__).parent.parent 
sys.path.insert(0, str(root))


import  translate # Import the translate module
import normalize.normalize as normalize


app = Flask(__name__)
CORS(app)  # Enable CORS for frontend applications (Angular, React, etc.)


@app.get("/Translate")
def home():    
    text = normalize.normalize(request.args.get('text', '')) 

    print("Texto a traducir:", text)

    translation = translate.translate(text)
    return  jsonify({"traduction": translation})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)