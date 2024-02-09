# Node-Mapper
Node Mapping software with simple a GUI. Nodes are represented by blue circles. A connection is a black line going between two nodes. A node can have multiple connections. Nodes will always attract the nodes they are attached to. If moved, nodes will continue to attracted their connected nodes.

## Usage
  ### Build
  The entire project can be run by executing the Makefile  
  After moving into project's directory simply run  
  $ `make`  
  and the program should start

  ### Controls
   - Left click: places new nodes
   - Right click: selects a node, if two nodes are selected they connect.
   - Middle click: moves the currently selected node with the mouse
