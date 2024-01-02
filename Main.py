import tkinter as tk
import numpy as np
from math import sqrt

class Node:
  def __init__(self, canvas: tk.Canvas, x: int, y: int):
    self.canvas = canvas
    self.coords = np.array([x, y])
    self.body_id = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="blue", tags="node")
    self.connections = list[Node]()
    self.connection_ids = list[int]()

  def move(self, x: int, y: int):
    self.coords[0] = x
    self.coords[1] = y
    self.canvas.coords(self.body_id, x - 20, y - 20, x + 20, y + 20)

    for i, other in enumerate(self.connections):
      self.canvas.coords(self.connection_ids[i], x, y, other.get_position_np()[0], other.get_position_np()[1])

  def connect(self, other):
    id = self.canvas.create_line(self.get_position_np()[0], self.get_position_np()[1],
                      other.get_position_np()[0], other.get_position_np()[1],
                      fill="black", width=2, tags="line")
    self.connections.append(other)
    self.connection_ids.append(id)
    other.connections.append(self)
    other.connection_ids.append(id)

  def get_position_np(self):
    return self.coords

  def get_position_list(self) -> list[int]:
    return [self.coords[0], self.coords[1]]

class InteractiveNodeSystem:
  def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("Interactive Node System")

    self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
    self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
    self.canvas.bind("<Button-1>", self.create_node)
    self.canvas.bind("<Button-2>", self.grab_node)
    self.canvas.bind("<Button2-Motion>", self.drag_node, '+')
    self.canvas.bind("<ButtonRelease-2>", self.clear_selected_nodes)
    self.canvas.bind("<Button-3>", self.connect_nodes)

    self.nodes = list[Node]()
    self.selected_nodes = list[Node]()

  def clear_selected_nodes(self, doNotUseThis=None):
    self.selected_nodes.clear()

  def create_node(self, event) -> Node:
    new_node = Node(self.canvas, event.x, event.y)
    self.nodes.append(new_node)
    #self.redraw_all()
    return new_node

  def grab_node(self, event):
    self.clear_selected_nodes()
    self.selected_nodes.append(self.get_clicked_node(event))

  def drag_node(self, event):
    if self.selected_nodes[0] != None:
      self.selected_nodes[0].move(event.x, event.y)

  def connect_nodes(self, event):

    clicked_node = self.get_clicked_node(event)
    if clicked_node:
      self.selected_nodes.append(clicked_node)

      if len(self.selected_nodes) == 2 and self.selected_nodes[0] != self.selected_nodes[1]:
        self.selected_nodes[0].connect(self.selected_nodes[1])
        self.selected_nodes = []

      if(len(self.selected_nodes) > 1):
        self.selected_nodes.pop(0)

  def get_clicked_node(self, event):
    for node in self.nodes:
      coords = node.get_position_np()
      distance = sqrt((event.x - coords[0]) ** 2 + (event.y - coords[1]) ** 2)
      if distance < 20:
        return node
    return None

  def redraw_all(self):
    self.canvas.delete("all")
    for node in self.nodes:
      self.canvas.create_oval(node.get_position_np()[0] - 20, node.get_position_np()[1] - 20,
                   node.get_position_np()[0] + 20, node.get_position_np()[1] + 20,
                   fill="blue", tags="node")
      for connected_node in node.connections:
        self.canvas.create_line(node.get_position_list(), connected_node.get_position_list(),
                    fill="black", width=2, tags="line")

  def mainloop(self):
    self.root.mainloop()

if __name__ == "__main__":
  root = tk.Tk()
  app = InteractiveNodeSystem(root)
  app.mainloop()
