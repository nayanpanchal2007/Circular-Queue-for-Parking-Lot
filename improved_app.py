import math
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class ParkingQueue:
    """Circular queue for parking slots."""

    def __init__(self, size=8):
        if size < 1:
            raise ValueError("Size must be >= 1")
        self.size = size
        self.data = [None] * size
        self.front = 0  # index of first element
        self.count = 0

    # ---------- Basic helpers ----------
    def is_full(self):
        return self.count == self.size

    def is_empty(self):
        return self.count == 0

    # ---------- Core operations ----------
    def enqueue(self, value):
        """
        value is a dict:
        {
            "id": str,
            "entry_time": datetime
        }
        """
        if self.is_full():
            raise OverflowError("Parking is full")
        idx = (self.front + self.count) % self.size
        self.data[idx] = value
        self.count += 1
        return idx  # physical index used

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Parking is empty")
        val = self.data[self.front]
        self.data[self.front] = None
        self.front = (self.front + 1) % self.size
        self.count -= 1
        return val

    def peek_front(self):
        if self.is_empty():
            raise IndexError("Parking is empty")
        return self.data[self.front]

    def clear(self):
        self.data = [None] * self.size
        self.front = 0
        self.count = 0

    def set_size(self, new_size):
        """Resize queue, preserving items in logical order."""
        if new_size < 1:
            raise ValueError("Size must be >= 1")
        items = [self.data[(self.front + i) % self.size] for i in range(self.count)]
        self.size = new_size
        self.data = [None] * new_size
        self.front = 0
        self.count = 0
        for it in items[:new_size]:
            if it is not None:
                self.enqueue(it)

    # ---------- Extended operations ----------
    def find_index_by_car_id(self, car_id):
        """
        Returns physical index of car with given id, or None if not found.
        """
        for i in range(self.size):
            car = self.data[i]
            if car is not None and car.get("id") == car_id:
                return i
        return None

    def remove_by_car_id(self, car_id):
        """
        Remove a car by ID from the circular queue, maintaining logical order.
        Returns removed car dict or None if not found.
        """
        if self.is_empty():
            return None

        items = [self.data[(self.front + i) % self.size] for i in range(self.count)]
        new_items = []
        removed = None

        for it in items:
            if it is not None and it.get("id") == car_id and removed is None:
                removed = it
                # skip adding this one => deleted
            else:
                new_items.append(it)

        if removed is None:
            return None

        # rebuild queue from new_items
        self.data = [None] * self.size
        self.front = 0
        self.count = 0
        for it in new_items:
            if it is not None:
                self.enqueue(it)

        return removed


class ParkingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Circular Queue - Parking Lot")
        self.configure(bg="#f5f7fa")
        self.geometry("1000x720")

        # core DS
        self.queue = ParkingQueue(size=8)
        self.auto_car_id = 1

        # for UI highlighting
        self.last_action_index = None
        self.last_action_type = None  # "enqueue", "dequeue", "search"

        # build UI
        self._build_controls()
        self._build_dashboard()
        self._build_canvas()
        self.draw_slots()
        self.update_dashboard()

    # ---------- UI builders ----------
    def _build_controls(self):
        ctrl = tk.Frame(self, bg="#f5f7fa")
        ctrl.pack(side=tk.TOP, fill=tk.X, padx=12, pady=8)

        # size controls
        tk.Label(ctrl, text="Parking size:", bg="#f5f7fa", fg="#1e272e",
                 font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.size_var = tk.IntVar(value=self.queue.size)
        self.size_entry = tk.Entry(ctrl, textvariable=self.size_var, width=6)
        self.size_entry.pack(side=tk.LEFT, padx=(4, 10))

        set_btn = tk.Button(ctrl, text="Set Size", command=self.on_set_size,
                            bg="#4b7bec", fg="white", relief=tk.FLAT,
                            font=("Segoe UI", 9, "bold"))
        set_btn.pack(side=tk.LEFT, padx=4)

        # car ID input
        tk.Label(ctrl, text="Car ID:", bg="#f5f7fa", fg="#1e272e",
                 font=("Segoe UI", 10)).pack(side=tk.LEFT, padx=(20, 4))
        self.car_entry = tk.Entry(ctrl, width=14)
        self.car_entry.pack(side=tk.LEFT)

        # main operations
        btn_style = dict(relief=tk.FLAT, font=("Segoe UI", 9, "bold"), padx=8, pady=2)

        enq_btn = tk.Button(ctrl, text="Enqueue (Park)", command=self.on_enqueue,
                            bg="#20bf6b", fg="white", **btn_style)
        enq_btn.pack(side=tk.LEFT, padx=6)

        deq_btn = tk.Button(ctrl, text="Dequeue (Leave)", command=self.on_dequeue,
                            bg="#eb3b5a", fg="white", **btn_style)
        deq_btn.pack(side=tk.LEFT, padx=6)

        peek_btn = tk.Button(ctrl, text="Peek Front", command=self.on_peek_front,
                             bg="#45aaf2", fg="white", **btn_style)
        peek_btn.pack(side=tk.LEFT, padx=6)

        search_btn = tk.Button(ctrl, text="Search Car", command=self.on_search_car,
                               bg="#a55eea", fg="white", **btn_style)
        search_btn.pack(side=tk.LEFT, padx=6)

        remove_btn = tk.Button(ctrl, text="Remove Car", command=self.on_remove_car,
                               bg="#fd9644", fg="white", **btn_style)
        remove_btn.pack(side=tk.LEFT, padx=6)

        reset_btn = tk.Button(ctrl, text="Clear All", command=self.on_clear,
                              bg="#3867d6", fg="white", **btn_style)
        reset_btn.pack(side=tk.RIGHT, padx=4)

        # status line
        status = tk.Frame(self, bg="#f5f7fa")
        status.pack(side=tk.TOP, fill=tk.X, padx=12, pady=(0, 4))
        self.status_label = tk.Label(
            status,
            text="Welcome — set size and start parking cars.",
            anchor=tk.W,
            bg="#dfe4ea",
            fg="#2f3542",
            font=("Segoe UI", 9)
        )
        self.status_label.pack(fill=tk.X)

    def _build_dashboard(self):
        dash = tk.Frame(self, bg="#f5f7fa")
        dash.pack(side=tk.TOP, fill=tk.X, padx=12, pady=(0, 8))

        card_bg = "#ffffff"
        card_fg = "#2f3542"
        card_font_title = ("Segoe UI", 9, "bold")
        card_font_val = ("Consolas", 11, "bold")

        def make_card(parent, title):
            frame = tk.Frame(parent, bg=card_bg, bd=0, highlightthickness=1,
                             highlightbackground="#dcdde1")
            lbl_title = tk.Label(frame, text=title, bg=card_bg, fg="#8395a7",
                                 font=card_font_title)
            lbl_title.pack(anchor=tk.W, padx=8, pady=(4, 0))
            lbl_val = tk.Label(frame, text="-", bg=card_bg, fg=card_fg,
                               font=card_font_val)
            lbl_val.pack(anchor=tk.W, padx=8, pady=(0, 6))
            return frame, lbl_val

        self.card_size, self.lbl_size = make_card(dash, "Total Slots")
        self.card_size.pack(side=tk.LEFT, padx=5)

        self.card_occ, self.lbl_occ = make_card(dash, "Occupied")
        self.card_occ.pack(side=tk.LEFT, padx=5)

        self.card_free, self.lbl_free = make_card(dash, "Free")
        self.card_free.pack(side=tk.LEFT, padx=5)

        self.card_front, self.lbl_front = make_card(dash, "Front Index")
        self.card_front.pack(side=tk.LEFT, padx=5)

        self.card_rear, self.lbl_rear = make_card(dash, "Rear Index")
        self.card_rear.pack(side=tk.LEFT, padx=5)

    def _build_canvas(self):
        self.canvas_frame = tk.Frame(self, bg="#f5f7fa")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        self.canvas = tk.Canvas(self.canvas_frame, bg="#ffffff", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Configure>", lambda event: self.draw_slots())

    # ---------- Dashboard ----------
    def update_dashboard(self):
        size = self.queue.size
        occ = self.queue.count
        free = size - occ
        front = self.queue.front if not self.queue.is_empty() else "-"
        rear = (self.queue.front + self.queue.count - 1) % self.queue.size if not self.queue.is_empty() else "-"

        self.lbl_size.config(text=str(size))
        self.lbl_occ.config(text=str(occ))
        self.lbl_free.config(text=str(free))
        self.lbl_front.config(text=str(front))
        self.lbl_rear.config(text=str(rear))

    # ---------- Drawing ----------
    def draw_slots(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width() or 800
        h = self.canvas.winfo_height() or 600
        cx, cy = w // 2, h // 2
        radius = min(w, h) * 0.35

        n = self.queue.size
        if n <= 0:
            return

        slot_angle = 360 / n
        self.slot_items = []

        for i in range(n):
            angle_deg = -90 + i * slot_angle
            angle = math.radians(angle_deg)
            sx = cx + radius * math.cos(angle)
            sy = cy + radius * math.sin(angle)

            slot_r = 32
            x0, y0 = sx - slot_r, sy - slot_r
            x1, y1 = sx + slot_r, sy + slot_r

            val = self.queue.data[i]

            # base colors
            if val is None:
                fill = "#f1f3f8"  # free
                outline = "#ced6e0"
            else:
                fill = "#74b9ff"  # occupied
                outline = "#0984e3"

            # highlight last operation
            if self.last_action_index is not None and i == self.last_action_index:
                outline = "#ff7675" if self.last_action_type in ("dequeue", "remove") else "#00b894"
                self.canvas.create_oval(
                    x0 - 4, y0 - 4, x1 + 4, y1 + 4,
                    outline=outline, width=2, dash=(3, 2)
                )

            oval = self.canvas.create_oval(x0, y0, x1, y1, fill=fill, outline=outline, width=2)

            # show car ID (if any)
            if val is not None:
                text = val.get("id", "")
            else:
                text = ""

            txt = self.canvas.create_text(
                sx, sy,
                text=str(text),
                font=("Segoe UI", 9, "bold"),
                fill="#2f3542"
            )

            # index label outside
            ix = cx + (radius + 55) * math.cos(angle)
            iy = cy + (radius + 55) * math.sin(angle)
            idx_label = self.canvas.create_text(ix, iy, text=str(i),
                                                font=("Segoe UI", 8),
                                                fill="#57606f")

            # markers for Front / Rear
            marker_text = ""
            if self.queue.count > 0:
                real_front = self.queue.front % n
                tail_idx = (self.queue.front + self.queue.count - 1) % n
                if i == real_front:
                    marker_text += "F"
                if i == tail_idx:
                    if marker_text:
                        marker_text += "/"
                    marker_text += "R"

            if marker_text:
                self.canvas.create_text(
                    sx, sy - slot_r - 12,
                    text=marker_text,
                    font=("Segoe UI", 8, "bold"),
                    fill="#2d3436"
                )

            self.slot_items.append((oval, txt, idx_label))

        # center title
        self.canvas.create_text(
            cx, cy,
            text="Parking Lot (Circular Queue)",
            font=("Segoe UI", 16, "bold"),
            fill="#2f3542"
        )

        # info footer
        info = f"Slots: {self.queue.size}  |  Occupied: {self.queue.count}  |  Front: {self.queue.front}"
        self.canvas.create_text(
            10, h - 20,
            text=info,
            anchor=tk.W,
            font=("Segoe UI", 9),
            fill="#57606f"
        )

    # ---------- UI event handlers ----------
    def on_set_size(self):
        try:
            new_size = int(self.size_var.get())
            if new_size < 1:
                raise ValueError
        except Exception:
            messagebox.showerror("Invalid size", "Please enter a positive integer for size.")
            return

        try:
            self.queue.set_size(new_size)
            self.status_label.config(text=f"Size set to {new_size}. Existing cars preserved (up to new size).")
            self.last_action_index = None
            self.draw_slots()
            self.update_dashboard()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_enqueue(self):
        car_id = self.car_entry.get().strip()
        if not car_id:
            car_id = f"Car{self.auto_car_id}"
            self.auto_car_id += 1

        car_obj = {
            "id": car_id,
            "entry_time": datetime.now()
        }

        try:
            idx = self.queue.enqueue(car_obj)
            self.status_label.config(text=f"Parked {car_id} at slot {idx}.")
            self.car_entry.delete(0, tk.END)
            self.last_action_index = idx
            self.last_action_type = "enqueue"
            self.draw_slots()
            self.update_dashboard()
        except OverflowError:
            messagebox.showwarning("Parking Full", "Parking is full. Cannot park more cars.")

    def _format_time(self, dt):
        return dt.strftime("%H:%M:%S")

    def _format_duration(self, start, end):
        delta = end - start
        total_sec = int(delta.total_seconds())
        mins = total_sec // 60
        secs = total_sec % 60
        return f"{mins} min {secs} sec"

    def on_dequeue(self):
        try:
            car = self.queue.dequeue()
            exit_time = datetime.now()
            entry_time = car["entry_time"]
            duration_str = self._format_duration(entry_time, exit_time)

            msg = (
                f"Car {car['id']} left the parking.\n"
                f"Entry time : {self._format_time(entry_time)}\n"
                f"Exit time  : {self._format_time(exit_time)}\n"
                f"Duration   : {duration_str}"
            )
            self.status_label.config(text=f"{car['id']} left the parking. Duration: {duration_str}.")
            messagebox.showinfo("Car Left", msg)

            self.last_action_index = self.queue.front  # new front after dequeue
            self.last_action_type = "dequeue"
            self.draw_slots()
            self.update_dashboard()
        except IndexError:
            messagebox.showwarning("Parking Empty", "Parking is empty. No car to dequeue.")

    def on_peek_front(self):
        try:
            car = self.queue.peek_front()
            entry_time = car["entry_time"]
            msg = (
                f"Next car to leave (front):\n"
                f"Car ID    : {car['id']}\n"
                f"Entry time: {self._format_time(entry_time)}"
            )
            self.status_label.config(text=f"Front car is {car['id']} (will leave first).")
            self.last_action_index = self.queue.front
            self.last_action_type = "search"
            self.draw_slots()
            self.update_dashboard()
            messagebox.showinfo("Peek Front", msg)
        except IndexError:
            messagebox.showinfo("Parking Empty", "No car is currently parked.")

    def on_search_car(self):
        car_id = self.car_entry.get().strip()
        if not car_id:
            messagebox.showwarning("Car ID missing", "Enter a Car ID in the box to search.")
            return

        idx = self.queue.find_index_by_car_id(car_id)
        if idx is None:
            self.status_label.config(text=f"Car {car_id} not found in parking.")
            messagebox.showinfo("Search Result", f"Car {car_id} not found.")
            self.last_action_index = None
        else:
            self.status_label.config(text=f"Car {car_id} found at slot {idx}.")
            messagebox.showinfo("Search Result", f"Car {car_id} is at slot {idx}.")
            self.last_action_index = idx
            self.last_action_type = "search"

        self.draw_slots()
        self.update_dashboard()

    def on_remove_car(self):
        car_id = self.car_entry.get().strip()
        if not car_id:
            messagebox.showwarning("Car ID missing", "Enter a Car ID in the box to remove.")
            return

        removed = self.queue.remove_by_car_id(car_id)
        if removed is None:
            self.status_label.config(text=f"Car {car_id} not found. Nothing removed.")
            messagebox.showinfo("Remove Result", f"Car {car_id} not found in parking.")
            self.last_action_index = None
        else:
            exit_time = datetime.now()
            entry_time = removed["entry_time"]
            duration_str = self._format_duration(entry_time, exit_time)
            msg = (
                f"Car {removed['id']} removed from queue.\n"
                f"Entry time : {self._format_time(entry_time)}\n"
                f"Exit time  : {self._format_time(exit_time)}\n"
                f"Duration   : {duration_str}"
            )
            self.status_label.config(text=f"Car {car_id} removed. Duration: {duration_str}.")
            messagebox.showinfo("Car Removed", msg)
            # After rebuild, front is at index 0 logically, we don't know old physical index
            self.last_action_index = self.queue.front if not self.queue.is_empty() else None
            self.last_action_type = "remove"

        self.draw_slots()
        self.update_dashboard()

    def on_clear(self):
        if messagebox.askyesno("Clear All", "Clear all parked cars?"):
            self.queue.clear()
            self.status_label.config(text="Cleared all slots.")
            self.last_action_index = None
            self.draw_slots()
            self.update_dashboard()


if __name__ == "__main__":
    app = ParkingApp()

    # ensure the canvas redraws after window is shown
    def delayed_draw():
        app.draw_slots()

    app.after(200, delayed_draw)
    app.mainloop()
