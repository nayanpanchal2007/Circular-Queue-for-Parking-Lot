# Circular Parking Queue (Mini Project)

A simple educational project that models a parking lot using a circular queue and shows a live GUI with Tkinter.

## 🚗 What this project does

- Visualizes parking slots in a circular layout
- Supports queue operations:
  - Enqueue (park new car)
  - Dequeue (car leaves FIFO)
  - Peek front car
- Additional operations:
  - Search car by ID
  - Remove car by ID
  - Resize parking capacity
  - Clear all cars
- Shows dashboard stats: total slots, occupied, free, front/rear indices
- Uses timestamps to calculate parked duration

## 🛠️ Requirements

- Python 3.x
- No extra libraries; uses built-in `tkinter`

## ▶️ Run

1. Open terminal in project directory
2. Run:

```powershell
python app.py
```

## 🎮 Controls (UI)

- `Set Size`: change the number of parking slots
- `Enqueue (Park)`: park car (ID optional, auto-generated if blank)
- `Dequeue (Leave)`: remove car at front
- `Peek Front`: preview next car to leave
- `Search Car`: highlight car by ID
- `Remove Car`: remove specific car by ID
- `Clear All`: empty the lot

## 🔍 Status panel

- Total slots
- Occupied slots
- Free slots
- Front index
- Rear index

## 💡 Notes

- Empty slots are gray; occupied are blue.
- `F` marks the front, `R` marks the rear.
- Latest operation slot is highlighted.
- Works best where GUI is supported (local desktop).

## 🧩 Code overview

`ParkingQueue` class in `app.py` implements:
- `enqueue`, `dequeue`, `peek_front`
- `find_index_by_car_id`, `remove_by_car_id`
- `set_size`, `is_empty`, `is_full`

## 🌱 Ideas to extend

- Save logs to file
- Parking fee computation
- Vehicle categories/colors
- Multi-level parking or space reservation

