# 8 Puzzle Game

This is a simple implementation of the classic 8 puzzle game using Python. The application also incorporates the A* algorithm to solve the 8 puzzle problem.

## Game Description

The 8 puzzle game is played on a 3x3 grid with 8 numbered tiles and an empty space. The objective of the game is to arrange the tiles in ascending order from left to right, top to bottom, with the empty space at the bottom right corner.

## Screenshot
These are images of the application:
![](https://imgur.com/UUyeLwD.png)
![](https://imgur.com/D6XqyeC.png)

## A* Algorithm

The A* algorithm is an informed search algorithm that finds the shortest path between a starting state and a goal state. In the context of the 8 puzzle game, the A* algorithm is used to solve the puzzle automatically.

The algorithm works by evaluating the cost of each possible move and estimating the cost of reaching the goal state from that move. It uses a heuristic function, such as the Manhattan distance, to estimate the cost. The A* algorithm then selects the move with the lowest cost and repeats the process until it reaches the goal state.

By incorporating the A* algorithm, this application provides an option to solve the puzzle automatically. The player can choose to let the algorithm find the optimal solution or try to solve the puzzle manually.

## Features

- Randomized initial board configuration.
- Move tiles by sliding or clicking them into the empty space.
- Detects and prevents illegal moves.
- Tracks the number of moves made by the player.
- Provides an option to reset the game board.
- Validates the winning condition and displays a victory message.
- Offers a "Guide" option to automatically solve the puzzle using the A* algorithm.

## How to Run

1. Download the ZIP file of the game from the GitHub repository.
2. Extract the contents of the ZIP file to a desired location on your computer.
3. Navigate to the extracted folder.
4. Double-click the `.exe` file to start the game.
5. Follow the on-screen instructions to play the game.
6. Use the arrow keys or the mouse to move the tiles.
   - For arrow key controls, press the arrow keys to slide the tiles into the empty space.
   - For mouse controls, click on a tile adjacent to the empty space to move it into the empty space.
7. Click on the "Guide" option during the game to utilize the A* algorithm and automatically solve the puzzle.


## Contributors
- Lương Vĩnh Lợi
- Phạm Duy Phú
- Đặng Hữu Tấn
- Hoàng Đình Trung

## About
This is the project for the Algorithm Design and Analysis course by Group 6, K65A6, VNU-HUS.
<br /><br /><em>Hà Nội 2023</em>
