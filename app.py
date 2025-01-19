from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/rating', methods=['GET'])
def calculate_rating():
    # Отримання параметрів з URL
    total_rating = int(request.args.get('total_rating', 0))
    rating_count = int(request.args.get('rating_count', 0))

    # Розрахунок середнього рейтингу
    if rating_count > 0:
        average_rating = round(total_rating / rating_count, 2)
    else:
        average_rating = 0.0

    return jsonify({"average_rating": average_rating})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
