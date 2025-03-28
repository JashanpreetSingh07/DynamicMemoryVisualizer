# File: frontend/main_ui.py

import tkinter as tk
from tkinter import ttk, messagebox
from backend.memory_management import PagingSimulator, SegmentationSimulator, VirtualMemorySimulator

class DynamicMemoryVisualizerApp:
    def __init__(self, master):
        self.master = master
        master.title("Dynamic Memory Management Visualizer")
        self.simulation_type = tk.StringVar(value="Paging")
        
        # Top frame for simulation type selection
        frame_top = tk.Frame(master)
        frame_top.pack(pady=10)
        
        tk.Label(frame_top, text="Select Simulation Type: ").pack(side=tk.LEFT)
        self.sim_type_combo = ttk.Combobox(frame_top, textvariable=self.simulation_type, 
                                           values=["Paging", "Segmentation"], state="readonly")
        self.sim_type_combo.pack(side=tk.LEFT)
        self.sim_type_combo.bind("<<ComboboxSelected>>", self.on_simulation_change)
        
        # Main frame that will contain simulation-specific frames
        self.main_frame = tk.Frame(master)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create separate frames for each simulation type
        self.create_paging_frame()
        self.create_segmentation_frame()
        self.create_virtual_memory_frame()
        
        self.show_frame("Paging")
    
    def on_simulation_change(self, event):
        sim_type = self.simulation_type.get()
        self.show_frame(sim_type)
    
    def show_frame(self, sim_type):
        # Hide all frames first
        self.paging_frame.pack_forget()
        self.segmentation_frame.pack_forget()
        self.virtual_frame.pack_forget()
        # Show the selected simulation frame
        if sim_type == "Paging":
            self.paging_frame.pack(fill=tk.BOTH, expand=True)
        elif sim_type == "Segmentation":
            self.segmentation_frame.pack(fill=tk.BOTH, expand=True)
        elif sim_type == "Virtual Memory":
            self.virtual_frame.pack(fill=tk.BOTH, expand=True)
    
    # ----------------- Paging Frame -----------------
    def create_paging_frame(self):
        self.paging_frame = tk.Frame(self.main_frame)
        # Input: Number of Frames
        # In frontend/main_ui.py inside create_paging_frame()
        self.canvas = tk.Canvas(self.paging_frame, width=400, height=100, bg="white")
        self.canvas.grid(row=7, column=0, columnspan=2, pady=5)

        tk.Label(self.paging_frame, text="Number of Frames:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.frames_entry = tk.Entry(self.paging_frame)
        self.frames_entry.grid(row=0, column=1, padx=5, pady=5)
        self.frames_entry.insert(0, "4")
        
        # Input: Replacement Algorithm
        tk.Label(self.paging_frame, text="Replacement Algorithm:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.algo_var = tk.StringVar(value="FIFO")
        self.algo_combo = ttk.Combobox(self.paging_frame, textvariable=self.algo_var, 
                                       values=["FIFO", "LRU"], state="readonly")
        self.algo_combo.grid(row=1, column=1, padx=5, pady=5)
        
        # Input: Page to Access
        tk.Label(self.paging_frame, text="Page to Access (integer):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.page_entry = tk.Entry(self.paging_frame)
        self.page_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Button to access page
        self.access_button = tk.Button(self.paging_frame, text="Access Page", command=self.access_page)
        self.access_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Status display
        self.paging_status = tk.Label(self.paging_frame, text="Status: ")
        self.paging_status.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Reset button
        self.reset_paging_button = tk.Button(self.paging_frame, text="Reset Paging", command=self.reset_paging)
        self.reset_paging_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Frames display
        self.frames_display = tk.Label(self.paging_frame, text="Frames: []")
        self.frames_display.grid(row=6, column=0, columnspan=2, pady=5)
        
        self.paging_simulator = None
    
    def access_page(self):
        try:
            num_frames = int(self.frames_entry.get())
            algo = self.algo_var.get()
            # Initialize simulator on first use or when settings change
            if self.paging_simulator is None:
                self.paging_simulator = PagingSimulator(num_frames, algo)
            page = int(self.page_entry.get())
            fault = self.paging_simulator.access_page(page)
            status = f"Accessed page {page}. "
            status += "Page fault occurred. " if fault else "Page hit. "
            status += f"Total faults: {self.paging_simulator.page_faults}."
            self.paging_status.config(text="Status: " + status)
            self.frames_display.config(text="Frames: " + str(self.paging_simulator.frames))
            self.update_canvas()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def reset_paging(self):
        if self.paging_simulator:
            self.paging_simulator.reset()
            self.paging_status.config(text="Status: Reset done.")
            self.frames_display.config(text="Frames: " + str(self.paging_simulator.frames))
            self.update_canvas()
    
    # ----------------- Segmentation Frame -----------------
    def create_segmentation_frame(self):
        self.segmentation_frame = tk.Frame(self.main_frame)
        # Input: Total Memory Size
        tk.Label(self.segmentation_frame, text="Total Memory Size:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.total_memory_entry = tk.Entry(self.segmentation_frame)
        self.total_memory_entry.grid(row=0, column=1, padx=5, pady=5)
        self.total_memory_entry.insert(0, "100")
        
        # Input: Segment Size
        tk.Label(self.segmentation_frame, text="Segment Size:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.segment_size_entry = tk.Entry(self.segmentation_frame)
        self.segment_size_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Input: Segment Label
        tk.Label(self.segmentation_frame, text="Segment Label:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.segment_label_entry = tk.Entry(self.segmentation_frame)
        self.segment_label_entry.grid(row=2, column=1, padx=5, pady=5)
        
        # Buttons for allocation and freeing
        self.allocate_segment_button = tk.Button(self.segmentation_frame, text="Allocate Segment", command=self.allocate_segment)
        self.allocate_segment_button.grid(row=3, column=0, columnspan=2, pady=5)
        self.free_segment_button = tk.Button(self.segmentation_frame, text="Free Segment", command=self.free_segment)
        self.free_segment_button.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Status display
        self.segmentation_status = tk.Label(self.segmentation_frame, text="Status: ")
        self.segmentation_status.grid(row=5, column=0, columnspan=2, pady=5)
        
        # Display allocated segments
        self.segments_display = tk.Label(self.segmentation_frame, text="Segments: []")
        self.segments_display.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Add Canvas for graphical visualization of segmentation
        self.seg_canvas = tk.Canvas(self.segmentation_frame, width=400, height=100, bg="white")
        self.seg_canvas.grid(row=7, column=0, columnspan=2, pady=10)
        self.segmentation_simulator = None
    
    def update_segmentation_canvas(self):
    # Clear the canvas
        self.seg_canvas.delete("all")
    
        if self.segmentation_simulator is None:
            return

        total_memory = self.segmentation_simulator.total_memory
        canvas_width = 400
        canvas_height = 100

    # Draw a background rectangle representing the total memory
        self.seg_canvas.create_rectangle(5, 20, canvas_width-5, canvas_height-20, outline="black", fill="lightgrey")
    
    # Sort segments by their start address to draw in order
        segments = sorted(self.segmentation_simulator.segments, key=lambda x: x[0])
    
        for seg in segments:
            start, size, label = seg
        # Calculate x coordinates relative to the total memory
            x0 = 5 + (start / total_memory) * (canvas_width - 10)
            x1 = 5 + ((start + size) / total_memory) * (canvas_width - 10)
        # Draw the segment as a rectangle with a distinct color
            self.seg_canvas.create_rectangle(x0, 20, x1, canvas_height-20, fill="lightblue", outline="black")
        # Place the segment's label in the middle of the rectangle
            self.seg_canvas.create_text((x0+x1)/2, canvas_height/2, text=label, font=("Arial", 12, "bold"))

    def allocate_segment(self):
        try:
            total_memory = int(self.total_memory_entry.get())
            if self.segmentation_simulator is None:
                self.segmentation_simulator = SegmentationSimulator(total_memory)
            size = int(self.segment_size_entry.get())
            label = self.segment_label_entry.get()
            success = self.segmentation_simulator.allocate_segment(size, label)
            status = f"Segment '{label}' allocated." if success else "Allocation failed. Not enough memory."
            self.segmentation_status.config(text="Status: " + status)
            self.segments_display.config(text="Segments: " + str(self.segmentation_simulator.segments))
            self.update_segmentation_canvas()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def free_segment(self):
        try:
            label = self.segment_label_entry.get()
            if self.segmentation_simulator is None:
                messagebox.showerror("Error", "No segments allocated yet.")
                return
            success = self.segmentation_simulator.free_segment(label)
            status = f"Segment '{label}' freed." if success else "Segment not found."
            self.segmentation_status.config(text="Status: " + status)
            self.segments_display.config(text="Segments: " + str(self.segmentation_simulator.segments))
            self.update_segmentation_canvas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_vm_canvas(self):
    # Clear the canvas
        self.vm_canvas.delete("all")
        if not self.virtual_simulator:
            return

    # Retrieve the physical memory state
        frames = self.virtual_simulator.physical_memory
        num_frames = len(frames)
        canvas_width = 400
        rect_width = canvas_width // num_frames

    # Draw each frame as a colored rectangle
        for i, vpage in enumerate(frames):
            x0 = i * rect_width + 5
            y0 = 20
            x1 = (i + 1) * rect_width - 5
            y1 = 100
            self.vm_canvas.create_rectangle(x0, y0, x1, y1, fill="lightgreen", outline="black")
        
        # Show the virtual page number if available
            display_text = str(vpage) if vpage is not None else ""
            self.vm_canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=display_text, font=("Arial", 14, "bold"))

    def update_canvas(self):
    # Clear the canvas
        self.canvas.delete("all")
        if not self.paging_simulator:
            return

        frames = self.paging_simulator.frames
        num_frames = len(frames)
        canvas_width = 400
        rect_width = canvas_width // num_frames

        for i, page in enumerate(frames):
            x0 = i * rect_width + 5
            y0 = 20
            x1 = (i + 1) * rect_width - 5
            y1 = 80
        # Draw rectangle for each frame
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="lightblue", outline="black")
        # Draw text (page number) inside the rectangle
            display_text = str(page) if page is not None else ""
            self.canvas.create_text((x0 + x1) / 2, (y0 + y1) / 2, text=display_text, font=("Arial", 14))

    # --------------- Virtual Memory Frame ---------------
    # def create_virtual_memory_frame(self):
    #     self.virtual_frame = tk.Frame(self.main_frame)
    #     # Input: Number of Frames for physical memory
    #     tk.Label(self.virtual_frame, text="Number of Frames (Physical Memory):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    #     self.vm_frames_entry = tk.Entry(self.virtual_frame)
    #     self.vm_frames_entry.grid(row=0, column=1, padx=5, pady=5)
    #     self.vm_frames_entry.insert(0, "4")
        
    #     # Input: Virtual Page to Access
    #     tk.Label(self.virtual_frame, text="Virtual Page to Access:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    #     self.virtual_page_entry = tk.Entry(self.virtual_frame)
    #     self.virtual_page_entry.grid(row=1, column=1, padx=5, pady=5)
        
    #     # Button to access virtual page
    #     self.vm_access_button = tk.Button(self.virtual_frame, text="Access Virtual Page", command=self.access_virtual_page)
    #     self.vm_access_button.grid(row=2, column=0, columnspan=2, pady=5)
        
    #     # Status display
    #     self.virtual_status = tk.Label(self.virtual_frame, text="Status: ")
    #     self.virtual_status.grid(row=3, column=0, columnspan=2, pady=5)
        
    #     # Physical memory display
    #     self.virtual_display = tk.Label(self.virtual_frame, text="Physical Memory: []")
    #     self.virtual_display.grid(row=4, column=0, columnspan=2, pady=5)
        
    #     self.virtual_simulator = None
    def create_virtual_memory_frame(self):
        self.virtual_frame = tk.Frame(self.main_frame)
        # Input: Number of Frames for physical memory
        tk.Label(self.virtual_frame, text="Number of Frames (Physical Memory):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.vm_frames_entry = tk.Entry(self.virtual_frame)
        self.vm_frames_entry.grid(row=0, column=1, padx=5, pady=5)
        self.vm_frames_entry.insert(0, "4")

        # Input: Virtual Page to Access
        tk.Label(self.virtual_frame, text="Virtual Page to Access:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.virtual_page_entry = tk.Entry(self.virtual_frame)
        self.virtual_page_entry.grid(row=1, column=1, padx=5, pady=5)

        # Button to access virtual page
        self.vm_access_button = tk.Button(self.virtual_frame, text="Access Virtual Page", command=self.access_virtual_page)
        self.vm_access_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Status display
        self.virtual_status = tk.Label(self.virtual_frame, text="Status: ")
        self.virtual_status.grid(row=3, column=0, columnspan=2, pady=5)

        # Physical memory display (textual)
        self.virtual_display = tk.Label(self.virtual_frame, text="Physical Memory: []")
        self.virtual_display.grid(row=4, column=0, columnspan=2, pady=5)

        # **New Canvas for Graphical Visualization**
        self.vm_canvas = tk.Canvas(self.virtual_frame, width=400, height=120, bg="white")
        self.vm_canvas.grid(row=5, column=0, columnspan=2, pady=10)

        self.virtual_simulator = None

    def access_virtual_page(self):
        try:
            num_frames = int(self.vm_frames_entry.get())
            if self.virtual_simulator is None:
                self.virtual_simulator = VirtualMemorySimulator(num_frames)
            vpage = int(self.virtual_page_entry.get())
            fault = self.virtual_simulator.access_virtual_page(vpage)
            status = f"Accessed virtual page {vpage}. "
            status += "Page fault occurred. " if fault else "Page hit. "
            status += f"Total faults: {self.virtual_simulator.page_faults}."
            self.virtual_status.config(text="Status: " + status)
            self.virtual_display.config(text="Physical Memory: " + str(self.virtual_simulator.physical_memory))
            self.update_vm_canvas()
        except Exception as e:
            messagebox.showerror("Error", str(e))

# If this module is run directly (for testing), launch the UI.
if __name__ == "__main__":
    root = tk.Tk()
    app = DynamicMemoryVisualizerApp(root)
    root.mainloop()
