import json

# ----------------------- 1. Load Data -----------------------
def load_data(file_path):
    """Load city grid, drone fleet, and orders from the input JSON file."""
    with open(file_path, "r") as file:
        data = json.load(file)

    city_grid = data["city"]["grid_size"]
    drones = data["drones"]["fleet"]
    orders = data["orders"]

    return city_grid, drones, orders

# ----------------------- 2. Helper Functions -----------------------
def manhattan_distance(x1, y1, x2, y2):
    """Calculate the Manhattan distance between two points."""
    return abs(x1 - x2) + abs(y1 - y2)

def can_fulfill_order(drone, order):
    """Check if a drone can fulfill an order based on payload and distance constraints."""
    distance = 2 * manhattan_distance(0, 0, order["delivery_x"], order["delivery_y"])  # Round-trip
    return order["package_weight"] <= drone["max_payload"] and distance <= drone["max_distance"]

def calculate_greedy_route(order_list):
    """
    Optimize order delivery sequence using a greedy nearest-neighbor heuristic.
    The drone selects the closest available order at each step.
    """
    if not order_list:
        return 0

    base_x, base_y = 0, 0  # Start from (0,0)
    total_distance = 0
    current_x, current_y = base_x, base_y
    remaining_orders = order_list.copy()

    while remaining_orders:
        # Find the closest order
        nearest_order = min(remaining_orders, key=lambda order: manhattan_distance(current_x, current_y, order["delivery_x"], order["delivery_y"]))

        # Travel to the order's location
        total_distance += manhattan_distance(current_x, current_y, nearest_order["delivery_x"], nearest_order["delivery_y"])
        current_x, current_y = nearest_order["delivery_x"], nearest_order["delivery_y"]

        # Remove fulfilled order
        remaining_orders.remove(nearest_order)

    # Return to base
    total_distance += manhattan_distance(current_x, current_y, base_x, base_y)
    
    return total_distance

# ----------------------- 3. Assign Drones to Orders -----------------------
def assign_drones(drones, orders):
    """Assign drones to orders by prioritizing payload capacity and speed."""
    assignments = []
    drones = sorted(drones, key=lambda d: (-d["max_payload"], d["speed"]))  # Sort by payload, then speed

    for drone in drones:
        if not drone["available"]:
            continue

        drone_orders = []
        remaining_capacity = drone["max_payload"]
        to_remove = []

        for i, order in enumerate(orders):
            if can_fulfill_order(drone, order) and remaining_capacity >= order["package_weight"]:
                drone_orders.append(order)
                remaining_capacity -= order["package_weight"]
                to_remove.append(i)

        # Remove assigned orders safely
        for index in sorted(to_remove, reverse=True):
            orders.pop(index)

        if drone_orders:
            total_distance = calculate_greedy_route(drone_orders)
            assignments.append({
                "id": drone["id"],
                "orders": [order["id"] for order in drone_orders],
                "total_distance": total_distance
            })

    return assignments

# ----------------------- 4. Write Output -----------------------
def write_output(assignments, file_path):
    """Save the drone assignments to an output JSON file."""
    output_data = {"assignments": assignments}
    with open(file_path, "w") as file:
        json.dump(output_data, file, indent=4)

# ----------------------- 5. Main Execution -----------------------
def main():
    """Main function to process multiple test cases."""
    test_cases = ["input_case1.json", "input_case2.json"]  # Test case files

    for test_file in test_cases:
        print(f"Running test case: {test_file}")

        # Step 1: Load Data
        city_grid, drones, orders = load_data(test_file)

        # Step 2: Assign Orders to Drones
        assignments = assign_drones(drones, orders)

        # Step 3: Write Output
        output_file = test_file.replace("input", "output")  # Example: input_case1.json → output_case1.json
        write_output(assignments, output_file)

        print(f"Results written to {output_file}")

# Run the program
if __name__ == "__main__":
    main()
