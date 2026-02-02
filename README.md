[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/Kf5HLjuv)

# Ping-Pong Game Tool Comparison 

This repository contains two implementations of a Python Ping-Pong game created using Cursor and GeminiCLI. The objective of the lab is to compare the tools based on code quality, speed of generation, ease of use, debugging experience, and flexibility.

## Repository Structure

```
ping_pong_cursor.py               # Cursor version
ping_pong_gemini.py         # Gemini basic version
ppg.py      # Gemini enhanced version
README.md
```

## How to Run

1. Install pygame:
   ```
   pip install pygame
   ```

2. Run any version:
   ```
   python cursor_pingpong.py
   python gemini_pingpong_basic.py
   python gemini_pingpong_enhanced.py
   ```

---

# Part A — Cursor Implementation Analysis

## Code Quality
- Cursor generated readable and well-structured code.
- The preview and diff features made it easy to follow changes.
- However, the logic often contained recurring issues:
  - Paddle freezing after first interaction.
  - Vertical speed (`dy`) too strong or inconsistent.
  - Paddle movement too fast or too slow.
- Even after 4–5 rounds of fixes, the same problems frequently reappeared.
- Readability was strong, but correctness and stability were weak.

## Speed of Generation
- A working prototype was produced within two minutes.
- Each iteration took less than 30 seconds.
- But because multiple iterations were needed, total time increased.

## Ease of Use
- Cursor is very user-friendly and intuitive.
- Code preview, automatic explanations, and step-by-step reasoning were helpful.

## Debugging and Error Handling
- Debugging became difficult because issues kept returning.
- Multiple attempts to fix the paddle movement and bounce logic were unsuccessful.
- Eventually reached the usage limit before solving all game issues.
- Needed to copy the code into Gemini/ChatGPT to diagnose certain bugs.

## Flexibility and Customization
- Cursor supports customization, but modifications often broke existing logic.
- Attempts to add menus, scoring systems, or angle dynamics caused older bugs to reappear.
- Final game was incomplete because recurring errors remained unresolved.

---

# Part B — Gemini CLI Implementation Analysis

Two versions were generated: a basic version and an enhanced version.

## 1. Basic Version
- Simple, stable Pygame implementation.
- No paddle freezing issues.
- Clear structure with constants grouped at the top.
- Worked on the first try with no syntax errors.

## 2. Enhanced Version
- Added start menu, gradient background, rounded paddles, and improved visuals.
- Implemented 11-point scoring with win-by-2 logic.
- Added match structure (best of 3 sets).
- Added procedural sound (no external assets required).
- Used a clear game-state structure (START_MENU, PLAYING, GAME_OVER).

## Speed of Generation
- Generated full files quickly once WriteTodos was disabled.
- First version were produced in a single pass.Second has some problem like Cursor did,still haven't figure it out.

## Ease of Use
- Initially confusing due to Todo Mode.
- After disabling WriteTodos, the workflow became direct and easy to use. 

## Debugging and Error Handling
- Both versions ran without syntax errors.
- Debugging mainly involved tuning parameters (speed, paddle size).
- Much easier to stabilize compared to Cursor.

## Flexibility and Customization
- Easy to modify due to clean structure.
- Enhanced version showed strong scalability for new features.
- Clear separation of constants, game state, and rendering.

---

# Part C — Comparison Between Tools

## Code Quality
- Cursor: readable but logically unstable; repeated bugs.
- Gemini: stable baseline and better structure.The enhanced version repeated the same problem as Cursor done, the paddle stucked after the first serve .

## Speed of Generation
- Cursor: fast per iteration, but overall slowed by repeated bug fixes.
- Gemini: fast and consistent; generated working versions in one step.

## Ease of Use
- Cursor: very easy to use, strong UI/UX, helpful previews.
- Gemini: easy after disabling Todo Mode; otherwise slowed by unnecessary interaction.Also I think is very humor when you waiting for the output, there are many humor phrases make you laugh.

## Debugging Experience
- Cursor: Medium, because the same problems reappeared many times.
- Gemini: Medium, for the easier task with no issue, but with a more advanced version, these ai assistant seems like cannot solve the real problem.

## Flexibility and Customization
- Cursor: flexible, changes often caused regressions.
- Gemini: flexible ,and with no sandbox, morelike openclaw, can direclty change and fix the file on my computer, with strong internal structure; easier to extend.

---

# Final Reflection

Cursor provided a smooth editing experience and produced readable code, but persistent gameplay issues and repeated debugging cycles made development inefficient. Gemini CLI produced more stable and scalable implementations with fewer iterations, especially after disabling Todo Mode. For this project, Gemini was the more reliable tool for generating a functional and extended Ping-Pong game, while Cursor remained strong as an interactive editor but weaker in stable logic generation.


