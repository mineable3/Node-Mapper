import tkinter
import numpy as np
import math

from Constants import Constants

class Node:
  def __init__(self, canvas: tkinter.Canvas, x: int, y: int, velocity: tuple = [0.0,0.0]):
    self.canvas = canvas
    self.coords = np.array([x, y])
    self.body_id = canvas.create_oval(x - Constants.NODE_SIZE, y - Constants.NODE_SIZE, x + Constants.NODE_SIZE, y + Constants.NODE_SIZE, fill="blue", tags="node")
    self.connections = list[Node]()
    self.connection_ids = list[int]()
    self.velocity = np.array(velocity)
    #canvas.create_polygon() draw velocity arrow here

  def move(self, x: int, y: int):
    self.coords[0] = x
    self.coords[1] = y
    self.canvas.coords(self.body_id, x - Constants.NODE_SIZE, y - Constants.NODE_SIZE, x + Constants.NODE_SIZE, y + Constants.NODE_SIZE)

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

  # should be done with pythagorean theorem because nodes can only attach in 90 or 180 degree orientations
  # without getting weird and glitchy
  def step_velocity(self):
    x = self.coords[0]
    y = self.coords[1]

    if(self.connections.__len__ != 0):
      for other in self.connections:
        xDiff = other.coords[0] - self.coords[0]
        yDiff = other.coords[1] - self.coords[1]

        #Attraction
        if(math.sqrt((math.fabs(xDiff)**2) + (math.fabs(yDiff)**2)) > Constants.attractionMax):
          if(xDiff > Constants.attractionMax):
            xDiff = Constants.attractionMax
          elif(xDiff < -Constants.attractionMax):
            xDiff = -Constants.attractionMax

          if(yDiff > Constants.attractionMax):
            yDiff = Constants.attractionMax
          elif(yDiff < -Constants.attractionMax):
            yDiff = -Constants.attractionMax

        #Repulsion
        if(math.sqrt((math.fabs(xDiff)**2) + (math.fabs(yDiff)**2)) < Constants.deadzoneInner):
          if(xDiff < Constants.deadzoneInner and xDiff > 0):
            xDiff = -Constants.deadzoneInner * 0.25
          elif(xDiff > -Constants.deadzoneInner and xDiff < 0):
            xDiff = Constants.deadzoneInner * 0.25

          if(yDiff < Constants.deadzoneInner and yDiff > 0):
            yDiff = -Constants.deadzoneInner * 0.25
          elif(yDiff > -Constants.deadzoneInner and yDiff < 0):
            yDiff = Constants.deadzoneInner * 0.25

        #Dead Zone
        if(math.sqrt((math.fabs(xDiff)**2) + (math.fabs(yDiff)**2)) <= Constants.deadzoneOuter and math.sqrt((math.fabs(xDiff)**2) + (math.fabs(yDiff)**2)) >= Constants.deadzoneInner):
          xDiff = 0
          yDiff = 0

        x += int(xDiff * 0.1)
        y += int(yDiff * 0.1)

    self.move(x, y)
