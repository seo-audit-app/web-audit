# main.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from crawler import crawl_website
import csv

def run_audit():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a URL.")
        return

    results = crawl_website(url)
    tree.delete(*tree.get_children())
    for row in results:
        tree.insert("", tk.END, values=row)

def export_csv():
    file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file:
        with open(file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["URL", "Status Code", "Title"])
            for child in tree.get_children():
                writer.writerow(tree.item(child)["values"])
        messagebox.showinfo("Success", f"Report saved to {file}")

# GUI Setup
root = tk.Tk()
root.title("Basic SEO Audit Tool")
root.geometry("800x500")

frame = ttk.Frame(root, padding=10)
frame.pack(fill="x")

url_label = ttk.Label(frame, text="Website URL:")
url_label.pack(side="left")

url_entry = ttk.Entry(frame, width=60)
url_entry.pack(side="left", padx=5)

run_button = ttk.Button(frame, text="Run Audit", command=run_audit)
run_button.pack(side="left", padx=5)

export_button = ttk.Button(frame, text="Export CSV", command=export_csv)
export_button.pack(side="left")

columns = ("URL", "Status Code", "Title")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="w", width=250 if col == "Title" else 200)
tree.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
