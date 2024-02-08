import tkinter
import numpy as np
import math

class Node:
  def __init__(self, canvas: tkinter.Canvas, x: int, y: int, velocity: tuple = [0.0,0.0]):
    self.canvas = canvas
    self.coords = np.array([x, y])
    self.body_id = canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="blue", tags="node")
    self.connections = list[Node]()
    self.connection_ids = list[int]()
    self.velocity = np.array(velocity)
    #canvas.create_polygon() draw velocity arrow here

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

    # velocity = np.array((other.coords[0]-self.coords[0], other.coords[1]-self.coords[1]))

    # self.add_to_velocity(velocity)

  def get_position_np(self):
    return self.coords

  def get_position_list(self) -> list[int]:
    return [self.coords[0], self.coords[1]]

  def get_velocity_np(self):
    return self.velocity

  def get_velocity_list(self) -> list[float]:
    return [self.velocity[0], self.velocity[1]]

  def add_to_velocity(self, vector):
    self.velocity += vector

  def step_velocity(self):
    x = self.coords[0]
    y = self.coords[1]

    if(self.connections.__len__ != 0):
      for other in self.connections:
        xDiff = other.coords[0] - self.coords[0]
        yDiff = other.coords[1] - self.coords[1]

        #Attraction
        if(xDiff > 50):
          xDiff = 50
        elif(xDiff < -50):
          xDiff = -50

        if(yDiff > 50):
          yDiff = 50
        elif(yDiff < -50):
          yDiff = -50

        #Repulsion
        if(xDiff < 20 and xDiff > 0):
          xDiff = -10
        elif(xDiff > -20 and xDiff < 0):
          xDiff = 10

        if(yDiff < 20 and yDiff > 0):
          yDiff = -10
        elif(yDiff > -20 and yDiff < 0):
          yDiff = 10

        x += int(xDiff * 0.1)
        y += int(yDiff * 0.1)

        print(xDiff)

    self.move(x, y)
