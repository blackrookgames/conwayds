import tkinter as tk
import tkinter.messagebox as tk_messagebox

#region protocols

def wm_delete_window():
    global window
    if tk_messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        window.destroy()

#endregion

window = tk.Tk()
window.title("tmap")
window.geometry("640x480")
window.protocol("WM_DELETE_WINDOW", wm_delete_window)

widget_m = tk.Menu(window)
window.config(menu = widget_m)

widget_mf = tk.Menu(widget_m, tearoff = 0)
widget_mf.add_command(label = "New", command = lambda: print("New"))
widget_mf.add_command(label = "Open", command = lambda: print("Open"))
widget_mf.add_command(label = "Save", command = lambda: print("Save"))
widget_mf.add_command(label = "Save As", command = lambda: print("Save As"))
widget_mf.add_command(label = "Exit", command = wm_delete_window)
widget_m.add_cascade(label = "File", menu = widget_mf)

widget_mt = tk.Menu(widget_m, tearoff = 0)
widget_mt.add_command(label = "Config", command = lambda: print("Config"))
widget_m.add_cascade(label = "Tileset", menu = widget_mt)

window.mainloop()