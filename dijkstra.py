import heapq
from typing import List, Optional, Callable, Generator, Tuple
from node import Node, NodeState


class DijkstraAlgorithm:
    def __init__(self, start_node: Node, end_node: Node):
        self.start_node = start_node
        self.end_node = end_node
        self.visited_count = 0
        self.path_length = 0
        self.is_running = False
        self.is_complete = False
        self.path_found = False
        
        self.start_node.distance = 0
        self.priority_queue = [(0, self.start_node)]
        self.visited_nodes = set()
    
    def step(self) -> Tuple[bool, Optional[Node]]:
        if not self.priority_queue or self.is_complete:
            self.is_complete = True
            self.is_running = False
            return False, None
        
        current_distance, current_node = heapq.heappop(self.priority_queue)
        
        if current_distance > current_node.distance:
            return True, None
        
        if current_node in self.visited_nodes:
            return True, None
        
        self.visited_nodes.add(current_node)
        self.visited_count += 1
        
        if not current_node.is_start() and not current_node.is_end():
            current_node.set_state(NodeState.VISITED)
        
        if current_node == self.end_node:
            self.path_found = True
            self.is_complete = True
            self.is_running = False
            self._reconstruct_path()
            return False, current_node
        
        for neighbor in current_node.neighbors:
            if neighbor in self.visited_nodes:
                continue
            
            new_distance = current_node.distance + 1
            
            if new_distance < neighbor.distance:
                neighbor.distance = new_distance
                neighbor.previous = current_node
                heapq.heappush(self.priority_queue, (new_distance, neighbor))
        
        return True, current_node
    
    def _reconstruct_path(self):
        if not self.path_found:
            return
        
        current = self.end_node
        path_nodes = []
        
        while current is not None:
            path_nodes.append(current)
            current = current.previous
        
        for node in path_nodes[1:-1]:
            node.set_state(NodeState.PATH)
        
        self.path_length = len(path_nodes) - 1
    
    def run_complete(self, draw_callback: Optional[Callable] = None) -> bool:
        self.is_running = True
        
        while not self.is_complete:
            continue_running, current_node = self.step()
            
            if draw_callback:
                draw_callback()
            
            if not continue_running:
                break
        
        return self.path_found
    
    def get_stats(self) -> dict:
        return {
            'visited_count': self.visited_count,
            'path_length': self.path_length if self.path_found else 0,
            'is_running': self.is_running,
            'is_complete': self.is_complete,
            'path_found': self.path_found
        }


def run_dijkstra_step_by_step(start_node: Node, end_node: Node) -> Generator[Tuple[bool, Optional[Node], dict], None, None]:
    algorithm = DijkstraAlgorithm(start_node, end_node)
    algorithm.is_running = True
    
    while not algorithm.is_complete:
        continue_running, current_node = algorithm.step()
        stats = algorithm.get_stats()
        
        yield continue_running, current_node, stats
        
        if not continue_running:
            break


def run_dijkstra_complete(start_node: Node, end_node: Node) -> Tuple[bool, dict]:
    algorithm = DijkstraAlgorithm(start_node, end_node)
    path_found = algorithm.run_complete()
    stats = algorithm.get_stats()
    
    return path_found, stats 