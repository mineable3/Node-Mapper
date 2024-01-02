import tkinter as tk
import numpy as np
from math import sqrt
from InteractiveNodeSystem import InteractiveNodeSystem

if __name__ == "__main__":
  root = tk.Tk()
  app = InteractiveNodeSystem(root)
  app.mainloop()
