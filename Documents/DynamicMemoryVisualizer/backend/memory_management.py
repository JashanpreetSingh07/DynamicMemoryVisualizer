# File: backend/memory_management.py

from collections import deque, OrderedDict

# ----------------- Paging Simulator -----------------
class PagingSimulator:
    def __init__(self, num_frames, replacement_algo):
        self.num_frames = num_frames
        self.frames = [None] * num_frames  # list representing physical frames
        self.page_faults = 0
        self.replacement_algo = replacement_algo
        if replacement_algo == "FIFO":
            self.queue = deque()
        elif replacement_algo == "LRU":
            self.lru_order = OrderedDict()
    
    def access_page(self, page):
        if page in self.frames:
            # Page hit: update usage for LRU
            if self.replacement_algo == "LRU":
                self.lru_order.move_to_end(page)
            return False  # No page fault
        else:
            self.page_faults += 1
            self.load_page(page)
            return True  # Page fault occurred
    
    def load_page(self, page):
        if None in self.frames:
            index = self.frames.index(None)
            self.frames[index] = page
            if self.replacement_algo == "FIFO":
                self.queue.append(index)
            elif self.replacement_algo == "LRU":
                self.lru_order[page] = index
        else:
            # When memory is full, replace a page based on the algorithm
            if self.replacement_algo == "FIFO":
                index = self.queue.popleft()
                self.frames[index] = page
                self.queue.append(index)
            elif self.replacement_algo == "LRU":
                # Remove least recently used
                oldest_page, index = self.lru_order.popitem(last=False)
                self.frames[index] = page
                self.lru_order[page] = index
    
    def reset(self):
        self.frames = [None] * self.num_frames
        self.page_faults = 0
        if self.replacement_algo == "FIFO":
            self.queue.clear()
        elif self.replacement_algo == "LRU":
            self.lru_order.clear()

# ------------- Segmentation Simulator -------------
class SegmentationSimulator:
    def __init__(self, total_memory):
        self.total_memory = total_memory
        self.segments = []  # List of tuples: (start, size, label)
        self.free_memory = total_memory
    
    def allocate_segment(self, size, label):
        # Check if enough free memory exists
        if size > self.free_memory:
            return False
        start = 0
        if self.segments:
            # Sort segments by starting address and find a gap
            self.segments.sort(key=lambda x: x[0])
            for seg in self.segments:
                if seg[0] - start >= size:
                    break
                start = seg[0] + seg[1]
            if self.total_memory - start < size:
                return False
        self.segments.append((start, size, label))
        self.free_memory -= size
        return True
    
    def free_segment(self, label):
        for seg in self.segments:
            if seg[2] == label:
                self.segments.remove(seg)
                self.free_memory += seg[1]
                return True
        return False
    
    def reset(self):
        self.segments = []
        self.free_memory = self.total_memory

# ---------- Virtual Memory Simulator -----------
class VirtualMemorySimulator:
    def __init__(self, num_frames):
        self.num_frames = num_frames
        self.physical_memory = [None] * num_frames
        self.page_table = {}  # maps virtual page to physical frame index
        self.page_faults = 0
        self.fifo_queue = deque()
    
    def access_virtual_page(self, vpage):
        if vpage in self.page_table:
            return False  # Page hit
        else:
            self.page_faults += 1
            self.load_virtual_page(vpage)
            return True  # Page fault occurred
    
    def load_virtual_page(self, vpage):
        if None in self.physical_memory:
            index = self.physical_memory.index(None)
            self.physical_memory[index] = vpage
            self.page_table[vpage] = index
            self.fifo_queue.append(index)
        else:
            index = self.fifo_queue.popleft()
            # Remove the virtual page that was in this frame
            for key, value in list(self.page_table.items()):
                if value == index:
                    del self.page_table[key]
                    break
            self.physical_memory[index] = vpage
            self.page_table[vpage] = index
            self.fifo_queue.append(index)
    
    def reset(self):
        self.physical_memory = [None] * self.num_frames
        self.page_table = {}
        self.page_faults = 0
        self.fifo_queue.clear()
