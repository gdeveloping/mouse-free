

class WindownProperty():
    def __init__(self, 
                 current_screen_width_column_size,
                 current_screen_height_row_size,
                 current_cell_width_column_size,
                 current_cell_height_row_size,
                 current_font_size,
                 x_start_in_current_screen,
                 y_start_in_current_screen) -> None:
        self.current_screen_width_column_size = current_screen_width_column_size
        self.current_screen_height_row_size = current_screen_height_row_size
        self.current_cell_width_column_size = current_cell_width_column_size
        self.current_cell_height_row_size = current_cell_height_row_size
        self.current_font_size = current_font_size
        self.x_start_in_current_screen = x_start_in_current_screen
        self.y_start_in_current_screen = y_start_in_current_screen