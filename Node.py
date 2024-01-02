import tkinter
import numpy as np

class Node:
  def __init__(self, canvas: tkinter.Canvas, x: int, y: int, velocity: tuple):
    self.canvas = canvas
    self.coords = np.array([x, y])
    self.body_id = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="blue", tags="node")
    self.connections = list[Node]()
    self.connection_ids = list[int]()
    self.velocity = np.array(velocity)

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
