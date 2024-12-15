# ScreenlessTicTacToe
Python Code for my group's project in a course callsed 'Interactions Beyond Screens': A screenless, wall-mounted TicTacToe game that utilizes a RasberryPi 5 to power a board of 18 LED's arranged in a 3x3 matrix on an Acrylic Board. The Game is controlled by 3 buttons that allow for a retro style interaction with no restrictions for time played.

## Project Overview

This project was developed as part of CCT490: Interactions Beyond Screens course. It reimagines the classic Tic-Tac-Toe game by removing the screen interface entirely and replacing it with physical LED lights and button controls. The game is built on a transparent acrylic board, creating a unique, tactile gaming experience.

### Key Features

- LED-based game board visualization (Red LEDs for Player X, Green LEDs for Player O)
- Three-button control system:
  - Select Button: Cycle through available positions
  - Confirm Button: Place marker in selected position
  - Reset Button: Start a new game
- Victory celebration light show animation
- Transparent acrylic board design
- Button debouncing for reliable input
- Real-time visual feedback through LED indicators

## Hardware Requirements

- Raspberry Pi (any model with GPIO pins)
- 18 LEDs:
  - 9 Red LEDs (Player X)
  - 9 Green LEDs (Player O)
- 3 Push buttons
- Resistors (one for each LED and button)
- Jumper wires
- Transparent acrylic board
- Breadboard(s)

## GPIO Pin Configuration

### LED Pins
```python
RED_LEDS = {
    0: 2,   # Top left
    1: 3,   # Top middle
    2: 4,   # Top right
    3: 17,  # Middle left
    4: 27,  # Center
    5: 22,  # Middle right
    6: 10,  # Bottom left
    7: 9,   # Bottom middle
    8: 11   # Bottom right
}

GREEN_LEDS = {
    0: 14,  # Top left
    1: 15,  # Top middle
    2: 18,  # Top right
    3: 23,  # Middle left
    4: 24,  # Center
    5: 25,  # Middle right
    6: 8,   # Bottom left
    7: 7,   # Bottom middle
    8: 12   # Bottom right
}
```

### Button Pins
```python
SELECT_BTN = 5
CONFIRM_BTN = 6
RESET_BTN = 13
```

## Software Dependencies

- Python 3
- gpiod library (`pip install gpiod`)

## Installation & Setup

1. Clone this repository:
```bash
git clone [repository-url]
cd screenless-tictactoe
```

2. Install required Python package:
```bash
pip install gpiod
```

3. Connect the hardware components according to the GPIO pin configuration above.

4. Run the game:
```bash
python tictactoe-gpiod.py
```

## How to Play

1. **Starting the Game**: When you run the program, Player X starts first.

2. **Making Moves**:
   - Use the Select button to cycle through available positions
   - Current selection is indicated by a flashing LED
   - Press Confirm to place your marker (Red LED for X, Green LED for O)
   - Players alternate turns after each valid move

3. **Winning the Game**:
   - Get three in a row (horizontally, vertically, or diagonally)
   - Winner is celebrated with a victory light show
   - Use Reset button to start a new game

4. **Reset**: Press the Reset button at any time to clear the board and start over

## Technical Implementation

The game uses the `gpiod` library for GPIO control, featuring:

- Debounced button inputs to prevent false triggers
- LED state management for game visualization
- Win condition detection across rows, columns, and diagonals
- Victory animation sequence
- Clean GPIO handling with proper cleanup

## Contributors

- Youssef Ghanem
- Ali Taha
- Omar Al Hunaidi

## License

N/A

## Acknowledgments

Special thanks to Professor Samar Sabie and TA Seemin Syed teaching the CCT490 course at the University of Toronto Mississauga and providing all the help to make our vision a reality and for givubg us the opportunity to explore interactions beyond traditional screen interfaces.
