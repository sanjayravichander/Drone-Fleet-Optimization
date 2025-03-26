# Drone Delivery Assignment System

## 📌 Project Overview
The **Drone Delivery Assignment System** is designed to efficiently allocate drones for delivering orders based on their payload capacity and speed. The system ensures optimal order fulfillment while minimizing total travel distance using a greedy nearest-neighbor approach.

## 🚀 Features
- **Prioritization of Drones**: Drones are sorted based on payload capacity and speed to maximize efficiency.
- **Dynamic Order Assignment**: Orders are assigned to available drones while respecting payload limits.
- **Greedy Route Optimization**: The system optimizes the delivery sequence to minimize travel distance.
- **Safe Order Removal**: Ensures that assigned orders are removed without index shifting errors.

## 🛠️ How It Works
1. **Sort Drones**: Drones are sorted in descending order of payload and ascending order of speed.
2. **Iterate Over Drones**: Each available drone attempts to fulfill as many orders as possible.
3. **Assign Orders Greedily**: Orders are selected based on weight capacity constraints.
4. **Optimize Delivery Route**: The system calculates the optimal delivery route for assigned orders.
5. **Store Results**: The assignments are stored and returned as structured data.

## 📄 Code Structure
### **`assign_drones(drones, orders)`**
```python
def assign_drones(drones, orders):
    """Assign drones to orders by prioritizing payload capacity and speed."""
    assignments = []
    drones = sorted(drones, key=lambda d: (-d["max_payload"], d["speed"]))
    
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
```

## 📊 Example Input & Output
### **Input:**
```json
{
    "drones": [
        {"id": "D1", "max_payload": 50, "speed": 20, "available": true},
        {"id": "D2", "max_payload": 80, "speed": 15, "available": true}
    ],
    "orders": [
        {"id": "O1", "package_weight": 10, "delivery_x": 2, "delivery_y": 3},
        {"id": "O2", "package_weight": 20, "delivery_x": 5, "delivery_y": 6},
        {"id": "O3", "package_weight": 30, "delivery_x": 8, "delivery_y": 9}
    ]
}
```

### **Output:**
```json
[
    {"id": "D2", "orders": ["O1", "O2", "O3"], "total_distance": 25},
    {"id": "D1", "orders": [], "total_distance": 0}
]
```

## 🛠️ Installation & Usage
1. **Clone the Repository:**
```sh
git clone https://github.com/yourusername/drone-delivery.git
cd drone-delivery
```

2. **Run the Script:**
```sh
python main.py
```

3. **Modify Inputs:** Update `drones.json` and `orders.json` for custom data.

## 📌 Dependencies
- Python 3.10+
- NumPy (for calculations)
