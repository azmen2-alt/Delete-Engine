# Delete Engine — Editing and Building Guide

For people who don't write Python. You don't need to understand the code. You just need to find a line and change one part of it.

---

## Part 1 — Before you edit anything

**Make a backup copy of `Delete_Engine.py` first.** Copy, paste, rename it `Delete_Engine_BACKUP.py`. If an edit breaks the app, delete the broken file and rename the backup back.

**Open the file the right way:**
- Right-click `Delete_Engine.py` → Open with → **Notepad**
- Do **not** open it in Word or WordPad. They add invisible formatting that breaks the file.

**Two rules that will save you:**

1. **Never change the spaces at the start of a line.** Python uses those spaces to understand the code. If a line starts with 8 spaces, it must keep 8 spaces.
2. **Only change what's between the quote marks.** The quotes themselves stay.

When you save, use File → Save. Don't use Save As unless you set "Save as type" to **All Files**, or Notepad will turn it into `Delete_Engine.py.txt` and it will stop working.

---

## Part 2 — The parts you might want to change

### A. The drive letter

Right now every path is forced to `Z:`. If your drive is mapped as something else, change it here.

**Find:**
```python
            path = 'Z:' + path[2:]
```

**Change** the `Z` to your letter. For drive O:
```python
            path = 'O:' + path[2:]
```

Keep the colon and keep the quotes.

There's also a mention of Z: in the on-screen instructions further down the file. Change that too so the text matches:
```python
5. It automatically fixes the drive letter to Z:.
```

---

### B. Which columns are checked

**Find:**
```python
    col_L_condition = df.iloc[:, 11].astype(str).str.strip().str.lower() == 'destroy'
    col_P_condition = df.iloc[:, 15].astype(str).str.strip().str.lower() == 'yes'
```

Two things you can change on each line: **the number** and **the word in quotes**.

**The number is the column position, counting from zero.** So the number is always one less than the real column number:

| Excel column | Number to use |
|---|---|
| A | 0 |
| B | 1 |
| ... | ... |
| K | 10 |
| L | **11** |
| M | 12 |
| N | 13 |
| O | 14 |
| P | **15** |
| Q | 16 |

So if your "destroy" flag moves from column L to column N, change `11` to `13`.

**The word in quotes is what it looks for.** Change `'destroy'` to `'purge'` if that's what your tracker says. Type it in lowercase — the app already handles capitals and extra spaces.

> This is the most dangerous edit in the file. If you point it at the wrong column, it will happily delete the wrong files. After any change here, test with the count set to 1 or 2 and check the results file before doing a real batch.

---

### C. The column names it reads

**Find:**
```python
    df = df.dropna(subset=['Full File Path'])
```

and further down:
```python
        path = str(row['Full File Path'])
        name = str(row['File Name'])
```

`'Full File Path'` and `'File Name'` must match your Excel headers **exactly** — same spelling, same capitals, same spaces. If your tracker says `FilePath` instead, change all three spots to `'FilePath'`.

Easier option: just rename the headers in Excel to match the script. Less to break.

---

### D. The starting number in the box

**Find:**
```python
entry_count.insert(0, "50")
```

Change `50` to whatever you want it to start at, like `10`. You can still type over it in the app.

---

### E. The app title and window size

**Find:**
```python
root.title("Delete Engine")
root.geometry("450x450")
```

Change the text in quotes for the title. For the size, the first number is width and the second is height. If the instructions get cut off after you edit them, make the second number bigger: `"450x550"`.

---

### F. The instructions shown in the app

**Find** the block that starts:
```python
instructions = """
HOW THIS APP WORKS:
```

Everything between the `"""` marks is plain text. Edit it however you like. Just don't delete either set of three quote marks.

---

### G. The results file name

**Find:**
```python
        results_path = f"{folder_path}/Deletion_Results_{timestamp}.xlsx"
```

Change `Deletion_Results` to whatever you want. Leave `{folder_path}`, `{timestamp}` and `.xlsx` alone — those fill themselves in.

---

## Part 3 — Test after every edit

1. Double-click the file. If the window opens, your edit didn't break anything.
2. If a black window flashes and disappears, something is wrong. Open Command Prompt, type `python ` (with a space), drag the file onto the window, press Enter. The error message will stay on screen. Usually it names the line number.
3. If you can't fix it, restore your backup.

Then run a real test with the count set to **1**. Open the results file and confirm it deleted the file you expected.

---

## Part 4 — Turning it into an .exe

The point of this is that other people can run it without installing Python.

You only need to do this on **your** machine. They just get the finished file.

### Step 1 — Install Python (skip if you already have it)

Download from python.org. During install, **tick the box that says "Add python.exe to PATH"** before clicking Install. This is the step everyone misses.

### Step 2 — Install the three packages

Open Command Prompt (press Start, type `cmd`, Enter) and paste:

```
pip install pandas openpyxl pyinstaller
```

Wait for it to finish. It takes a few minutes.

### Step 3 — Go to your file's folder

In Command Prompt, type `cd ` (with a space), then drag the folder containing `Delete_Engine.py` onto the Command Prompt window, then press Enter.

### Step 4 — Build it

Paste this and press Enter:

```
pyinstaller --onefile --windowed --name "Delete Engine" Delete_Engine.py
```

What those parts mean:
- `--onefile` — makes one single .exe instead of a folder full of files
- `--windowed` — stops a black console window from appearing behind the app
- `--name` — what the .exe will be called

This takes 2–10 minutes. Lots of text will scroll by. That's normal.

### Step 5 — Get your file

Look in the new **`dist`** folder next to your script. `Delete Engine.exe` is in there. That one file is everything you send out.

You can ignore or delete the `build` folder and the `.spec` file.

---

## Part 5 — Things people run into

**The .exe is 300+ MB.** Normal. Pandas and Excel support are bundled inside. Too big to email — share it through OneDrive or a network folder.

**It takes 10–20 seconds to open.** Also normal for `--onefile`. It's unpacking itself each time. If that's annoying, build without `--onefile` — you get a folder instead of a single file, it opens instantly, but you have to share the whole folder and they must keep it together.

**Antivirus blocks it or deletes it.** Common with PyInstaller files. You'll likely need IT to whitelist it. Tell them upfront rather than after it gets quarantined.

**"Windows protected your PC" on their machine.** They click "More info" → "Run anyway". This appears because the file isn't code-signed.

**It won't find any files on their computer.** They need the same drive letter mapped as you do. The .exe doesn't carry the drive mapping with it.

**You edited the .py but the .exe still behaves the old way.** The .exe is a frozen snapshot. Every time you change the script, you have to run the build command again and send out the new .exe.

---
