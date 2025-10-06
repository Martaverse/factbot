from flask import Flask, request, jsonify
import requests, os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
MW_API_KEY = os.getenv("MW_API_KEY")

def define_word(word):
    url = f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={MW_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if not data or not isinstance(data[0], dict):
        return {"error": "No definition found"}

    entry = data[0]
    definition = entry["shortdef"][0]
    part_of_speech = entry.get("fl", "unknown")
    return {
        "word": word,
        "definition": definition,
        "part_of_speech": part_of_speech,
        "example": "Example not available",
        "source": "Merriam-Webster Dictionary"
    }

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    parts = user_input.strip().split(maxsplit=1)
    command = parts[0].lower()
    payload = parts[1] if len(parts) > 1 else ""

    if command == "dfine":
        result = define_word(payload)
        if "error" in result:
            return jsonify({"response": result["error"]})
        return jsonify({
            "response": f"""📚 *{result['word']}* ({result['part_of_speech']}): {result['definition']}
🔗 {result['source']}"""
        })
    return jsonify({"response": "Unknown command"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
