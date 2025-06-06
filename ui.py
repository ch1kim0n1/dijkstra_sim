"""
UI components for the Dijkstra pathfinding visualizer.
"""
import pygame
from typing import Dict, Any, Tuple
from node import NodeState


class UI:
    """
    Handles UI elements like legend, statistics, and instructions.
    
    Attributes:
        font (pygame.font.Font): Font for text rendering
        small_font (pygame.font.Font): Smaller font for details
        colors (Dict): Color scheme for UI elements
    """
    
    def __init__(self):
        """Initialize the UI system."""
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)
        self.title_font = pygame.font.Font(None, 32)
        
        # UI color scheme
        self.colors = {
            'background': (255, 255, 255),
            'text': (33, 37, 41),
            'text_light': (108, 117, 125),
            'panel': (248, 249, 250),
            'border': (222, 226, 230),
            'accent': (63, 81, 181)
        }
    
    def draw_legend(self, win: pygame.Surface, x: int, y: int, width: int = 200) -> int:
        """
        Draw the color legend.
        
        Args:
            win (pygame.Surface): Surface to draw on
            x (int): X position
            y (int): Y position
            width (int): Width of the legend panel
            
        Returns:
            int: Height of the drawn legend
        """
        from node import Node  # Import here to avoid circular imports
        
        # Legend items
        legend_items = [
            ("Start Node", NodeState.START),
            ("End Node", NodeState.END),
            ("Barrier", NodeState.BARRIER),
            ("Visited", NodeState.VISITED),
            ("Shortest Path", NodeState.PATH),
            ("Empty", NodeState.EMPTY)
        ]
        
        # Panel background
        panel_height = len(legend_items) * 30 + 40
        pygame.draw.rect(win, self.colors['panel'], (x, y, width, panel_height))
        pygame.draw.rect(win, self.colors['border'], (x, y, width, panel_height), 2)
        
        # Title
        title_text = self.font.render("Legend", True, self.colors['text'])
        win.blit(title_text, (x + 10, y + 10))
        
        # Legend items
        current_y = y + 40
        for name, state in legend_items:
            # Color square
            color = Node.COLORS[state]
            pygame.draw.rect(win, color, (x + 10, current_y, 20, 20))
            pygame.draw.rect(win, self.colors['border'], (x + 10, current_y, 20, 20), 1)
            
            # Text
            text = self.small_font.render(name, True, self.colors['text'])
            win.blit(text, (x + 40, current_y + 3))
            
            current_y += 25
        
        return panel_height
    
    def draw_controls(self, win: pygame.Surface, x: int, y: int, width: int = 200) -> int:
        """
        Draw the controls instructions.
        
        Args:
            win (pygame.Surface): Surface to draw on
            x (int): X position
            y (int): Y position
            width (int): Width of the controls panel
            
        Returns:
            int: Height of the drawn controls panel
        """
        controls = [
            "Controls:",
            "",
            "Left Click: Set Start",
            "Right Click: Set End",
            "Middle Click: Barriers",
            "",
            "SPACE: Run Algorithm",
            "R: Reset Grid",
            "1-10: Speed Control"
        ]
        
        # Calculate panel height
        panel_height = len(controls) * 20 + 20
        
        # Panel background
        pygame.draw.rect(win, self.colors['panel'], (x, y, width, panel_height))
        pygame.draw.rect(win, self.colors['border'], (x, y, width, panel_height), 2)
        
        # Draw controls
        current_y = y + 10
        for control in controls:
            if control == "Controls:":
                text = self.font.render(control, True, self.colors['text'])
            elif control == "":
                current_y += 20
                continue
            else:
                text = self.small_font.render(control, True, self.colors['text_light'])
            
            win.blit(text, (x + 10, current_y))
            current_y += 20
        
        return panel_height
    
    def draw_statistics(self, win: pygame.Surface, x: int, y: int, width: int, stats: Dict[str, Any]) -> int:
        """
        Draw algorithm statistics.
        
        Args:
            win (pygame.Surface): Surface to draw on
            x (int): X position
            y (int): Y position
            width (int): Width of the statistics panel
            stats (Dict[str, Any]): Algorithm statistics
            
        Returns:
            int: Height of the drawn statistics panel
        """
        stat_lines = [
            "Statistics:",
            "",
            f"Visited Nodes: {stats.get('visited_count', 0)}",
            f"Path Length: {stats.get('path_length', 0)}",
            f"Status: {self._get_status_text(stats)}"
        ]
        
        # Calculate panel height
        panel_height = len(stat_lines) * 25 + 20
        
        # Panel background
        pygame.draw.rect(win, self.colors['panel'], (x, y, width, panel_height))
        pygame.draw.rect(win, self.colors['border'], (x, y, width, panel_height), 2)
        
        # Draw statistics
        current_y = y + 10
        for line in stat_lines:
            if line == "Statistics:":
                text = self.font.render(line, True, self.colors['text'])
            elif line == "":
                current_y += 25
                continue
            else:
                text = self.small_font.render(line, True, self.colors['text_light'])
            
            win.blit(text, (x + 10, current_y))
            current_y += 25
        
        return panel_height
    
    def _get_status_text(self, stats: Dict[str, Any]) -> str:
        """Get human-readable status text from statistics."""
        if stats.get('is_running', False):
            return "Running..."
        elif stats.get('is_complete', False):
            if stats.get('path_found', False):
                return "Path Found!"
            else:
                return "No Path"
        else:
            return "Ready"
    
    def draw_title(self, win: pygame.Surface, x: int, y: int, width: int) -> int:
        """
        Draw the main title.
        
        Args:
            win (pygame.Surface): Surface to draw on
            x (int): X position
            y (int): Y position
            width (int): Width available for title
            
        Returns:
            int: Height of the drawn title
        """
        title = "Dijkstra's Pathfinding Simulator"
        title_text = self.title_font.render(title, True, self.colors['accent'])
        
        # Center the title
        text_rect = title_text.get_rect()
        title_x = x + (width - text_rect.width) // 2
        
        win.blit(title_text, (title_x, y))
        
        return text_rect.height + 10
    
    def draw_speed_indicator(self, win: pygame.Surface, x: int, y: int, width: int, speed: int) -> int:
        """
        Draw the current speed setting.
        
        Args:
            win (pygame.Surface): Surface to draw on
            x (int): X position
            y (int): Y position
            width (int): Width available
            speed (int): Current speed setting (1-10)
            
        Returns:
            int: Height of the drawn indicator
        """
        speed_text = f"Speed: {speed}/10"
        text = self.font.render(speed_text, True, self.colors['text'])
        
        # Panel background
        panel_width = 120
        panel_height = 35
        pygame.draw.rect(win, self.colors['panel'], (x, y, panel_width, panel_height))
        pygame.draw.rect(win, self.colors['border'], (x, y, panel_width, panel_height), 2)
        
        # Center text in panel
        text_rect = text.get_rect()
        text_x = x + (panel_width - text_rect.width) // 2
        text_y = y + (panel_height - text_rect.height) // 2
        
        win.blit(text, (text_x, text_y))
        
        return panel_height
    
    def show_splash_screen(self, win: pygame.Surface, width: int, height: int) -> bool:
        """
        Show a splash screen with instructions.
        
        Args:
            win (pygame.Surface): Surface to draw on
            width (int): Window width
            height (int): Window height
            
        Returns:
            bool: True if user wants to continue, False to quit
        """
        # Fill background
        win.fill(self.colors['background'])
        
        # Title
        title = "Dijkstra's Pathfinding Simulator"
        title_text = self.title_font.render(title, True, self.colors['accent'])
        title_rect = title_text.get_rect()
        title_x = (width - title_rect.width) // 2
        win.blit(title_text, (title_x, height // 4))
        
        # Instructions
        instructions = [
            "Welcome to the Dijkstra's Algorithm Visualizer!",
            "",
            "Instructions:",
            "• Left click to place/move the start point (green)",
            "• Right click to place/move the end point (red)",
            "• Middle click or Shift+click to add/remove barriers (blue)",
            "• Press SPACE to start the pathfinding algorithm",
            "• Press R to reset the entire grid",
            "• Press 1-10 to control animation speed",
            "",
            "Press any key to start, or ESC to quit"
        ]
        
        current_y = height // 2 - 100
        for instruction in instructions:
            if instruction == "Welcome to the Dijkstra's Algorithm Visualizer!":
                text = self.font.render(instruction, True, self.colors['text'])
            elif instruction == "Instructions:":
                text = self.font.render(instruction, True, self.colors['text'])
            elif instruction == "":
                current_y += 25
                continue
            else:
                text = self.small_font.render(instruction, True, self.colors['text_light'])
            
            text_rect = text.get_rect()
            text_x = (width - text_rect.width) // 2
            win.blit(text, (text_x, current_y))
            current_y += 25
        
        pygame.display.flip()
        
        # Wait for user input
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    else:
                        return True
        
        return True 