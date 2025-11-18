import math
import tkinter as tk
from tkinter import simpledialog, messagebox


class ParkingQueue:
    """Circular queue for parking slots."""

    def __init__(self, size=8):
        if size < 1:
            raise ValueError("Size must be >= 1")
        self.size = size
        self.data = [None] * size
        self.front = 0  # index of first element
        self.count = 0

    def is_full(self):
        return self.count == self.size

    def is_empty(self):
        return self.count == 0

    def enqueue(self, value):
        if self.is_full():
            raise OverflowError("Parking is full")
        idx = (self.front + self.count) % self.size
        self.data[idx] = value
        self.count += 1
        return idx

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Parking is empty")
        val = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.size
        self.count -= 1
        return val

    def clear(self):
        self.data = [None] * self.size
        self.front = 0
        self.count = 0

    def set_size(self, new_size):
        if new_size < 1:
            raise ValueError("Size must be >= 1")
        # preserve existing queue items (in order) up to new_size
        items = [self.data[(self.front + i) % self.size] for i in range(self.count)]
        self.size = new_size
        self.data = [None] * new_size
        self.front = 0
        self.count = 0
        for it in items[:new_size]:
            if it is not None:
                self.enqueue(it)


class ParkingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Circular Queue - Parking Lot")
        self.configure(bg="#f5f7fa")
        self.geometry("900x700")

        # default
        self.queue = ParkingQueue(size=8)
        self.auto_car_id = 1

        # UI layout
        self._build_controls()
        self._build_canvas()
        self.draw_slots()

    def _build_controls(self):
        ctrl = tk.Frame(self, bg="#f5f7fa")
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=12, pady=8)

        tk.Label(ctrl, text="Parking size:", bg="#f5f7fa").pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=self.queue.size)
        self.size_entry = tk.Entry(ctrl, textvariable=self.size_var, width=6)
        self.size_entry.pack(side=tk.LEFT, padx=(4, 10))

        set_btn = tk.Button(ctrl, text="Set Size", command=self.on_set_size, bg="#4b7bec", fg="white")
        set_btn.pack(side=tk.LEFT, padx=4)

        tk.Label(ctrl, text="Car ID (optional):", bg="#f5f7fa").pack(side=tk.LEFT, padx=(20, 4))
        self.car_entry = tk.Entry(ctrl, width=12)
        self.car_entry.pack(side=tk.LEFT)

        enq_btn = tk.Button(ctrl, text="Enqueue (Park)", command=self.on_enqueue, bg="#20bf6b", fg="white")
        enq_btn.pack(side=tk.LEFT, padx=8)

        deq_btn = tk.Button(ctrl, text="Dequeue (Leave)", command=self.on_dequeue, bg="#eb3b5a", fg="white")
        deq_btn.pack(side=tk.LEFT, padx=8)

        reset_btn = tk.Button(ctrl, text="Clear All", command=self.on_clear, bg="#3867d6", fg="white")
        reset_btn.pack(side=tk.RIGHT)

        # status area
        status = tk.Frame(self, bg="#f5f7fa")
        status.pack(side=tk.TOP, fill=tk.X, padx=12)
        self.status_label = tk.Label(status, text="Welcome — set size and park cars.", anchor=tk.W, bg="#f5f7fa")
        self.status_label.pack(fill=tk.X)

    def _build_canvas(self):
        self.canvas_frame = tk.Frame(self, bg="#f5f7fa")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.canvas = tk.Canvas(self.canvas_frame, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda event: self.draw_slots())

    def draw_slots(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 600
        cx, cy = w // 2, h // 2
        radius = min(w, h) * 0.35

        n = self.queue.size
        slot_angle = 360 / n
        self.slot_items = []

        for i in range(n):
            angle_deg = -90 + i * slot_angle
            angle = math.radians(angle_deg)
            sx = cx + radius * math.cos(angle)
            sy = cy + radius * math.sin(angle)

            # draw slot as rounded rectangle-like oval
            slot_r = 30
            x0, y0 = sx - slot_r, sy - slot_r
            x1, y1 = sx + slot_r, sy + slot_r

            val = self.queue.data[i]
            if val is None:
                fill = "#e9eef8"  # free
                outline = "#a0b4d9"
            else:
                fill = "#45aaf2"  # occupied
                outline = "#2d98da"

            oval = self.canvas.create_oval(x0, y0, x1, y1, fill=fill, outline=outline, width=2)
            txt = self.canvas.create_text(sx, sy, text=str(val) if val is not None else "", font=("Arial", 10, "bold"), fill="#0b132b")

            # index label near slot
            ix = cx + (radius + 50) * math.cos(angle)
            iy = cy + (radius + 50) * math.sin(angle)
            idx_label = self.canvas.create_text(ix, iy, text=str(i), font=("Arial", 9), fill="#525f7f")

            # head/tail marker
            marker_text = ""
            rel = ""
            if self.queue.count > 0:
                real_idx = (self.queue.front) % n
                tail_idx = (self.queue.front + self.queue.count - 1) % n
                if i == real_idx:
                    marker_text += "F"
                if i == tail_idx:
                    if marker_text:
                        marker_text += "/"
                    marker_text += "R"

            if marker_text:
                self.canvas.create_text(sx, sy - slot_r - 14, text=marker_text, font=("Arial", 9, "bold"), fill="#222f3e")

            self.slot_items.append((oval, txt, idx_label))

        # center label
        self.canvas.create_text(cx, cy, text="Parking Lot", font=("Helvetica", 18, "bold"), fill="#0f1724")

        # occupancy info
        info = f"Slots: {self.queue.size}  |  Occupied: {self.queue.count}  |  Front: {self.queue.front}"
        self.canvas.create_text(10, h - 20, text=info, anchor=tk.W, font=("Arial", 10), fill="#2d3a4a")

    def on_set_size(self):
        try:
            new_size = int(self.size_var.get())
            if new_size < 1:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid size", "Please enter a positive integer for size.")
            return

        # reset queue with new size (preserve order)
        try:
            self.queue.set_size(new_size)
            self.status_label.config(text=f"Size set to {new_size}.")
            self.draw_slots()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_enqueue(self):
        car_id = self.car_entry.get().strip()
        if not car_id:
            car_id = f"Car{self.auto_car_id}"
            self.auto_car_id += 1

        try:
            idx = self.queue.enqueue(car_id)
            self.status_label.config(text=f"Parked {car_id} at slot {idx}.")
            self.car_entry.delete(0, tk.END)
            self.draw_slots()
        except OverflowError:
            messagebox.showwarning("Full", "Parking is full. Cannot park.")

    def on_dequeue(self):
        try:
            car = self.queue.dequeue()
            self.status_label.config(text=f"{car} left the parking.")
            self.draw_slots()
        except IndexError:
            messagebox.showwarning("Empty", "Parking is empty.")

    def on_clear(self):
        if messagebox.askyesno("Clear", "Clear all parked cars?"):
            self.queue.clear()
            self.status_label.config(text="Cleared all slots.")
            self.draw_slots()


if __name__ == "__main__":
    app = ParkingApp()
    # ensure the canvas redraws after window is shown
    def delayed_draw():
        app.draw_slots()

    app.after(200, delayed_draw)
    app.mainloop()
