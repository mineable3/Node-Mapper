import tkinter as tk
from math import sqrt

class Node:
  def __init__(self, canvas, x, y):
    self.canvas = canvas
    self.x = x
    self.y = y
    self.body_id = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="blue", tags="node")
    self.connections = list()
    self.connection_ids = list()

  def move(self, x, y):
    self.x = x
    self.y = y
    self.canvas.coords(self.body_id, x - 20, y - 20, x + 20, y + 20)

    i = 0
    for other in self.connections:
      self.canvas.coords(self.connection_ids[i], x, y, other.x, other.y)
      i += 1

  def connect(self, other):
    id = self.canvas.create_line(self.get_position(), other.get_position(), fill="black", width=2, tags="line")
    self.connections.append(other)
    self.connection_ids.append(id)
    other.connections.append(self)
    other.connection_ids.append(id)

  def get_position(self):
    return self.x, self.y

class InteractiveNodeSystem:
  def __init__(self, root):
    self.root = root
    self.root.title("Interactive Node System")

    self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
    self.canvas.pack(expand=tk.YES, fill=tk.BOTH)
    self.canvas.bind("<Button-1>", self.create_node)
    self.canvas.bind("<Button-2>", self.grab_node)
    self.canvas.bind("<Button2-Motion>", self.drag_node, '+')
    self.canvas.bind("<ButtonRelease-2>", self.clear_selected_nodes)
    self.canvas.bind("<Button-3>", self.connect_nodes)

    self.nodes = []
    self.selected_nodes = []
    self.moving = False

  def clear_selected_nodes(self, thing=None):
    self.selected_nodes.clear()

  def create_node(self, event):
    new_node = Node(self.canvas, event.x, event.y)
    self.nodes.append(new_node)
    #self.redraw_all()

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
      coords = node.get_position()
      distance = sqrt((event.x - coords[0]) ** 2 + (event.y - coords[1]) ** 2)
      if distance < 20:
        return node
    return None

  def redraw_all(self):
    self.canvas.delete("all")
    for node in self.nodes:
      self.canvas.create_oval(node.get_position()[0] - 20, node.get_position()[1] - 20,
                   node.get_position()[0] + 20, node.get_position()[1] + 20,
                   fill="blue", tags="node")
      for connected_node in node.connections:
        self.canvas.create_line(node.get_position(), connected_node.get_position(),
                    fill="black", width=2, tags="line")

  def mainloop(self):
    self.root.mainloop()

if __name__ == "__main__":
  root = tk.Tk()
  app = InteractiveNodeSystem(root)
  app.mainloop()
