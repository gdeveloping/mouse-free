

class WindownProperty():
    def __init__(self) -> None:
        self.x_start_of_current_screen = 0
        self.y_start_of_current_screen = 0
        
        self.x_start_in_current_screen = 0
        self.y_start_in_current_screen = 0

        self.current_screen_width_column_size = 0
        self.current_screen_height_row_size = 0

        self.current_cell_width_column_size = 0
        self.current_cell_height_row_size = 0
        
        self.current_font_size = 0

        self.width_of_current_screen = 0
        self.height_of_current_screen = 0
        
        
class MousenProperty():
    def __init__(self) -> None:
        self.x_old = 0
        self.y_old = 0