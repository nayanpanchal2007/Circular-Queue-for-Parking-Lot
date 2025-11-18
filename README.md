# Circular Parking Queue (Mini Project)

This is a small college mini-project demonstrating a circular queue used to model a parking lot.

Features:
- Visual circular layout of parking slots (Tkinter Canvas).
- Enqueue (park) and Dequeue (leave) operations.
- Dynamic parking size (set size preserves existing cars in order when possible).
- Simple, attractive UI with head/tail markers.

Requirements
- Python 3.x (no external packages required — uses built-in Tkinter)

How to run
1. Open a terminal in the project folder `circular_parking_app`.
2. Run:

```powershell
python app.py
```

Usage
- Set the parking size, or use the default (8).
- Enter an optional Car ID or leave blank to auto-generate one.
- Click "Enqueue (Park)" to park a car.
- Click "Dequeue (Leave)" to remove the car at the front (FIFO).

Notes
- The GUI uses a circular layout to visualize the queue. "F" marks the front and "R" marks the rear.
- If the environment is headless (no GUI display), run locally on your machine to see the interface.

Instructor / Student
- This project is intentionally simple and readable. You can extend it by adding colors per car, saving logs, or adding animations.
