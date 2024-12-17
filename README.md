---

# Cat and Mouse Split-Screen Game 🎮

A split-screen **Cat and Mouse game** built using Python's Pygame library. The game allows players to place mousetraps strategically to eliminate enemies while competing against an AI using a **genetic algorithm** for mousetrap placement.

## Features

- 🎯 **Split-Screen Gameplay**: Compete against the AI in a split-screen environment.
- 🧠 **Genetic Algorithm**: The AI uses a genetic algorithm to decide optimal mousetrap placement.
- 💥 **mousetrap Defense Mechanics**: Place mousetraps manually to attack and defeat incoming enemies.
- 🔊 **Sound Effects and Music**: Background music and effects enhance gameplay.
- 🏆 **Dynamic Win Conditions**: Compete to eliminate a set number of enemies before the AI does.

---

## How to Play

1. **Start the Game**:
   - Run the Python script.
   - Press `ENTER` at the main menu to begin.

2. **Placing mousetraps**:
   - Use the **mouse** to click on the left side of the screen (Player's side) to place mousetraps.
   - mousetraps will automatically attack nearby enemies.

3. **Objective**:
   - Eliminate **5 enemies** before the AI to win the game.

4. **AI Side**:
   - The AI will automatically place mousetraps and eliminate enemies using its pre-calculated strategy.

5. **Winning**:
   - If you defeat all enemies first, you win.
   - If the AI eliminates all enemies first, the AI wins.

---

## Controls

- **Mouse Click**: Place mousetraps on the player's grid.
- **ESC**: Quit the game at any time.
- **ENTER**: Start or restart the game.

---

## Dependencies

- **Python 3.x**
- **Pygame** (install via pip)

### Installation

1. Install Python and Pygame:
   ```bash
   pip install pygame
   ```

2. Place all required files (e.g., sound and music files) in a folder structure as follows:

   ```
   game_folder/
   ├── bulk_commit.ps1       # (Optional script for bulk commits)
   ├── cat_mouse_game.py     # The main game script
   ├── tracks/
   │   ├── background_music_1.mp3
   │   ├── background_music_2.mp3
   │   ├── enemy_hit5.mp3
   │   ├── win_sound.mp3
   │   └── lose_sound.mp3
   ```

3. Run the game:
   ```bash
   python cat_mouse_game.py
   ```

---

## Game Overview

### Grid Layout:
- The screen is divided into **two halves**:
   - Left Half: Player's area for mousetrap placement.
   - Right Half: AI's area for automated mousetrap placement.

### mousetraps:
- **Player**: Manually places mousetraps using mouse clicks.
- **AI**: Automatically places mousetraps using a genetic algorithm.

### Enemies:
- Move randomly but stay within grid boundaries.
- Have health bars that decrease when mousetraps attack.

---

## Notes

- Ensure all **music and sound effect files** are located in the specified `tracks` folder.
- Modify the `n` variable in the code to adjust the number of targets(mouse) required to win.

---

## Future Improvements (To-Do)

- Add more **enemy types** with different behaviors.
- Implement **upgradable mousetraps**.
- Introduce more **levels** and increasing difficulty.
- Improve AI mousetrap placement strategies for better competition.

---

## Credits

- **Game Development**: Built using Python and Pygame.
<!-- - **Sound Effects and Music**: (List or link if sourced from a library). -->

---

## License

This project is released under the **MIT License**. Feel free to modify and distribute it.

--- 

Enjoy the game! 😊
