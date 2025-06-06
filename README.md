# dijkstra_sim

![Dijkstra Pathfinding Demo](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![Pygame](https://img.shields.io/badge/Pygame-2.5.0%2B-green?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Screenshots

![image](https://github.com/user-attachments/assets/ab281372-582c-4e2d-9a80-72901e8ab1bc)
![image](https://github.com/user-attachments/assets/58134c85-933a-4cb7-8146-b3f5bc3bc1ec)


## Controls

| Action                 | Control                               |
| ---------------------- | ------------------------------------- |
| Place/Move Start Point | **Left Click**                        |
| Place/Move End Point   | **Right Click**                       |
| Toggle Barriers        | **Middle Click** or **Shift + Click** |
| Start/Stop Algorithm   | **Spacebar**                          |
| Reset Grid             | **R Key**                             |
| Speed Control          | **1-5 Keys** (1=Slow, 5=Fast)         |
| Exit Application       | **ESC Key**                           |

## Quick Start

### Installation

1. install the needed libraries from `requirements.txt`
2. run `game.py`

## How to Use

### Getting Started

1. **Launch the Application**

   - Run `python game.py`
   - Read the splash screen instructions
   - Press any key to continue

2. **Set Up Your Scenario**

   - **Left-click** on any empty cell to place the green **start point**
   - **Right-click** on any empty cell to place the red **end point**
   - **Middle-click** or **Shift+click** on empty cells to create blue **barriers**

3. **Run the Algorithm**

   - Press **Spacebar** to start the pathfinding visualization
   - Watch as yellow cells show the algorithm's exploration
   - The final path will be highlighted in orange/gold

4. **Experiment**
   - Press **R** to reset and try different configurations
   - Use **1-5** keys to adjust animation speed
   - Create mazes and complex obstacle patterns

### Understanding the Visualization

| Color         | Meaning                                   |
| ------------- | ----------------------------------------- |
| 🟢 **Green**  | Start point - where pathfinding begins    |
| 🔴 **Red**    | End point - the target destination        |
| 🔵 **Blue**   | Barriers - impassable obstacles           |
| 🟡 **Yellow** | Visited cells - explored by the algorithm |
| 🟠 **Orange** | Shortest path - the optimal route found   |
| ⚪ **White**  | Empty cells - available for pathfinding   |

## Project Structure

```
python_game/
├── game.py                 # Main entry point
├── dijkstra_visualizer.py  # Main application class
├── grid.py                 # Grid management and operations
├── node.py                 # Individual cell/node implementation
├── dijkstra.py             # Dijkstra's algorithm implementation
├── ui.py                   # User interface components
├── requirements.txt        # Python dependencies
└── README.md              # This file
```
