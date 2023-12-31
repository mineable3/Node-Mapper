import tkinter as tk
from math import sqrt


class Node:
  def __init__(self, canvas, x, y):
    self.canvas = canvas
    self.id = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="blue", tags="node")
    self.connections = set()

  def move(self, x, y):
    self.canvas.coords(self.id, x - 20, y - 20, x + 20, y + 20)

  def connect(self, other):
    self.connections.add(other)
    other.connections.add(self)
    self.canvas.create_line(self.get_position(), other.get_position(), fill="black", width=2, tags="line")

  def get_position(self):
    return self.canvas.coords(self.id)[0] + 20, self.canvas.coords(self.id)[1] + 20


class InteractiveNodeSystem:
  def __init__(self, root):
    self.root = root
    self.root.title("Interactive Node System")

    self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
    self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
    self.canvas.bind("<Button-1>", self.create_node)
    self.canvas.bind("<Button-3>", self.connect_nodes)
    self.canvas.bind("<Button-2>", self.remove_node)

    self.nodes = []
    self.selected_nodes = []

  def create_node(self, event):
    new_node = Node(self.canvas, event.x, event.y)
    self.nodes.append(new_node)

  def connect_nodes(self, event):
    clicked_node = self.get_clicked_node(event)
    if clicked_node:
      self.selected_nodes.append(clicked_node)
      if len(self.selected_nodes) == 2:
        self.selected_nodes[0].connect(self.selected_nodes[1])
        self.selected_nodes = []

  def get_clicked_node(self, event):
    for node in self.nodes:
      coords = node.get_position()
      distance = sqrt((event.x - coords[0]) ** 2 + (event.y - coords[1]) ** 2)
      if distance < 20:  # You can adjust the distance threshold as needed
        return node
    return None

  def remove_node(self, event):
    for node in self.nodes:
      coords = node.get_position()
      distance = sqrt((event.x - coords[0]) ** 2 + (event.y - coords[1]) ** 2)
      if distance < 20:  # You can adjust the distance threshold as needed
        self.nodes.remove(node)

  def mainloop(self):
    self.root.mainloop()


if __name__ == "__main__":
  root = tk.Tk()
  app = InteractiveNodeSystem(root)
  app.mainloop()
