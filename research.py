import json

# The Sample cases are loaded and saved as input_case1.json and input_case2.json
# Loading the Data
def load_data(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    city_grid = data["city"]["grid_size"]
    drones = data["drones"]["fleet"]
    orders = data["orders"]

    return city_grid, drones, orders

# Functions needed to drones to take orders
def manhattan_distance(x1, y1, x2, y2):
    # Calculate the distance between base and delivery points to get the distance
    # This distance is later used to detect whether a drone can take the order that satifies below the max_payload
    return abs(x1 - x2) + abs(y1 - y2)

def can_fulfill_order(drone, order):
    # Take the orders if the drone can fulfill the given constraints
    # 1. calculate the total distance From and to, that's why it is multiplied by 2
    distance = 2 * manhattan_distance(0, 0, order["delivery_x"], order["delivery_y"])  # Round-trip
    # 2. Take only the order that satisfies the condition given to drones like payload and max_distance
    return order["package_weight"] <= drone["max_payload"] and distance <= drone["max_distance"]

def calculate_greedy_route(order_list):
# This particular function is to make the drones available to take multiple order if the condition satisfies like total distance should be lesser than max_distance
# After completing orders it should return to base
    if not order_list:
        return 0

    base_x, base_y = 0, 0 #(Start point)
    total_distance = 0
    current_x, current_y = base_x, base_y
    remaining_orders = order_list.copy() # copying from the orders list of the recent order

    while remaining_orders:
        # If order is placed, it should check the distance of that particular order need to be delivered
        nearest_order = min(remaining_orders, key=lambda order: manhattan_distance(current_x, current_y, order["delivery_x"], order["delivery_y"]))

        # If order is placed and it's distance is lesser then the max_distance covered by that drone, take that order
        total_distance += manhattan_distance(current_x, current_y, nearest_order["delivery_x"], nearest_order["delivery_y"])
        current_x, current_y = nearest_order["delivery_x"], nearest_order["delivery_y"]

        # Carefully removing the fulfilled orders from order list
        remaining_orders.remove(nearest_order)

    # After completing it should return to base
    total_distance += manhattan_distance(current_x, current_y, base_x, base_y)
    
    return total_distance

# Assigning Drones
def assign_drones(drones, orders):
    # Assigning drones which should prioritize the weight and speed
    assignments = []
    drones = sorted(drones, key=lambda d: (-d["max_payload"], d["speed"]))  # Sort by payload, then speed
    # Checks if the drone is available
    for drone in drones:
        if not drone["available"]:
            continue

        drone_orders = []
        remaining_capacity = drone["max_payload"]
        to_remove = [] #  Storings indexes of assigned orders so they can be removed safely later.

        for i, order in enumerate(orders):
            if can_fulfill_order(drone, order) and remaining_capacity >= order["package_weight"]:
                drone_orders.append(order)
                remaining_capacity -= order["package_weight"]
                to_remove.append(i)

        # Remove assigned orders safely
        for index in sorted(to_remove, reverse=True):
            orders.pop(index) # Sorts indices in descending order before removal.This ensures we remove items from the end first, preventing shifting errors.

        if drone_orders:
            total_distance = calculate_greedy_route(drone_orders)
            assignments.append({
                "id": drone["id"],
                "orders": [order["id"] for order in drone_orders],
                "total_distance": total_distance
            })

    return assignments

# Formatting output in structured way
def write_output(assignments, file_path):
    """Save the drone assignments to an output JSON file."""
    output_data = {"assignments": assignments}
    with open(file_path, "w") as file:
        json.dump(output_data, file, indent=4)

# Executing the code and it should give results for two test cases and it should be able to handle future test cases too
def main():
    # For Handling multiple test cases
    test_cases = ["input_case1.json", "input_case2.json"]  # Test case files

    for test_file in test_cases:
        print(f"Running test case: {test_file}")

        # Loading the data
        city_grid, drones, orders = load_data(test_file)

        # Asigning orders to drones
        assignments = assign_drones(drones, orders)

        # Output format
        output_file = test_file.replace("input", "output")  # Example: My input_case1.json will reflect as output_case1.json. Same goes to my input_case2
        write_output(assignments, output_file)

        print(f"Results written to {output_file}")

# Run the program
if __name__ == "__main__":
    main()
