"""
Main Dijkstra visualizer class that coordinates all components.
"""
import pygame
import sys
from typing import Optional, Generator, Tuple, Dict, Any
from grid import Grid
from dijkstra import run_dijkstra_step_by_step
from ui import UI


class DijkstraVisualizer:
    """
    Main class that handles the Dijkstra pathfinding visualization application.
    
    Attributes:
        WIDTH (int): Window width
        HEIGHT (int): Window height
        GRID_WIDTH (int): Width of the grid area
        UI_WIDTH (int): Width of the UI panel
        ROWS (int): Number of grid rows/columns
        
        win (pygame.Surface): Main window surface
        clock (pygame.time.Clock): Pygame clock for frame rate control
        grid (Grid): The pathfinding grid
        ui (UI): UI components handler
        
        algorithm_generator (Optional[Generator]): Generator for step-by-step algorithm
        algorithm_stats (Dict[str, Any]): Current algorithm statistics
        running (bool): Whether the application is running
        algorithm_running (bool): Whether the algorithm is currently running
        animation_speed (int): Animation speed (1-10)
        frame_counter (int): Frame counter for animation timing
        middle_mouse_pressed (bool): Whether the middle mouse button is pressed
    """
    
    # Window dimensions
    WIDTH = 1000
    HEIGHT = 800
    GRID_WIDTH = 750
    UI_WIDTH = 250
    ROWS = 100
    
    # Animation speeds (frames to wait between steps)
    SPEED_SETTINGS = {
        1: 15,
        2: 12,
        3: 10,
        4: 8,
        5: 6,
        6: 4,
        7: 3,
        8: 2,
        9: 1,
        10: 1
    }
    
    def __init__(self):
        """Initialize the Dijkstra visualizer."""
        pygame.init()
        
        # Set up the display
        self.win = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Dijkstra's Pathfinding Simulator")
        
        # Initialize components
        self.clock = pygame.time.Clock()
        self.grid = Grid(self.ROWS, self.GRID_WIDTH)
        self.ui = UI()
        
        # Algorithm state
        self.algorithm_generator: Optional[Generator] = None
        self.algorithm_stats: Dict[str, Any] = {
            'visited_count': 0,
            'path_length': 0,
            'is_running': False,
            'is_complete': False,
            'path_found': False
        }
        
        # Application state
        self.running = True
        self.algorithm_running = False
        self.animation_speed = 5  # Default medium speed
        self.frame_counter = 0
        self.middle_mouse_pressed = False
        
        # Show splash screen
        if not self.ui.show_splash_screen(self.win, self.WIDTH, self.HEIGHT):
            self.running = False
    
    def handle_mouse_click(self, pos: Tuple[int, int], button: int, keys_pressed: pygame.key.ScancodeWrapper):
        """
        Handle mouse click events.
        
        Args:
            pos (Tuple[int, int]): Mouse position
            button (int): Mouse button (1=left, 2=middle, 3=right)
            keys_pressed: Current key states
        """
        # Only handle clicks in the grid area
        if pos[0] >= self.GRID_WIDTH:
            return
        
        # Don't allow changes while algorithm is running
        if self.algorithm_running:
            return
        
        # Get grid position
        row, col = self.grid.get_clicked_pos(pos)
        
        if button == 1:  # Left click - set start
            self.grid.set_start(row, col)
        elif button == 3:  # Right click - set end
            self.grid.set_end(row, col)
        elif button == 2 or keys_pressed[pygame.K_LSHIFT] or keys_pressed[pygame.K_RSHIFT]:
            # Middle click or shift+click - toggle barrier
            self.grid.set_barrier(row, col)
            self.middle_mouse_pressed = True
    
    def handle_mouse_motion(self, pos: Tuple[int, int]):
        if not self.middle_mouse_pressed or self.algorithm_running:
            return
        
        if pos[0] >= self.GRID_WIDTH:
            return
        
        row, col = self.grid.get_clicked_pos(pos)
        self.grid.set_barrier(row, col)
    
    def handle_mouse_release(self, button: int):
        if button == 2:
            self.middle_mouse_pressed = False
    
    def handle_keyboard_input(self, key: int):
        """
        Handle keyboard input.
        
        Args:
            key (int): Pygame key constant
        """
        if key == pygame.K_SPACE:
            # Start/stop algorithm
            if not self.algorithm_running and self.grid.is_ready_for_pathfinding():
                self.start_algorithm()
            elif self.algorithm_running:
                self.stop_algorithm()
        
        elif key == pygame.K_r:
            # Reset grid
            self.reset_grid()
        
        elif key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, 
                     pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9, pygame.K_0]:
            # Set animation speed
            if key == pygame.K_0:
                self.animation_speed = 10
            else:
                self.animation_speed = key - pygame.K_0
        
        elif key == pygame.K_ESCAPE:
            # Quit application
            self.running = False
    
    def start_algorithm(self):
        """Start the Dijkstra algorithm visualization."""
        if not self.grid.is_ready_for_pathfinding():
            return
        
        # Reset any previous algorithm data
        self.grid.reset_algorithm_data()
        self.grid.update_neighbors()
        
        # Create algorithm generator
        self.algorithm_generator = run_dijkstra_step_by_step(
            self.grid.start_node, 
            self.grid.end_node
        )
        
        self.algorithm_running = True
        self.frame_counter = 0
        
        # Reset stats
        self.algorithm_stats = {
            'visited_count': 0,
            'path_length': 0,
            'is_running': True,
            'is_complete': False,
            'path_found': False
        }
    
    def stop_algorithm(self):
        """Stop the algorithm visualization."""
        self.algorithm_running = False
        self.algorithm_generator = None
        self.algorithm_stats['is_running'] = False
    
    def reset_grid(self):
        """Reset the entire grid."""
        self.stop_algorithm()
        self.grid.reset_grid()
        self.algorithm_stats = {
            'visited_count': 0,
            'path_length': 0,
            'is_running': False,
            'is_complete': False,
            'path_found': False
        }
    
    def update_algorithm(self):
        """Update the algorithm by one step if needed."""
        if not self.algorithm_running or not self.algorithm_generator:
            return
        
        # Check if it's time for the next step based on animation speed
        speed_delay = self.SPEED_SETTINGS[self.animation_speed]
        self.frame_counter += 1
        
        if self.frame_counter < speed_delay:
            return
        
        self.frame_counter = 0
        
        try:
            # Get next step from algorithm
            continue_running, current_node, stats = next(self.algorithm_generator)
            self.algorithm_stats = stats
            
            if not continue_running:
                self.algorithm_running = False
                self.algorithm_generator = None
                
        except StopIteration:
            # Algorithm completed
            self.algorithm_running = False
            self.algorithm_generator = None
            self.algorithm_stats['is_complete'] = True
    
    def draw(self):
        """Draw the entire application."""
        # Clear screen
        self.win.fill((255, 255, 255))
        
        # Draw grid
        self.grid.draw(self.win)
        
        # Draw UI elements in the right panel
        ui_x = self.GRID_WIDTH + 10
        current_y = 10
        
        # Title
        title_height = self.ui.draw_title(self.win, ui_x, current_y, self.UI_WIDTH - 20)
        current_y += title_height + 10
        
        # Statistics
        stats_height = self.ui.draw_statistics(self.win, ui_x, current_y, self.UI_WIDTH - 20, self.algorithm_stats)
        current_y += stats_height + 10
        
        # Speed indicator
        speed_height = self.ui.draw_speed_indicator(self.win, ui_x, current_y, self.UI_WIDTH - 20, self.animation_speed)
        current_y += speed_height + 10
        
        # Legend
        legend_height = self.ui.draw_legend(self.win, ui_x, current_y, self.UI_WIDTH - 20)
        current_y += legend_height + 10
        
        # Controls
        self.ui.draw_controls(self.win, ui_x, current_y, self.UI_WIDTH - 20)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Run the main application loop."""
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    keys_pressed = pygame.key.get_pressed()
                    self.handle_mouse_click(pygame.mouse.get_pos(), event.button, keys_pressed)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.handle_mouse_release(event.button)
                
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(pygame.mouse.get_pos())
                
                elif event.type == pygame.KEYDOWN:
                    self.handle_keyboard_input(event.key)
            
            # Update algorithm
            self.update_algorithm()
            
            # Draw everything
            self.draw()
            
            # Control frame rate
            self.clock.tick(60)  # 60 FPS
        
        # Cleanup
        pygame.quit()
        sys.exit()


def main():
    """Main entry point for the application."""
    try:
        visualizer = DijkstraVisualizer()
        visualizer.run()
    except Exception as e:
        print(f"Error running Dijkstra visualizer: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main() 