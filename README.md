# Wordle


It is my own project that i built for myself just out of boredom, so it won't be supported or maintained :)
I know, code in there is really dirty and buggy, but i don't care because it works well enough.

**auto_wordle bug:**
Unfortunately, the script gets data for game state by reading colours of specified pixels on the screen,
so it won't work properly if your UI is misplaced (windowed mode or just different browser or OS).
Though, pixels which are used to determine the game state can be set at the begginning of a file.


**Description of all files in repository:**

**Database.txt** - plain text file with a database of 5-letter english words, all lowercase, separated by a newline (\n)

**Wordle.py** - tkinter GUI game which copies real game "Wordle" at https://www.nytimes.com/games/wordle/index.html

**auto_wordle** - script which opens Wordle game at previously specified url and plays it. It detects game state by taking screenshots and looking at specific pixels'
colours, so it is advised to open game on 1980x1080 monitor, in chrome browser, not in full-screen mode and not scrolling the page. Script usually **goes rogue**
(even though it shouldn't) after completing the game, so I recommend to stop it immediately after.
