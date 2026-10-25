import tkinter
import ttkbootstrap
import subprocess, sys
import re

patterns = {
    "keywords": r'\b(def|class|if|else|elif|for|while|in|import|from|\
        return|True|False|None|and|or|not|try|except|with|as|print)\b',
    "strings": r'(["\'])(?:\\.|(?!\1).)*\1',
    "comments": r'#.*'
}

def highlight(event=None):
    text = editor.get("1.0", "end")
    for tag in ("keywords", "strings", "comments"):
        editor.tag_remove(tag, "1.0", "end")

    for tag, pattern in patterns.items():
        for m in re.finditer(pattern, text):
            editor.tag_add(tag, f"1.0 + {m.start()}c", f"1.0 + {m.end()}c")    

def run():
    process = subprocess.run(
        [
            sys.executable,
            "-c",
            editor.get("1.0", "end")
        ],
        capture_output = True,
        text = True
    )
    console.insert("end", process.stdout + process.stderr)

def open_file():    
    file_path = tkinter.filedialog.askopenfilename(filetypes=[("Python", "*.py")])
    if file_path:
        editor.delete("1.0", "end")
        editor.insert("1.0", open(file_path, encoding="utf-8").read())
    highlight()

def save_file():
    file_path = tkinter.filedialog.asksaveasfilename(
        defaultextension = ".py", filetypes=[("Python", "*.py")]
    )        
    if file_path:
        open(file_path, "w", encoding="utf-8").write(editor.get("1.0", "end"))

window = ttkbootstrap.Window(themename="darkly")
window.title("Python Editor")

menubar = ttkbootstrap.Frame(window)
menubar.pack(fill="x")

ttkbootstrap.Button(menubar, text="▶ Run", command=run).pack(side="left")                                                                                                                                                                                           
ttkbootstrap.Button(menubar, text="📄 Open", command=open_file).pack(side="left")                                                                                                                                                                                           
ttkbootstrap.Button(menubar, text="💾 Save", command=save_file).pack(side="left")                                                                                                                                                                                           

panedwindow = tkinter.PanedWindow(window, orient="vertical", bg="#333333", sashwidth=5)
panedwindow.pack(fill="both", expand=True)

editor = tkinter.Text(panedwindow, bg="#1e1e1e", fg="#d4d4d4", insertbackground="#d4d4d4", font=("Consolas", 12), undo=True)

console = tkinter.Text(panedwindow, bg="#111111", fg="#dddddd", font=("Consolas", 12), height=10)

editor.insert("1.0", 'print("Hey, It is me, it is Verity")')
highlight()

panedwindow.add(editor)
panedwindow.add(console)

editor.tag_configure("keywords", foreground="#00ffe5")
editor.tag_configure("strings", foreground="#ff00bb")
editor.tag_configure("comments", foreground="#56d69f")
editor.bind("<KeyRelease>", highlight)

window.mainloop()

