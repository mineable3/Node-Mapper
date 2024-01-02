from math import sqrt
from Node import Node
import tkinter as tk

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

  def mainloop(self):
    self.root.mainloop()
