[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Kf5HLjuv)

# Ping-Pong Game (Python)

A two-player Ping-Pong game built with **Pygame**. Created for a lab exercise comparing coding tools.

## Requirements Met

| Requirement | Implementation |
|-------------|----------------|
| **Game environment** | Playing field (800×500), two paddles, one ball, center net |
| **Player input** | Player 1: W/S; Player 2: Up/Down arrows; ESC to quit |
| **Ball movement & collisions** | Ball moves and bounces off top/bottom walls and paddles; angle depends on where the ball hits the paddle |
| **Score keeping** | Scores shown at top; first to 11 wins; game resets after win |

## How to Run

1. **Install Python** (3.7+).

2. **Open Command Prompt or PowerShell** (do not just double‑click the .py file—you won’t see errors).

3. **Go to the game folder and install Pygame:**
   ```bash
   cd C:\Users\lenovo\ping_pong_game
   pip install pygame
   ```
   If `pip` doesn’t work, try: `py -3 -m pip install pygame`

4. **Start the game:**
   ```bash
   python ping_pong.py
   ```
   Or: `py ping_pong.py`

4. **Controls:**
   - **Player 1 (left paddle):** `W` = up, `S` = down  
   - **Player 2 (right paddle):** `↑` = up, `↓` = down  
   - **Quit:** `ESC` or close the window  

## Project Layout

```
ping_pong_game/
├── ping_pong.py      # Main game (single file, ~220 lines)
├── requirements.txt  # pygame>=2.5.0
└── README.md         # This file
```

## Troubleshooting

- **No window appears / game “doesn’t run”**  
  1. **Install pygame** (if needed): `python -m pip install pygame`  
  2. **Run from an external Command Prompt**, not only from Cursor’s terminal: press **Win+R**, type `cmd`, Enter, then:
     ```text
     cd C:\Users\lenovo\ping_pong_game
     python -u ping_pong.py
     ```
     The game window may open *behind* the Cursor window—check the **taskbar** for “Ping-Pong” and click it.  
  3. **Or double‑click `run_ping_pong.bat`** in the `ping_pong_game` folder. A console will open and start the game (again, check the taskbar if you don’t see the window).

- **`pip` not found**  
  Use: `python -m pip install pygame` (or `py -3 -m pip install pygame`).

- **Double‑clicking the .py file does nothing**  
  Use Command Prompt as above, or double‑click `run_ping_pong.bat` so you can see any messages.

## Customization

Constants at the top of `ping_pong.py` can be changed:

- `WINDOW_WIDTH`, `WINDOW_HEIGHT` — screen size  
- `PADDLE_SPEED`, `PADDLE_HEIGHT` — paddle behavior  
- `BALL_SPEED_INITIAL`, `BALL_SPEED_INCREMENT` — ball speed  
- `WINNING_SCORE` — points needed to win (default 11)  

---

## Lab: Tool Comparison (Analysis Template)

After building the game with **Tool A** and **Tool B**, fill in or adapt the following.

### 1. Code quality

- **Readability:** Is naming clear? Are sections (setup, input, physics, draw) easy to find?
- **Maintainability:** Can you change paddle speed or winning score in one place? Are constants separated from logic?
- **Efficiency:** Is the game loop simple (update → draw → tick)? Any unnecessary work per frame?
- **Best practices:** Single responsibility, constants at top, docstring at top of file, `if __name__ == "__main__"` for entry point.
- **Comments:** Are comments used for intent (e.g., “Angle based on where ball hit paddle”) rather than restating the code?

**This implementation:** One main file, constants at top, comments for each major block and non-obvious logic.

### 2. Speed of generation

- How long from “I want a Ping-Pong game” to a runnable prototype?
- Did you need multiple rounds of prompts or fixes?
- Did the tool produce runnable code on the first try?

### 3. Ease of use

- How clear were the instructions you had to give (e.g., “Ping-Pong with two paddles and score”)?
- Did you need to look up Pygame or Python syntax, or did the tool generate correct usage?
- How easy was it to install and run (e.g., `pip install -r requirements.txt` and `python ping_pong.py`)?

### 4. Debugging and error handling

- If something broke (e.g., ball stuck in paddle, wrong score), how easy was it to describe the bug and get a fix?
- Did the tool suggest adding checks (e.g., paddle bounds, ball reset on goal)?
- How did you handle Pygame not installed or wrong Python version?

### 5. Flexibility and customization

- How easily could you change window size, paddle size, or winning score?
- Could you add features (e.g., sound, AI opponent, menus) with small, clear instructions?
- Did the tool keep the code structured so that new features fit in without rewriting everything?

---

Use this README and the comparison section when writing your lab report.
