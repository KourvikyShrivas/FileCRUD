import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path


# ─── Color Palette & Font ─────────────────────────────────────────────────────
BG        = "#0d0d0d"
BG2       = "#141414"
BG3       = "#1a1a1a"
BORDER    = "#2a2a2a"
FG        = "#e8e8e0"
FG_DIM    = "#888888"
ACCENT    = "#c8f564"
ACCENT2   = "#6496f5"
DANGER    = "#f56464"
MONO      = ("Courier", 10)
MONO_SM   = ("Courier", 9)
SANS      = ("Helvetica", 11, "bold")
SANS_LG   = ("Helvetica", 22, "bold")
SANS_SM   = ("Helvetica", 9)


# ─── Helper ───────────────────────────────────────────────────────────────────
def get_all_items():
    return list(Path('').rglob('*'))


# ─── Main App ─────────────────────────────────────────────────────────────────
class FileManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Manager")
        self.geometry("1050x680")
        self.resizable(True, True)
        self.configure(bg=BG)
        self._build_ui()

    # ── Layout ──────────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Sidebar ──────────────────────────────────────────────────────
        sidebar = tk.Frame(self, bg="#0a0a0a", width=220)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="🗂️", font=("Helvetica", 36), bg="#0a0a0a", fg=FG).pack(pady=(28, 0))
        tk.Label(sidebar, text="File\nManager", font=("Helvetica", 20, "bold"),
                 bg="#0a0a0a", fg=FG, justify="left").pack(padx=20, pady=(4, 2), anchor="w")
        tk.Label(sidebar, text="v1.0 · Tkinter UI", font=MONO_SM,
                 bg="#0a0a0a", fg=FG_DIM).pack(padx=20, anchor="w")

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X, padx=20, pady=16)

        self.selected_op = tk.StringVar(value="List Files")
        ops = [
            ("📋  List Files",    "List Files"),
            ("✏️  Create File",   "Create File"),
            ("👁️  Read File",     "Read File"),
            ("🔄  Update File",   "Update File"),
            ("🗑️  Delete File",   "Delete File"),
            ("✏️  Rename File",   "Rename File"),
            ("📁  Create Folder", "Create Folder"),
            ("🗑️  Delete Folder", "Delete Folder"),
        ]
        for label, value in ops:
            btn = tk.Radiobutton(
                sidebar, text=label, variable=self.selected_op, value=value,
                font=MONO_SM, bg="#0a0a0a", fg=FG_DIM,
                selectcolor="#1e1e1e", activebackground="#0a0a0a",
                activeforeground=ACCENT, indicatoron=False,
                relief="flat", anchor="w", padx=14, pady=7,
                cursor="hand2",
                command=self._switch_panel,
            )
            btn.pack(fill=tk.X, padx=12, pady=2)

        ttk.Separator(sidebar, orient="horizontal").pack(fill=tk.X, padx=20, pady=12)
        tk.Label(sidebar, text=f"CWD\n{Path.cwd()}", font=("Courier", 7),
                 bg="#0a0a0a", fg="#444", wraplength=190, justify="left").pack(padx=16, anchor="w")

        # ── Main Content ─────────────────────────────────────────────────
        content = tk.Frame(self, bg=BG)
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Op Panel (left of content)
        self.op_frame = tk.Frame(content, bg=BG)
        self.op_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=24, pady=20)

        # File tree (right of content)
        tree_frame = tk.Frame(content, bg=BG2, width=260)
        tree_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 16), pady=20)
        tree_frame.pack_propagate(False)
        self._build_tree_panel(tree_frame)

        self._switch_panel()

    def _build_tree_panel(self, parent):
        hdr = tk.Frame(parent, bg=BG2)
        hdr.pack(fill=tk.X, padx=12, pady=(12, 4))
        tk.Label(hdr, text="/ FILE TREE", font=("Courier", 8),
                 bg=BG2, fg=FG_DIM).pack(side=tk.LEFT)
        tk.Button(hdr, text="↺", font=("Courier", 10, "bold"),
                  bg=BG3, fg=ACCENT, relief="flat", bd=0,
                  cursor="hand2", command=self._refresh_tree,
                  padx=6).pack(side=tk.RIGHT)

        self.tree_box = scrolledtext.ScrolledText(
            parent, font=MONO_SM, bg=BG2, fg=FG_DIM,
            relief="flat", bd=0, state="disabled",
            wrap=tk.NONE, width=30, insertbackground=FG,
        )
        self.tree_box.pack(fill=tk.BOTH, expand=True, padx=8, pady=(4, 12))
        self._refresh_tree()

    def _refresh_tree(self):
        items = get_all_items()
        self.tree_box.configure(state="normal")
        self.tree_box.delete("1.0", tk.END)
        if not items:
            self.tree_box.insert(tk.END, "(empty)")
        for item in items:
            icon = "📁" if item.is_dir() else "📄"
            self.tree_box.insert(tk.END, f"{icon} {item}\n")
        self.tree_box.configure(state="disabled")

    # ── Panel Switcher ────────────────────────────────────────────────────
    def _switch_panel(self):
        for w in self.op_frame.winfo_children():
            w.destroy()
        op = self.selected_op.get()

        tk.Label(self.op_frame, text=f"/ {op.upper()}", font=("Courier", 8),
                 bg=BG, fg=FG_DIM).pack(anchor="w", pady=(0, 12))

        panels = {
            "List Files":    self._panel_list,
            "Create File":   self._panel_create_file,
            "Read File":     self._panel_read_file,
            "Update File":   self._panel_update_file,
            "Delete File":   self._panel_delete_file,
            "Rename File":   self._panel_rename_file,
            "Create Folder": self._panel_create_folder,
            "Delete Folder": self._panel_delete_folder,
        }
        panels.get(op, lambda: None)()

    # ── Shared Widgets ────────────────────────────────────────────────────
    def _label(self, parent, text):
        tk.Label(parent, text=text, font=MONO_SM, bg=BG, fg=FG_DIM).pack(anchor="w", pady=(8, 2))

    def _entry(self, parent, **kw):
        e = tk.Entry(parent, font=MONO, bg=BG3, fg=FG, relief="flat",
                     insertbackground=FG, bd=0, highlightthickness=1,
                     highlightbackground=BORDER, highlightcolor=ACCENT, **kw)
        e.pack(fill=tk.X, ipady=6, pady=(0, 4))
        return e

    def _btn(self, parent, text, cmd, danger=False):
        color = DANGER if danger else ACCENT
        b = tk.Button(parent, text=text, font=("Helvetica", 10, "bold"),
                      bg=BG3, fg=color, relief="flat", bd=0,
                      activebackground=color, activeforeground=BG,
                      cursor="hand2", padx=16, pady=8, command=cmd)
        b.pack(anchor="w", pady=(10, 0))
        return b

    def _textarea(self, parent, height=8, **kw):
        t = scrolledtext.ScrolledText(parent, font=MONO, bg=BG3, fg=FG,
                                       relief="flat", bd=0, height=height,
                                       insertbackground=FG, wrap=tk.WORD,
                                       highlightthickness=1,
                                       highlightbackground=BORDER,
                                       highlightcolor=ACCENT, **kw)
        t.pack(fill=tk.X, pady=(0, 4))
        return t

    def _dropdown(self, parent, items):
        var = tk.StringVar(value="— select —")
        cb = ttk.Combobox(parent, textvariable=var, values=["— select —"] + items,
                          font=MONO_SM, state="readonly")
        cb.pack(fill=tk.X, ipady=4, pady=(0, 4))
        # Style
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TCombobox", fieldbackground=BG3, background=BG3,
                        foreground=FG, selectbackground=ACCENT, selectforeground=BG)
        return var, cb

    def _status(self, parent, text, ok=True):
        color = ACCENT if ok else DANGER
        tk.Label(parent, text=text, font=MONO_SM, bg=BG, fg=color, wraplength=500,
                 justify="left").pack(anchor="w", pady=6)

    # ── Panels ────────────────────────────────────────────────────────────
    def _panel_list(self):
        items = get_all_items()
        box = scrolledtext.ScrolledText(self.op_frame, font=MONO_SM, bg=BG2, fg=FG_DIM,
                                         relief="flat", bd=0, height=25, wrap=tk.NONE,
                                         highlightthickness=1, highlightbackground=BORDER)
        box.pack(fill=tk.BOTH, expand=True)
        if not items:
            box.insert(tk.END, "No files or folders found.")
        for i, item in enumerate(items, 1):
            icon = "📁" if item.is_dir() else "📄"
            tag  = "DIR " if item.is_dir() else "FILE"
            box.insert(tk.END, f"  {i:>3}.  {icon} {item}  [{tag}]\n")
        box.configure(state="disabled")

    def _panel_create_file(self):
        f = self.op_frame
        self._label(f, "File name")
        name_var = self._entry(f)
        self._label(f, "File content")
        content_box = self._textarea(f)

        def do_create():
            name = name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Please enter a file name.")
                return
            p = Path(name)
            if p.exists():
                messagebox.showwarning("Warning", "File already exists.")
                return
            try:
                p.write_text(content_box.get("1.0", tk.END))
                self._status(f, f"✅  File '{name}' created successfully!")
                self._refresh_tree()
            except Exception as e:
                self._status(f, f"❌  Error: {e}", ok=False)

        self._btn(f, "✏️  Create File", do_create)

    def _panel_read_file(self):
        f = self.op_frame
        self._label(f, "Select a file")
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        var, _ = self._dropdown(f, items)
        result_box = self._textarea(f, height=16, state="disabled")

        def do_read():
            name = var.get()
            if name == "— select —":
                messagebox.showerror("Error", "Select a file.")
                return
            p = Path(name)
            if p.exists():
                try:
                    content = p.read_text()
                    result_box.configure(state="normal")
                    result_box.delete("1.0", tk.END)
                    result_box.insert(tk.END, content)
                    result_box.configure(state="disabled")
                except Exception as e:
                    self._status(f, f"❌  Error: {e}", ok=False)
            else:
                messagebox.showerror("Error", "File not found.")

        self._btn(f, "👁️  Read File", do_read)

    def _panel_update_file(self):
        f = self.op_frame
        self._label(f, "Select a file")
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        var, _ = self._dropdown(f, items)

        tk.Label(f, text="Mode", font=MONO_SM, bg=BG, fg=FG_DIM).pack(anchor="w", pady=(8, 2))
        mode_var = tk.StringVar(value="Overwrite")
        row = tk.Frame(f, bg=BG)
        row.pack(anchor="w")
        for m in ["Overwrite", "Append"]:
            tk.Radiobutton(row, text=m, variable=mode_var, value=m,
                           font=MONO_SM, bg=BG, fg=FG, selectcolor=BG3,
                           activebackground=BG, activeforeground=ACCENT).pack(side=tk.LEFT, padx=(0, 12))

        self._label(f, "New content")
        content_box = self._textarea(f, height=8)

        def do_update():
            name = var.get()
            if name == "— select —":
                messagebox.showerror("Error", "Select a file."); return
            p = Path(name)
            if not p.exists():
                messagebox.showerror("Error", "File not found."); return
            mode = 'w' if mode_var.get() == "Overwrite" else 'a'
            try:
                with open(name, mode) as fh:
                    fh.write(content_box.get("1.0", tk.END))
                self._status(f, f"✅  File '{name}' updated ({mode_var.get().lower()})!")
            except Exception as e:
                self._status(f, f"❌  Error: {e}", ok=False)

        self._btn(f, "🔄  Update File", do_update)

    def _panel_delete_file(self):
        f = self.op_frame
        self._label(f, "Select a file to delete")
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        var, _ = self._dropdown(f, items)
        tk.Label(f, text="⚠️  This action is permanent.", font=MONO_SM, bg=BG, fg=DANGER).pack(anchor="w", pady=6)

        def do_delete():
            name = var.get()
            if name == "— select —":
                messagebox.showerror("Error", "Select a file."); return
            if not messagebox.askyesno("Confirm Delete", f"Delete '{name}'? This cannot be undone."):
                return
            p = Path(name)
            if p.exists():
                try:
                    os.remove(p)
                    self._status(f, f"✅  File '{name}' deleted.")
                    self._refresh_tree()
                except Exception as e:
                    self._status(f, f"❌  Error: {e}", ok=False)
            else:
                messagebox.showerror("Error", "File not found.")

        self._btn(f, "🗑️  Delete File", do_delete, danger=True)

    def _panel_rename_file(self):
        f = self.op_frame
        self._label(f, "Select a file to rename")
        items = [str(i) for i in get_all_items() if Path(i).is_file()]
        var, _ = self._dropdown(f, items)
        self._label(f, "New file name")
        new_name_var = self._entry(f)

        def do_rename():
            name = var.get()
            new_name = new_name_var.get().strip()
            if name == "— select —" or not new_name:
                messagebox.showerror("Error", "Select a file and enter a new name."); return
            p = Path(name)
            if p.exists():
                try:
                    p.rename(new_name)
                    self._status(f, f"✅  '{name}'  →  '{new_name}'")
                    self._refresh_tree()
                except Exception as e:
                    self._status(f, f"❌  Error: {e}", ok=False)
            else:
                messagebox.showerror("Error", "File not found.")

        self._btn(f, "✏️  Rename File", do_rename)

    def _panel_create_folder(self):
        f = self.op_frame
        self._label(f, "Folder name")
        name_var = self._entry(f)

        def do_create():
            name = name_var.get().strip()
            if not name:
                messagebox.showerror("Error", "Enter a folder name."); return
            p = Path(name)
            if p.exists():
                messagebox.showwarning("Warning", "Folder already exists."); return
            try:
                p.mkdir(parents=True)
                self._status(f, f"✅  Folder '{name}' created!")
                self._refresh_tree()
            except Exception as e:
                self._status(f, f"❌  Error: {e}", ok=False)

        self._btn(f, "📁  Create Folder", do_create)

    def _panel_delete_folder(self):
        f = self.op_frame
        self._label(f, "Select a folder to delete")
        items = [str(i) for i in get_all_items() if Path(i).is_dir()]
        var, _ = self._dropdown(f, items)
        tk.Label(f, text="⚠️  Folder must be empty to delete.", font=MONO_SM, bg=BG, fg=DANGER).pack(anchor="w", pady=6)

        def do_delete():
            name = var.get()
            if name == "— select —":
                messagebox.showerror("Error", "Select a folder."); return
            if not messagebox.askyesno("Confirm Delete", f"Delete folder '{name}'?"):
                return
            p = Path(name)
            if p.exists():
                try:
                    p.rmdir()
                    self._status(f, f"✅  Folder '{name}' deleted.")
                    self._refresh_tree()
                except Exception as e:
                    self._status(f, f"❌  Error: {e}", ok=False)
            else:
                messagebox.showerror("Error", "Folder not found.")

        self._btn(f, "🗑️  Delete Folder", do_delete, danger=True)


# ─── Run ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = FileManagerApp()
    app.mainloop()