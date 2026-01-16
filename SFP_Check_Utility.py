import epics
import sys
import os
import time
import statistics
import numpy as np
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- IMPORT ADDRESS BOOK ---
try:
    from bpm_addresses import srbpm
except ImportError:
    print("CRITICAL ERROR: Could not import 'bpm_addresses.py'.")
    sys.exit(1)

# ==============================================================================
# CONFIGURATION
# ==============================================================================
SIGMA_THRESHOLD = 1.0 
CHUNK_SIZE = 100 

CW_FAULT_SUFFIXES = ["Sdi:Cw-LossCnt-I", "Sdi:CW_CrcErrorCnt-I", "Sdi:CW_LbLoPacketTO-I", "Sdi:CW_RePacketTO-I"]
CCW_FAULT_SUFFIXES = ["Sdi:Cw-LossCnt-I", "Sdi:CW_CrcErrorCnt-I", "Sdi:CW_LbLoPacketTO-I", "Sdi:CW_RePacketTO-I"]
SFP_SUFFIXES = ["SFP1:RxPow-I", "SFP2:RxPow-I"]
CLEAR_SUFFIX = "Sdi:RegClr-SP"

class SFPAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SFP Power & Fault Manager")
        self.root.geometry("1400x900")
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        # --- 1. SETUP GUI LAYOUT ---
        self.frame_top = tk.Frame(root)
        self.frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.frame_controls = tk.Frame(root, height=50, bg="#dddddd")
        self.frame_controls.pack(side=tk.BOTTOM, fill=tk.X)
        self.frame_plot = tk.Frame(self.frame_top)
        self.frame_plot.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.frame_right = tk.Frame(self.frame_top, width=500)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tabs = ttk.Notebook(self.frame_right)
        self.tabs.pack(fill=tk.BOTH, expand=True)
        
        self.tab_sfp = tk.Frame(self.tabs)
        self.tabs.add(self.tab_sfp, text="SFP Power Analysis")
        self.setup_sfp_table()

        self.tab_faults = tk.Frame(self.tabs)
        self.tabs.add(self.tab_faults, text="Active Faults")
        self.setup_fault_table()

        # --- 2. CONTROLS ---
        self.btn_refresh = tk.Button(self.frame_controls, text="Re-Acquire Data", 
                                     font=("Arial", 12, "bold"), bg="#ccffcc",
                                     command=self.start_acquisition)
        self.btn_refresh.pack(side=tk.LEFT, padx=20, pady=10)

        self.btn_clear = tk.Button(self.frame_controls, text="CLEAR ALL FAULTS", 
                                   font=("Arial", 12, "bold"), bg="#ffcccc", fg="red",
                                   command=self.confirm_clear_faults)
        self.btn_clear.pack(side=tk.RIGHT, padx=20, pady=10)

        self.lbl_status = tk.Label(self.frame_controls, text="Ready", bg="#dddddd", font=("Arial", 10))
        self.lbl_status.pack(side=tk.LEFT, padx=10)

        # --- 3. MATPLOTLIB SETUP ---
        self.fig = plt.Figure(figsize=(10, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame_plot)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # --- 4. PREPARE DATA ---
        self.targets = self.prepare_targets()
        self.clear_pvs = self.prepare_clear_targets()
        
        self.start_acquisition()

    def on_close(self):
        print("Closing application and terminating CA context...")
        self.root.destroy()
        os._exit(0)

    # --- SORTING FUNCTIONALITY ---
    def sort_column(self, tv, col, reverse):
        """Sorts treeview contents when header is clicked."""
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        
        # Try to sort as numbers first, fallback to string
        try:
            l.sort(key=lambda t: float(t[0]), reverse=reverse)
        except ValueError:
            l.sort(reverse=reverse)

        # Rearrange items in sorted order
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # Reset heading command to toggle reverse direction next time
        tv.heading(col, command=lambda: self.sort_column(tv, col, not reverse))

    def setup_sfp_table(self):
        cols = ("Cell", "BPM", "Link", "Power", "Sigma")
        self.tree_sfp = ttk.Treeview(self.tab_sfp, columns=cols, show='headings')
        
        for col in cols:
            self.tree_sfp.heading(col, text=col, command=lambda c=col: self.sort_column(self.tree_sfp, c, False))
            self.tree_sfp.column(col, anchor="center")
        
        # Specific widths
        self.tree_sfp.column("Cell", width=60)
        self.tree_sfp.column("BPM", width=60)
        self.tree_sfp.column("Link", width=60) # Shows CW/CCW
        self.tree_sfp.column("Power", width=80)
        self.tree_sfp.column("Sigma", width=80)
        
        vsb = ttk.Scrollbar(self.tab_sfp, orient="vertical", command=self.tree_sfp.yview)
        self.tree_sfp.configure(yscrollcommand=vsb.set)
        self.tree_sfp.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree_sfp.tag_configure('dead', background='#ffcccc') 
        self.tree_sfp.tag_configure('weak', background='#ffeebb')
        self.tree_sfp.tag_configure('normal', background='white')

    def setup_fault_table(self):
        cols = ("Cell", "BPM", "Fault", "Count")
        self.tree_faults = ttk.Treeview(self.tab_faults, columns=cols, show='headings')
        
        for col in cols:
            self.tree_faults.heading(col, text=col, command=lambda c=col: self.sort_column(self.tree_faults, c, False))
        
        self.tree_faults.column("Cell", width=60, anchor="center")
        self.tree_faults.column("BPM", width=60, anchor="center")
        self.tree_faults.column("Fault", width=180, anchor="w")
        self.tree_faults.column("Count", width=60, anchor="center")
        
        vsb = ttk.Scrollbar(self.tab_faults, orient="vertical", command=self.tree_faults.yview)
        self.tree_faults.configure(yscrollcommand=vsb.set)
        self.tree_faults.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_faults.tag_configure('fault', background='#ffcccc')

    def prepare_targets(self):
        targets = []
        for i in range(30):
            if i >= len(srbpm): break
            cell_id = i + 1
            for item in srbpm[i]:
                if len(item) > 3:
                    prefix = item[3]
                    try: bpm_num = prefix.split("BPM:")[-1].replace("}", "")
                    except: bpm_num = "?"
                    bpm_name = prefix.split("}")[-1] if "}" in prefix else prefix
                    
                    # SFP Targets
                    for suffix in SFP_SUFFIXES:
                        pv = f"{prefix}{suffix}"
                        # DETERMINE CW/CCW LABEL
                        raw_sfp = suffix.split(":")[0] # "SFP1" or "SFP2"
                        link_label = "CW" if "SFP1" in raw_sfp else "CCW"

                        lbl = f"C{cell_id:02d} {bpm_name} {link_label}"
                        targets.append({
                            'pv': pv, 'label': lbl, 'type': 'SFP', 
                            'cell': cell_id, 'cell_str': f"C{cell_id:02d}",
                            'bpm_num': bpm_num, 'link_label': link_label
                        })
                    
                    # FAULT Targets
                    for suffix in CW_FAULT_SUFFIXES + CCW_FAULT_SUFFIXES:
                        pv = f"{prefix}{suffix}"
                        short_fault = suffix.replace("Sdi:", "").replace("-I", "")
                        lbl = f"C{cell_id:02d} {bpm_name}"
                        targets.append({
                            'pv': pv, 'label': lbl, 'type': 'FAULT',
                            'cell': cell_id, 'cell_str': f"C{cell_id:02d}",
                            'bpm_num': bpm_num, 'fault_name': short_fault
                        })
        return targets

    def prepare_clear_targets(self):
        pvs = []
        for i in range(30):
            if i >= len(srbpm): break
            for item in srbpm[i]:
                if len(item) > 3:
                    prefix = item[3]
                    pvs.append(f"{prefix}{CLEAR_SUFFIX}")
        return pvs

    def start_acquisition(self):
        self.btn_refresh.config(state="disabled")
        self.lbl_status.config(text="Acquiring Data...", fg="blue")
        threading.Thread(target=self.collect_data, daemon=True).start()

    def collect_data(self):
        all_pvs = [t['pv'] for t in self.targets]
        all_values = []
        total = len(all_pvs)
        
        for i in range(0, total, CHUNK_SIZE):
            chunk = all_pvs[i:i + CHUNK_SIZE]
            chunk_values = epics.caget_many(chunk)
            all_values.extend(chunk_values)
            progress_pct = int((i/total)*100)
            self.root.after(0, lambda p=progress_pct: self.lbl_status.config(text=f"Acquiring... {p}%"))

        self.root.after(0, lambda: self.process_and_update(all_values))

    def process_and_update(self, all_values):
        self.tree_sfp.delete(*self.tree_sfp.get_children())
        self.tree_faults.delete(*self.tree_faults.get_children())
        self.ax.clear()

        results_list = list(zip(self.targets, all_values))
        sfp_valid_values = [v for t, v in results_list if t['type']=='SFP' and v is not None and v > 1.0]

        if sfp_valid_values:
            global_mean = statistics.mean(sfp_valid_values)
            global_stdev = statistics.stdev(sfp_valid_values)
            limit = global_mean - (SIGMA_THRESHOLD * global_stdev)
        else:
            global_mean = 0; global_stdev = 1; limit = 0

        plot_data = []
        cell_boundaries = []
        current_cell = 0
        idx = 0
        fault_count_total = 0

        for target, val in results_list:
            if val is None: val = 0
            
            # --- FAULTS ---
            if target['type'] == 'FAULT':
                if val > 0:
                    self.tree_faults.insert("", "end", 
                        values=(target['cell_str'], target['bpm_num'], target['fault_name'], int(val)), 
                        tags=('fault',))
                    fault_count_total += 1
                continue

            # --- SFP ---
            if target['cell'] != current_cell:
                cell_boundaries.append(idx)
                current_cell = target['cell']

            sigma = 0.0
            status_tag = 'normal'
            color = 'blue'

            if val < 1.0:
                sigma = -99.9
                status_tag = 'dead'
                color = 'red'
            else:
                sigma = (val - global_mean) / global_stdev
                if val < limit:
                    status_tag = 'weak'
                    color = 'orange'

            self.tree_sfp.insert("", "end", 
                values=(target['cell_str'], target['bpm_num'], target['link_label'], f"{val:.1f}", f"{sigma:.2f}"), 
                tags=(status_tag,))
            
            plot_data.append({'x': idx, 'y': val, 'c': color})
            idx += 1

        if plot_data:
            x_vals = [p['x'] for p in plot_data]
            y_vals = [p['y'] for p in plot_data]
            colors = [p['c'] for p in plot_data]

            self.ax.scatter(x_vals, y_vals, c=colors, s=15, alpha=0.7)
            for x_pos in cell_boundaries:
                self.ax.axvline(x=x_pos, color='gray', linestyle=':', alpha=0.5)
                c_num = cell_boundaries.index(x_pos) + 1
                if c_num % 2 != 0:
                     self.ax.text(x_pos, max(y_vals)*1.02, f"C{c_num}", fontsize=8, color='gray')

            self.ax.axhline(y=limit, color='red', linestyle='--', label='Limit')
            self.ax.axhline(y=global_mean, color='green', linestyle='-', label='Mean')
            self.ax.legend(loc='upper right')

        self.ax.set_title(f"SFP Rx Power (Faults Found: {fault_count_total})")
        self.ax.set_ylabel("uW")
        self.ax.grid(True, linestyle='--', alpha=0.3)
        self.canvas.draw()

        self.btn_refresh.config(state="normal")
        self.lbl_status.config(text=f"Updated. Active Faults: {fault_count_total}", fg="black")

    def confirm_clear_faults(self):
        if messagebox.askyesno("Confirm Clear", "Are you sure you want to clear faults on ALL BPMs?"):
            self.lbl_status.config(text="Clearing Faults...", fg="red")
            threading.Thread(target=self.run_clear_sequence, daemon=True).start()

    def run_clear_sequence(self):
        def clear_one(pv):
            epics.caput(pv, 1)
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            executor.map(clear_one, self.clear_pvs)
        self.root.after(0, lambda: self.lbl_status.config(text="Faults Cleared. Refreshing...", fg="green"))
        self.root.after(1000, self.start_acquisition)

if __name__ == "__main__":
    root = tk.Tk()
    app = SFPAnalyzerApp(root)
    root.mainloop()
