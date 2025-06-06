import pygame
from typing import List, Tuple, Optional
from node import Node, NodeState


class Grid:
    def __init__(self, rows: int, width: int):
        self.rows = rows
        self.width = width
        self.gap = width // rows
        self.grid: List[List[Node]] = []
        self.start_node: Optional[Node] = None
        self.end_node: Optional[Node] = None
        self._create_grid()
    
    def _create_grid(self):
        self.grid = []
        for i in range(self.rows):
            self.grid.append([])
            for j in range(self.rows):
                node = Node(i, j, self.gap, self.rows)
                self.grid[i].append(node)
    
    def get_clicked_pos(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        y, x = pos
        row = y // self.gap
        col = x // self.gap
        return row, col
    
    def get_node(self, row: int, col: int) -> Optional[Node]:
        if 0 <= row < self.rows and 0 <= col < self.rows:
            return self.grid[row][col]
        return None
    
    def set_start(self, row: int, col: int) -> bool:
        node = self.get_node(row, col)
        if node and (node.is_empty() or node.is_start()):
            if self.start_node:
                self.start_node.set_state(NodeState.EMPTY)
            node.set_state(NodeState.START)
            self.start_node = node
            return True
        return False
    
    def set_end(self, row: int, col: int) -> bool:
        node = self.get_node(row, col)
        if node and (node.is_empty() or node.is_end()):
            if self.end_node:
                self.end_node.set_state(NodeState.EMPTY)
            node.set_state(NodeState.END)
            self.end_node = node
            return True
        return False
    
    def toggle_barrier(self, row: int, col: int) -> bool:
        node = self.get_node(row, col)
        if node and (node.is_empty() or node.is_barrier()):
            if node.is_barrier():
                node.set_state(NodeState.EMPTY)
            else:
                node.set_state(NodeState.BARRIER)
            return True
        return False
    
    def set_barrier(self, row: int, col: int) -> bool:
        node = self.get_node(row, col)
        if node and node.is_empty():
            node.set_state(NodeState.BARRIER)
            return True
        return False
    
    def reset_grid(self):
        for row in self.grid:
            for node in row:
                node.reset()
        self.start_node = None
        self.end_node = None
    
    def reset_algorithm_data(self):
        for row in self.grid:
            for node in row:
                node.reset_algorithm_data()
    
    def update_neighbors(self):
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)
    
    def is_ready_for_pathfinding(self) -> bool:
        return self.start_node is not None and self.end_node is not None
    
    def draw_grid_lines(self, win: pygame.Surface):
        line_color = (220, 220, 220)
        
        for i in range(self.rows):
            pygame.draw.line(win, line_color, 
                           (0, i * self.gap), 
                           (self.width, i * self.gap))
        
        for j in range(self.rows):
            pygame.draw.line(win, line_color, 
                           (j * self.gap, 0), 
                           (j * self.gap, self.width))
    
    def draw(self, win: pygame.Surface):
        win.fill((240, 242, 247))
        
        for row in self.grid:
            for node in row:
                node.draw(win)
        
        self.draw_grid_lines(win)
    
    def get_all_nodes(self) -> List[Node]:
        nodes = []
        for row in self.grid:
            nodes.extend(row)
        return nodes 