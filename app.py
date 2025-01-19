import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Отримання токена доступу до API SendPulse


def get_access_token(client_id, client_secret):
    url = "https://api.sendpulse.com/oauth/access_token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }
    response = requests.post(url, data=data)
    return response.json().get("access_token")

# Оновлення змінної в SendPulse


def update_sendpulse_variable(user_id, average_rating, access_token):
    url = f"https://api.sendpulse.com/chatbot/variable"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    data = {
        "user_id": user_id,
        "variable_name": "average_rating",
        "value": average_rating,
    }
    response = requests.post(url, json=data, headers=headers)
    return response.status_code


@app.route('/rating', methods=['POST'])
def calculate_and_update_rating():
    # Отримання даних з вебхука
    data = request.json
    total_rating = int(data.get("total_rating", 0))
    rating_count = int(data.get("rating_count", 0))
    user_id = data.get("user_id", None)  # Отримай user_id з SendPulse

    # Розрахунок середнього рейтингу
    if rating_count > 0:
        average_rating = round(total_rating / rating_count, 2)
    else:
        average_rating = 0.0

    # Оновлення змінної через API SendPulse
    client_id = "3549ebd6350dd94d31f869947d7d1f16"
    client_secret = "3f98eae71a6f3e84a30036eb4855396d"
    access_token = get_access_token(client_id, client_secret)

    if user_id:
        status_code = update_sendpulse_variable(
            user_id, average_rating, access_token)
        return jsonify({"average_rating": average_rating, "status": status_code})
    else:
        return jsonify({"error": "user_id is missing"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
