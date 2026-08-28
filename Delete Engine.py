import pandas as pd
import os
import time
import tkinter as tk
from tkinter import filedialog, messagebox

def start_deletion():
    # 1. Get the number of files the user typed
    try:
        batch_size = int(entry_count.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")
        return
        
    if batch_size <= 0:
        messagebox.showerror("Error", "Please enter a number greater than 0.")
        return

    # 2. Ask user to select the Excel file
    file_path = filedialog.askopenfilename(
        title="Select your Excel File",
        filetypes=[("Excel Files", "*.xlsx")]
    )
    
    if not file_path:
        return # Stops if you close the window without picking a file
        
    # 3. Read the Excel file
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        messagebox.showerror("Error", f"Could not read file:\n{e}")
        return
        
    df = df.dropna(subset=['Full File Path'])
    
    # Check Column L for "destroy" and Column P for "yes"
    col_L_condition = df.iloc[:, 11].astype(str).str.strip().str.lower() == 'destroy'
    col_P_condition = df.iloc[:, 15].astype(str).str.strip().str.lower() == 'yes'
    df_filtered = df[col_L_condition & col_P_condition]
    
    # 4. Find files on the server
    files_to_delete = []
    for _, row in df_filtered.iterrows():
        path = str(row['Full File Path'])
        name = str(row['File Name'])
        
        # Change any drive letter to Z:
        if len(path) >= 2 and path[1] == ':' and path[0].isalpha():
            path = 'Z:' + path[2:]
            
        if os.path.exists(path):
            files_to_delete.append({"path": path, "name": name})
            if len(files_to_delete) >= batch_size:
                break
                
    if len(files_to_delete) == 0:
        messagebox.showinfo("Done", "No matching files found on the server.")
        return
        
    # 5. Confirm with you before deleting
    confirm = messagebox.askyesno(
        "Confirm Deletion", 
        f"Found {len(files_to_delete)} files ready to delete.\n\nDo you want to permanently delete them now?"
    )
    
    if confirm:
        deleted_count = 0
        results_data = []
        
        for item in files_to_delete:
            path = item['path']
            name = item['name']
            try:
                os.remove(path)
                status = "DELETED"
                deleted_count += 1
            except Exception as e:
                status = "ERROR"
            
            results_data.append({
                "File Name": name,
                "Checked Path": path,
                "Status": status
            })
            
        # Save results
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        folder_path = os.path.dirname(file_path)
        results_path = f"{folder_path}/Deletion_Results_{timestamp}.xlsx"
        
        results_df = pd.DataFrame(results_data)
        results_df.to_excel(results_path, index=False)
        
        messagebox.showinfo("Finished", f"Successfully deleted {deleted_count} files.\n\nResults saved to:\n{results_path}")

# --- App Window Setup ---
root = tk.Tk()
root.title("Delete Engine")
root.geometry("450x450")

instructions = """
HOW THIS APP WORKS:
1. Type how many files you want to delete below.
2. Click the 'Select File & Start' button.
3. Pick your Excel tracker.
4. The app checks Column L for "destroy" and Column P for "yes".
5. It automatically fixes the drive letter to Z:.
6. It checks if the files exist on the server.
7. It asks for your final permission before deleting.
8. It saves a results file in the same folder as your tracker.
"""

lbl_instructions = tk.Label(root, text=instructions, justify="left", font=("Arial", 10))
lbl_instructions.pack(pady=15)

lbl_count = tk.Label(root, text="Number of files to delete:", font=("Arial", 11, "bold"))
lbl_count.pack()

entry_count = tk.Entry(root, width=10, font=("Arial", 12), justify="center")
entry_count.insert(0, "50") # Automatically starts at 50
entry_count.pack(pady=5)

btn_start = tk.Button(root, text="Select File & Start", command=start_deletion, font=("Arial", 12, "bold"), bg="lightblue", padx=10, pady=5)
btn_start.pack(pady=20)

root.mainloop()