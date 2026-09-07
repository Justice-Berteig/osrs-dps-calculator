# About
This program is used to calculate a player's average damage per second against a
given enemy in Old School Runescape. It uses a Markov Chain to account for any
damage that would be lost by dealing more damage than the enemy has health
remaining as well as the enemy's health regeneration. Results are displayed with
Matplotlib.

Currently this program doesn't work for general DPS calculations, I made it
because I wanted to know how much of a difference different arrow types made
against ogresses. I hope to make it work for general use in the future.

# Instructions
1. Clone and cd into the repo
2. Create virtual environment with `python -m venv venv`
3. Enter virtual environment with `source venv/bin/activate`
4. Install dependencies with `pip install -r requirements.txt`
5. Leave virtual environment with `deactivate`
6. Run the program:
    - On Linux use `./run.sh` to run the program
    - On Windows re-enter the virtual environment and run main.py with python
