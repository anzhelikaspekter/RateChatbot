from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Server is working!", 200
@app.route('/rating', methods=['POST'])
def calculate_rating():
    data = request.json
    total_rating = int(data.get('total_rating', 0))
    rating_count = int(data.get('rating_count', 0))

    if rating_count > 0:
        average_rating = round(total_rating / rating_count, 2)
    else:
        average_rating = 0.0

    return jsonify({"average_rating": average_rating})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
