import zmq

nutrition_data = {
    "veggie lasagna": {"calories": 150, "protein": 7, "fat": 5},
    "black bean tacos": {"calories": 200, "protein": 8, "fat": 7},
    "grilled cheese sandwich": {"calories": 250, "protein": 12, "fat": 15},
    "avocado toast": {"calories": 220, "protein": 6, "fat": 18},
    "pesto zoodles": {"calories": 120, "protein": 4, "fat": 8},
    "eggplant parmesan": {"calories": 180, "protein": 9, "fat": 10},
    "mushroom risotto": {"calories": 160, "protein": 5, "fat": 6},
    "lentil soup": {"calories": 90, "protein": 7, "fat": 2},
    "stuffed shells": {"calories": 200, "protein": 10, "fat": 8},
}


def get_nutrition(item):
    return nutrition_data.get(item.lower(), {})

def calculate_custom_serving(item, num_servings):
    nutrition_data = get_nutrition(item)
    if not nutrition_data:
        return {"error": f"No data available for item: {item}"}
    
    if num_servings <= 0:
        return {"error": "Number of servings must be greater than zero"}
    
    factor = 1 / num_servings
    per_serving_data = {key: value * factor for key, value in nutrition_data.items()}
    
    return {
        "per_serving": per_serving_data,
        "number_of_servings": num_servings
    }

def compare_nutrition(current_food, new_food):
    data1 = get_nutrition(current_food)
    data2 = get_nutrition(new_food)
    if not data1 or not data2:
        return {}
    
    comparison = {
        key: {
            current_food: data1.get(key, 0),
            new_food: data2.get(key, 0)
        }
        for key in set(data1.keys()).union(data2.keys())
    }
    return comparison

def nutrition_service():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    print("Nutrition Service is running on port 5555...")
    
    while True:
        message = socket.recv_json()
        action = message.get("action")
        item = message.get("item")

        if not action:
            response = {"error": "Action not specified"}
        elif action == "retrieve_nutrition":
            if not item:
                response = {"error": "'item' not provided"}
            else:
                response = get_nutrition(item)
        elif action == "calculate_serving":
            num_servings = message.get("num_servings")
            if not item or num_servings is None:
                response = {"error": "'item' or 'num_servings' not provided"}
            else:
                response = calculate_custom_serving(item, num_servings)
        elif action == "compare_food":
            current_food = message.get("current_food")
            new_food = message.get("new_food")
            if not current_food or not new_food:
                response = {"error": "'current_food' or 'new_food' not provided"}
            else:
                response = compare_nutrition(current_food, new_food)
        else:
            response = {"error": "Unknown action"}

        socket.send_json(response)

if __name__ == "__main__":
    nutrition_service()
