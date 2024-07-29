import requests
import time

# Define the common headers (excluding the authorization token)
common_headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "origin": "https://app.duckcoop.xyz",
    "priority": "u=1, i",
    "referer": "https://app.duckcoop.xyz/",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
    "content-type": "application/json"
}

# List of authorization tokens / Multiple Accounts
authorization_tokens = [
    "Bearer eyJhbGcxxxxIUzI1NiIsInR5xxxxxxxx.eyJ1c2VySWQiOjQ0NjIxNzxxxxVzdGFtcCI6MTcyxxxxxxEyMywidHlwZSI6MSwiaWF0IjoxNzIyMjQ3NDI0LCJleHAiOjExxxxx.UG-972JDJl03LaF8Ry56nSxXYJzR4XM_50GtC5xxxxxx",
    "Bearer eyJhbGcxxxxIUzI1NiIsInR5xxxxxxxx.eyJ1c2VySWQiOjQ0NjIxNzxxxxVzdGFtcCI6MTcyxxxxxxEyMywidHlwZSI6MSwiaWF0IjoxNzIyMjQ3NDI0LCJleHAiOjExxxxx.UG-972JDJl03LaF8Ry56nSxXYJzR4XM_50GtC5xxxxxx"
]

order_limit = 3
account_state = {
    token: {
        "current_game_id": None,
        "orders_placed": 0,
        "orders_finished": False,
        "previous_loss": False,
        "initial_quantity": 500
    } for token in authorization_tokens
}

def get_balance(headers):
    url = "https://game-api.duckcoop.xyz/balance/get"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'balance' in data['data']:
            return int(float(data['data']['balance']))  # Convert to integer
    return None

def get_latest_game_id(headers):
    url = "https://game-api.duckcoop.xyz/dump-game/list-game"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        if 'data' in data and 'data' in data['data']:
            latest_game = data['data']['data'][0]
            return latest_game['id']
    return None

def create_order(headers, game_id, quantity, price_out):
    url = "https://game-api.duckcoop.xyz/dump-game/create-order"
    payload = {
        "game_id": game_id,
        "quantity": quantity,
        "price_out": price_out
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to create order. Status code: {response.status_code}, Response: {response.text}")
    return None

def process_orders_for_account(token):
    headers = common_headers.copy()
    headers["authorization"] = token

    state = account_state[token]
    game_id = get_latest_game_id(headers)
    if game_id is None:
        print(f"Failed to get the latest game ID for token {token}")
        return

    # Check if the game ID has changed and reset the order count and finished flag
    if game_id != state["current_game_id"]:
        state["current_game_id"] = game_id
        state["orders_placed"] = 0
        state["orders_finished"] = False

    # Skip placing orders if the order limit has been reached or orders are finished
    if state["orders_placed"] >= order_limit or state["orders_finished"]:
        print(f"Order limit reached or orders finished for game ID {game_id} for token {token}. Skipping order placement.")
        return

    balance = get_balance(headers)
    if balance is None:
        print(f"Failed to get the balance for token {token}")
        return

    # Skip placing orders if the balance is below 10,000
    if balance < 10000:
        print(f"Balance {balance} is below 10,000 for token {token}. Skipping order placement.")
        state["orders_finished"] = True
        return

    # Determine order quantity based on previous outcome
    if state["previous_loss"]:
        order_quantity = 5000
    else:
        order_quantity = state["initial_quantity"]

    orders_to_create = []
    remaining_balance = balance

    while remaining_balance >= order_quantity and len(orders_to_create) + state["orders_placed"] < order_limit:
        orders_to_create.append(order_quantity)
        remaining_balance -= order_quantity

    if remaining_balance > 0 and len(orders_to_create) + state["orders_placed"] < order_limit:
        orders_to_create.append(remaining_balance)

    print(f"Creating orders for game ID {game_id} with balance {balance} for token {token}")
    for quantity in orders_to_create:
        order_response = create_order(headers, game_id, quantity, 1.1)  # Minimum price_out set to 1.1
        if order_response:
            state["orders_placed"] += 1
            state["previous_loss"] = False  # Reset the loss flag after a successful order
            print(f"Created order for token {token}: {order_response}")
        else:
            state["previous_loss"] = True  # Set the loss flag if the order fails
            print(f"Failed to create order for token {token}")

# Run the process in a loop every 15 seconds
while True:
    for token in authorization_tokens:
        process_orders_for_account(token)
    time.sleep(15)
