import asyncio
import math
import tkinter as tk
import tkinter.messagebox as tk_messagebox

from async_tkinter_loop import async_handler, async_mainloop
from tkinter import ttk

import gui.tmap as gui

#region const

TILESET_SIZE = 0x10000
TILESET_COLS = round(math.sqrt(0x10000))
TILESET_ROWS = TILESET_SIZE // TILESET_COLS

#endregion

#region variables

tileset:None|tk.PhotoImage = None

#endregion

#region protocols

def wm_delete_window():
    global root
    if tk_messagebox.askokcancel("Quit", "Do you really wish to quit?"):
        root.destroy()

#endregion

#region commands

async def background_task(label):
    count = 0
    while True:
        # Simulate some asynchronous work
        await asyncio.sleep(1)
        count += 1
        # Update the UI thread-safely (async-tkinter-loop handles the integration)
        label.config(text=f"Background count: {count}")
        print(f"Task running: {count}")

async def cmd_widget_mt():
    global root, tileset
    TILE_TOTAL = gui.TILESET_SIZE * 64
    #region events
    def _dialog_delete():
        nonlocal task_stopping
        task_stopping = True
    #endregion
    src_tileset = gui.Tileset()
    src_palette = gui.Palette()
    # Create dialog
    dialog = tk.Toplevel(root)
    dialog.title("Updating tileset")
    dialog.transient(root) # Makes the dialog dependent on the parent
    dialog.protocol("WM_DELETE_WINDOW", _dialog_delete)
    # Add progress bar
    progbar = ttk.Progressbar(dialog)
    progbar.pack()
    # Create task
    task_stopping = False
    task_tileset = tk.PhotoImage(\
        width = gui.TILESET_TILE_W * TILESET_COLS,\
        height = gui.TILESET_TILE_H * TILESET_ROWS)
    task_progress = 0
    async def _task():
        nonlocal src_tileset, src_palette
        nonlocal task_tileset, task_stopping, task_progress
        while (not task_stopping) and task_progress < TILE_TOTAL:
            # Properties
            _tile_index = task_progress % gui.TILESET_SIZE
            _tile_props = task_progress // gui.TILESET_SIZE
            _tile_sub = _tile_props % gui.PALETTE_SUBCOUNT # TODO: Update
            _tile_flip = _tile_props // gui.PALETTE_SUBCOUNT # TODO: Update
            _tile_flip_x = (_tile_flip & 0b01) != 0 # TODO: Update
            _tile_flip_y = (_tile_flip & 0b10) != 0 # TODO: Update
            # Input X-coordinates
            if _tile_flip_x:
                _x_beg = gui.TILESET_TILE_W - 1
                _x_inc = -1
            else:
                _x_beg = 0
                _x_inc = 1
            # Input Y-coordinates
            if _tile_flip_y:
                _y_beg = gui.TILESET_TILE_H - 1
                _y_inc = -1
            else:
                _y_beg = 0
                _y_inc = 1
            # Tile
            _off_x = (task_progress % TILESET_COLS) * gui.TILESET_TILE_W
            _off_y = (task_progress // TILESET_COLS) * gui.TILESET_TILE_H
            for _x in range(gui.TILESET_TILE_W):
                _column:list[str] = []
                for _y in range(gui.TILESET_TILE_H):
                    _pixel = src_tileset[_tile_index, _x_beg + _x * _x_inc, _y_beg + _y * _y_inc]
                    _column.append(src_palette[_tile_sub][_pixel])
                _to = (\
                    _off_x + _x, _off_y,\
                    _off_x + _x + 1, _off_y + gui.TILESET_TILE_H)
                task_tileset.put(_column, _to)
            task_progress += 1
            # Await
            if (task_progress % 512) == 0: await asyncio.sleep(0.01)
    task = asyncio.create_task(_task())
    # Make dialog modal
    dialog.grab_set()
    # Wait for task to finish
    while not task.done():
        progbar['value'] = 100 * (task_progress / TILE_TOTAL)
        await asyncio.sleep(0.1)
    # Destroy window
    dialog.destroy()
    # Update tileset
    if not task_stopping:
        tileset = task_tileset
        # TODO: Remove
        global test
        test.create_image(\
            (0, 0),\
            image = tileset)

#endregion

#region window/widgets

root = tk.Tk()
root.title("gui")
root.geometry("640x480")
root.protocol("WM_DELETE_WINDOW", wm_delete_window)

widget_m = tk.Menu(root)
root.config(menu = widget_m)

widget_mf = tk.Menu(widget_m, tearoff = 0)
widget_mf.add_command(label = "New", command = lambda: print("New"))
widget_mf.add_command(label = "Open", command = lambda: print("Open"))
widget_mf.add_command(label = "Save", command = lambda: print("Save"))
widget_mf.add_command(label = "Save As", command = lambda: print("Save As"))
widget_mf.add_command(label = "Exit", command = wm_delete_window)
widget_m.add_cascade(label = "File", menu = widget_mf)

widget_mt = tk.Menu(widget_m, tearoff = 0)
widget_mt.add_command(label = "Config", command = async_handler(cmd_widget_mt))
widget_m.add_cascade(label = "Tileset", menu = widget_mt)

#endregion

test = tk.Canvas(root,\
    width = gui.TILESET_TILE_W * TILESET_COLS,\
    height = gui.TILESET_TILE_H * TILESET_ROWS)
test.grid(column = 0, row = 0)
async_mainloop(root)