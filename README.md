# Circular Parking Queue (Mini Project)

This is a small college mini-project demonstrating a circular queue data structure used to model a parking lot with a graphical user interface.

## Features

- **Visual circular layout** of parking slots displayed on a Tkinter Canvas
- **Enqueue (Park)** – Add a car to the parking lot
- **Dequeue (Leave)** – Remove the car at the front (FIFO order)
- **Peek Front** – View the next car to leave without removing it
- **Search Car** – Find a specific car by ID and highlight its location
- **Remove Car** – Remove a specific car by ID from anywhere in the parking lot
- **Dynamic parking size** – Adjust parking capacity; existing cars are preserved in order when possible
- **Entry/Exit timestamps** – Track when cars enter and how long they stay parked
- **Visual indicators** – "F" marks the front and "R" marks the rear; highlighted slots show last operations
- **Live dashboard** – Displays total slots, occupied count, free slots, and front/rear indices
- **Auto Car ID generation** – If no Car ID is provided, one is automatically generated

## Requirements

- Python 3.x (no external packages required — uses built-in Tkinter)

## How to Run

1. Open a terminal in the project folder
2. Run:

```powershell
python app.py
```

## Usage

### Basic Operations

- **Set Parking Size**: Enter a number and click "Set Size" to change capacity (default is 8)
- **Park a Car**: Enter an optional Car ID (or leave blank for auto-generation) and click "Enqueue (Park)"
- **Remove a Car (FIFO)**: Click "Dequeue (Leave)" to remove the car at the front and see its stay duration
- **Check Next Car**: Click "Peek Front" to view the car that will leave next
- **Search for a Car**: Enter a Car ID and click "Search Car" to locate it in the parking lot
- **Remove Specific Car**: Enter a Car ID and click "Remove Car" to remove that car from any position
- **Clear All**: Click "Clear All" to empty the entire parking lot

### Dashboard Information

- **Total Slots**: Total parking capacity
- **Occupied**: Number of parked cars
- **Free**: Number of available slots
- **Front Index**: Position of the car at the front of the queue
- **Rear Index**: Position of the car at the rear of the queue

## UI Details

- The circular layout visualizes the queue structure with slots arranged in a circle
- Occupied slots are blue; empty slots are gray
- "F" and "R" markers indicate the front and rear of the queue
- Highlighted slots (dashed outline) show the result of the last operation
- Entry and exit times are displayed for parked and departing cars
- The status bar provides real-time feedback on all actions

## Implementation Details

The `ParkingQueue` class implements a circular queue with the following operations:

- `enqueue(car)` – Add a car (O(1))
- `dequeue()` – Remove front car (O(1))
- `peek_front()` – View front car (O(1))
- `find_index_by_car_id(car_id)` – Search by ID (O(n))
- `remove_by_car_id(car_id)` – Remove by ID, maintaining order (O(n))
- `set_size(new_size)` – Resize with preservation (O(n))
- `is_empty()` / `is_full()` – Status checks (O(1))

## Notes

- The GUI uses a circular layout to visualize the queue structure
- If the environment is headless (no GUI display), run locally on your machine to see the interface
- Cars are stored with ID and entry timestamp for duration calculation
- The project is intentionally simple and readable; you can extend it with features like:
  - Different colors for different vehicle types
  - Persistent parking logs (save to file)
  - Animations for car movement
  - Fee calculation based on duration
  - Multi-level parking structure
