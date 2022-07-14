Ludo - Game
Ricardo Selas Vieira de Andrade

Full game
Build Contents
Game complete and working
requirements
Python 3

Pygame With Python installed, it is possible to install PyGame through the command: pip install pygame or python -m pip install pygame

MySQL and Connector: During MySQL installation, it is possible to install the Connector directly in the installer, or installed later through the command pip install mysql-connector or python -m pip install mysql-connector. In addition, it will be necessary to note the username and password that was registered during installation.

The other modules used are already installed in the standard Python distribution.

How to play
To start the game, you need to run the main.py file

When running the program, it will open a menu screen. From this screen, you can create a two- to four-player match or load a previous match. It is also possible to configure the connection to the database, which is essential for the game to function. To do so, it is necessary to access the configuration screen, which allows configuring the user, password and database connection server.

When starting or loading a game, the menu screen will close, and a screen with the game will open. Player colors are pre-selected.

During the game, it is possible to disable the sound effects, as well as the music, through the buttons on the left.

To interact in the game, you must use the mouse to select which pawn to move, or to roll the dice.

The game can be stopped at any time by closing the game screen. It can be recovered from the last round played.

At the end of a match, the score of the winners will be displayed, and the game will be closed automatically.

Tests
The tests file is in teste/test.py. When running, it will do all game tests automatically.