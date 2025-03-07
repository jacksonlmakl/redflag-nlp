from flask import Flask, request, jsonify
from analyzer import RedFlag

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def get_redflags():
    """
    Flask endpoint that receives a text body and returns detected biases, fallacies, and propaganda techniques.
    """
    data = request.get_json()  # Expecting JSON input

    if not data or 'text_body' not in data:
        return jsonify({"error": "Missing 'text_body' in request"}), 400

    text_body = data['text_body'].strip()
    rf = RedFlag(text_body)
    summary_out=rf.summary
    del summary_out['text_body']
    output={
        "summary": summary_out.to_dict(orient='records'),
        "analysis": rf.agentic_analysis.to_dict(orient='records')
    }
    return jsonify(output)  # Assuming `rf.summary` is a JSON-ready object

if __name__ == '__main__':
    app.run(debug=True)  # Runs the server on localhost
