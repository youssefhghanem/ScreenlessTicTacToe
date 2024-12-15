import gpiod
import time
from enum import Enum

class Player(Enum):
    NONE = 0
    X = 1  # Red LED
    O = 2  # Green LED

# GPIO Pin assignments (using physical pin numbers)
RED_LEDS = {
    0: 2,  # Top left
    1: 3,  # Top middle
    2: 4,  # Top right
    3: 17, # Middle left
    4: 27, # Center
    5: 22, # Middle right
    6: 10, # Bottom left
    7: 9,  # Bottom middle
    8: 11  # Bottom right
}

GREEN_LEDS = {
    0: 14, # Top left
    1: 15, # Top middle
    2: 18, # Top right
    3: 23, # Middle left
    4: 24, # Center
    5: 25, # Middle right
    6: 8,  # Bottom left
    7: 7,  # Bottom middle
    8: 12  # Bottom right
}

# Button GPIO pins
SELECT_BTN = 5
CONFIRM_BTN = 6
RESET_BTN = 13

DEBOUNCE_TIME = 0.05  # 50 milliseconds

class TicTacToe:
    def __init__(self):
        # Initialize gpiod chip
        self.chip = gpiod.Chip('gpiochip0')
        
        # Setup LED lines
        self.red_leds = {}
        self.green_leds = {}
        for pos, pin in RED_LEDS.items():
            self.red_leds[pos] = self.chip.get_line(pin)
            self.red_leds[pos].request(consumer="tictactoe", type=gpiod.LINE_REQ_DIR_OUT)
            
        for pos, pin in GREEN_LEDS.items():
            self.green_leds[pos] = self.chip.get_line(pin)
            self.green_leds[pos].request(consumer="tictactoe", type=gpiod.LINE_REQ_DIR_OUT)
        
        # Setup button lines with pull-up
        self.select_btn = self.chip.get_line(SELECT_BTN)
        self.confirm_btn = self.chip.get_line(CONFIRM_BTN)
        self.reset_btn = self.chip.get_line(RESET_BTN)
        
        self.select_btn.request(consumer="tictactoe", type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
        self.confirm_btn.request(consumer="tictactoe", type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
        self.reset_btn.request(consumer="tictactoe", type=gpiod.LINE_REQ_DIR_IN, flags=gpiod.LINE_REQ_FLAG_BIAS_PULL_UP)
        
        # Button state tracking for debouncing
        self.btn_states = {
            'select': {'current': 1, 'previous': 1, 'last_press': 0},
            'confirm': {'current': 1, 'previous': 1, 'last_press': 0},
            'reset': {'current': 1, 'previous': 1, 'last_press': 0}
        }
        
        self.reset_game()
    
    def cleanup(self):
        """Release all GPIO lines"""
        for led in self.red_leds.values():
            led.release()
        for led in self.green_leds.values():
            led.release()
        self.select_btn.release()
        self.confirm_btn.release()
        self.reset_btn.release()
        self.chip.close()
    
    def debounce(self, btn, btn_type):
        """Debounce button input"""
        current_time = time.time()
        state = self.btn_states[btn_type]
        
        state['current'] = btn.get_value()
        
        if (state['current'] != state['previous'] and 
            (current_time - state['last_press']) > DEBOUNCE_TIME):
            state['last_press'] = current_time
            state['previous'] = state['current']
            return state['current'] == 0  # Button pressed (active low)
        
        state['previous'] = state['current']
        return False

    def reset_game(self):
        """Reset the game state and turn off all LEDs"""
        self.board = [[Player.NONE] * 3 for _ in range(3)]
        self.current_player = Player.X
        self.selected_row = 0
        self.selected_col = 0
        self.game_over = False
        self.moves_count = 0
        
        # Turn off all LEDs
        for led in self.red_leds.values():
            led.set_value(0)
        for led in self.green_leds.values():
            led.set_value(0)
        
        print("\nNew game started!")
        print("Player X goes first")
        print("Use Button 1 to select position")
        print("Use Button 2 to confirm position")
        print("Use Button 3 to reset game\n")
    
    def get_next_available_position(self):
        """Find next available position"""
        current_pos = self.selected_row * 3 + self.selected_col
        for offset in range(1, 10):
            next_pos = (current_pos + offset) % 9
            row = next_pos // 3
            col = next_pos % 3
            if self.board[row][col] == Player.NONE:
                return row, col
        return self.selected_row, self.selected_col
    
    def flash_selected_position(self):
        """Flash the LED at the currently selected position"""
        if self.game_over:
            return
            
        position = self.selected_row * 3 + self.selected_col
        led = self.red_leds[position] if self.current_player == Player.X else self.green_leds[position]
        
        if self.board[self.selected_row][self.selected_col] == Player.NONE:
            led.set_value(1)
            time.sleep(0.2)
            led.set_value(0)
            time.sleep(0.2)
    
    def place_marker(self):
        """Place the current player's marker at the selected position"""
        if self.board[self.selected_row][self.selected_col] != Player.NONE:
            return False
            
        self.board[self.selected_row][self.selected_col] = self.current_player
        position = self.selected_row * 3 + self.selected_col
        led = self.red_leds[position] if self.current_player == Player.X else self.green_leds[position]
        led.set_value(1)
        self.moves_count += 1
        return True
    
    def check_winner(self):
        """Check if there's a winner"""
        # Check rows and columns
        for i in range(3):
            if (self.board[i][0] == self.board[i][1] == self.board[i][2] != Player.NONE or
                self.board[0][i] == self.board[1][i] == self.board[2][i] != Player.NONE):
                return self.board[i][i]
        
        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != Player.NONE or
            self.board[0][2] == self.board[1][1] == self.board[2][0] != Player.NONE):
            return self.board[1][1]
        
        # Check for draw
        if self.moves_count == 9:
            return Player.NONE
            
        return False
    
    def celebrate_win(self, winner):
        """Victory celebration pattern"""
        leds = self.red_leds if winner == Player.X else self.green_leds
        for _ in range(5):
            # All on/off
            for led in leds.values():
                led.set_value(1)
            time.sleep(0.3)
            for led in leds.values():
                led.set_value(0)
            time.sleep(0.3)
            
            # Sequential
            for led in leds.values():
                led.set_value(1)
                time.sleep(0.1)
                led.set_value(0)
    
    def run_game(self):
        """Main game loop"""
        try:
            while True:
                # Reset button handling
                if self.debounce(self.reset_btn, 'reset'):
                    self.reset_game()
                    continue
                
                if self.game_over:
                    continue
                
                # Flash current selection
                self.flash_selected_position()
                
                # Select button handling
                if self.debounce(self.select_btn, 'select'):
                    print(f"Player {self.current_player.name} selecting position...")
                    self.selected_row, self.selected_col = self.get_next_available_position()
                
                # Confirm button handling
                if self.debounce(self.confirm_btn, 'confirm'):
                    if self.place_marker():
                        print(f"Player {self.current_player.name} placed at position ({self.selected_row}, {self.selected_col})")
                        winner = self.check_winner()
                        if winner:
                            self.game_over = True
                            if winner != Player.NONE:
                                print(f"Player {winner.name} wins!")
                                self.celebrate_win(winner)
                            else:
                                print("It's a draw!")
                        else:
                            self.current_player = Player.O if self.current_player == Player.X else Player.X
                            print(f"\nPlayer {self.current_player.name}'s turn")
                            self.selected_row, self.selected_col = self.get_next_available_position()

        except KeyboardInterrupt:
            print("\nGame terminated by user")
        finally:
            self.cleanup()

if __name__ == "__main__":
    try:
        game = TicTacToe()
        game.run_game()
    except Exception as e:
        print(f"Error: {e}")
