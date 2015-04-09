## VisionBot - An Image Recognition Bot

VisionBot is a Python program that can help you play [Save The Earth!](http://www.savetheearth.es/)It was written to learn a little about Python and about how to create a bot to help you 'cheat' at a game. [How to Build a Python Bot That Can Play Web Games](http://code.tutsplus.com/tutorials/how-to-build-a-python-bot-that-can-play-web-games--active-11117)was used as a guide for this project. 

To use, run ScreenGrab.py. Make sure Save The Earth is running and is visible on your screen. 

* * *

### What is Save The Earth!?

Save The Earth is an [incremental](http://en.wikipedia.org/wiki/Incremental_game) game where you split your time between clicking on aliens (to destroy them and gain resources) and upgrading your forces. There is no hard end to the game but once you've researched every upgrade there is little point in continuing. Like most incrementals it can take a very long time to get to the end of the game. That is where this bot comes in... 

### How Does the Bot Work?

The goal of the bot is to have it automatically click all of the aliens on the screen as fast as possible. The question is how can the bot know where to click? We need two things, a screenshot of the game window, and an image of the alien. 

To get an image of the alien I took a screenshot of the game, opened it in Paint, and cropped it down to just a 3x3 pixel section of the alien. Why 3x3? That was big enough to be unique to the alien so that we wouldn't accidentally click on other parts of the screen. 

Now we have a large image to search (the game window) and a small 3x3 image that we are looking for. The bot scans the large image pixel by pixel. If a match is found, the bot will move your cursor to the location of the match and click the alien. It performs the loop of taking screenshots and scanning them until it is closed. 

To summarize: 

1.  Capture image of the game
2.  Scan image for instances of aliens
3.  When an alien is found, move cursor to that location and click
4.  When end of game image is reached, return to step 1

### Libraries Needed

*   NumPy
*   Python for Windows Extensions (Pywin32)
*   Python Imaging Library (PIL)
