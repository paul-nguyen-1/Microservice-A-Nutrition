import zmq

class ZeroMQ:
    def __init__(self):
        self.nutrition_context = zmq.Context()
        self.nutrition_socket = self.nutrition_context.socket(zmq.REQ)
        self.nutrition_socket.connect("tcp://localhost:5555")
        
    def get_nutrition_data(self, item):
        try:
            self.nutrition_socket.send_json({
                "action": "retrieve_nutrition",
                "item": item
            })
            return self.nutrition_socket.recv_json()
        except Exception as e:
            return {"error": f"Failed to fetch nutrition data: {str(e)}"}
        
    def calculate_custom_serving(self, item, num_servings):
        try:
            self.nutrition_socket.send_json({
                "action": "calculate_serving",
                "item": item,
                "num_servings": num_servings
            })
            return self.nutrition_socket.recv_json()
        except Exception as e:
            return {"error": f"Failed to calculate custom serving: {str(e)}"}

    
    def get_compare_data(self, current_food, new_food):
        try:
            self.nutrition_socket.send_json({
                "action": "compare_food",
                "current_food": current_food,
                "new_food": new_food,
            })
            return self.nutrition_socket.recv_json()

        except Exception as e:
            return {"error": f"Failed to compare foods: {str(e)}"}

def test_client():
    client = ZeroMQ()

    print("Test retrieve nutrition data")
    food_item = "Veggie Lasagna"
    nutrition_data = client.get_nutrition_data(food_item)
    if "error" in nutrition_data:
        print(f"Error: {nutrition_data['error']}")
    else:
        print(f"Nutrition data for {food_item}: {nutrition_data}")

    print("\nTesting calculate custom serving size...")
    food_item = "Veggie Lasagna"
    num_servings = 4 
    custom_serving_data = client.calculate_custom_serving(food_item, num_servings)
    if "error" in custom_serving_data:
        print(f"Error: {custom_serving_data['error']}")
    else:
        print(f"Custom serving size data for {food_item} (split into {num_servings} servings): {custom_serving_data}")

    print("\nTest compare foods")
    current_food = "Veggie Lasagna"
    new_food = "Black Bean Tacos"
    comparison_data = client.get_compare_data(current_food, new_food)
    if "error" in comparison_data:
        print(f"Error: {comparison_data['error']}")
    else:
        print(f"Comparison between {current_food} and {new_food}: {comparison_data}")

if __name__ == "__main__":
    test_client()
