import pygame
from enum import Enum
from typing import List, Tuple, Optional


class NodeState(Enum):
    EMPTY = "empty"
    START = "start"
    END = "end"
    BARRIER = "barrier"
    VISITED = "visited"
    PATH = "path"


class Node:
    COLORS = {
        NodeState.EMPTY: (248, 249, 250),
        NodeState.START: (76, 175, 80),
        NodeState.END: (244, 67, 54),
        NodeState.BARRIER: (63, 81, 181),
        NodeState.VISITED: (255, 235, 59),
        NodeState.PATH: (255, 152, 0),
    }
    
    def __init__(self, row: int, col: int, width: int, total_rows: int):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.total_rows = total_rows
        self.state = NodeState.EMPTY
        self.distance = float('inf')
        self.previous: Optional[Node] = None
        self.neighbors: List[Node] = []
    
    def get_pos(self) -> Tuple[int, int]:
        return self.row, self.col
    
    def is_empty(self) -> bool:
        return self.state == NodeState.EMPTY
    
    def is_start(self) -> bool:
        return self.state == NodeState.START
    
    def is_end(self) -> bool:
        return self.state == NodeState.END
    
    def is_barrier(self) -> bool:
        return self.state == NodeState.BARRIER
    
    def is_visited(self) -> bool:
        return self.state == NodeState.VISITED
    
    def is_path(self) -> bool:
        return self.state == NodeState.PATH
    
    def set_state(self, state: NodeState):
        self.state = state
    
    def reset(self):
        self.state = NodeState.EMPTY
        self.distance = float('inf')
        self.previous = None
    
    def reset_algorithm_data(self):
        if self.state in [NodeState.VISITED, NodeState.PATH]:
            self.state = NodeState.EMPTY
        self.distance = float('inf')
        self.previous = None
    
    def draw(self, win: pygame.Surface):
        color = self.COLORS[self.state]
        pygame.draw.rect(win, color, (self.x, self.y, self.width, self.width))
    
    def update_neighbors(self, grid: List[List['Node']]):
        self.neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            new_row, new_col = self.row + dr, self.col + dc
            
            if (0 <= new_row < self.total_rows and 
                0 <= new_col < self.total_rows):
                neighbor = grid[new_row][new_col]
                if not neighbor.is_barrier():
                    self.neighbors.append(neighbor)
    
    def __lt__(self, other: 'Node') -> bool:
        return self.distance < other.distance 