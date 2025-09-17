from flask import Flask, request, jsonify
from joblib import load
import sys

app = Flask(__name__)
clf = None

def loadModel():
    global clf
    clf = load("safety_rules.model")
    print("model loaded", file=sys.stderr)

# load on import (works for gunicorn too)
loadModel()

@app.route("/")
def hello():
    return "hello :)"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json(force=True, silent=False)
        val = payload["data"]
        if isinstance(val, (int, float)):
            features = [[val]]
        elif isinstance(val, list) and len(val) == 1 and isinstance(val[0], (int, float)):
            features = [val]
        else:
            return jsonify(error="Expected 'data' to be a number or [number]."), 400

        pred = float(clf.predict(features)[0])
        return jsonify(prediction=pred), 200
    except KeyError:
        return jsonify(error="Missing 'data' in JSON body."), 400
    except Exception as e:
        return jsonify(error=f"prediction failed: {e.__class__.__name__}"), 500

@app.route("/_health")
def _health():
    return "_health", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=False)
