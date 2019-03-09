Maze Generation
===============

This folder has some scripts that generate mazes, using two different algorithms.

`mazegenerator.py` generates mazes randomly by creating a tree with a graph-search algorithm; `config.ini` configures the size and aspect of such mazes.

The three `.py` files that start with `wilson_` use [Wilson's algorithm](https://en.wikipedia.org/wiki/Loop-erased_random_walk) to create the maze.
 - `wilson_generator.py` ~~equires Python 3.7~~ (used to require Python3.7 but then I couldn't find a way to freeze it, so now it) runs with Python3 and pygame. The file `wilsonconfig.ini` configures the size of the maze and possibly the directory to which screenshots will be saved. The controls are as follows:
   * upon running the script, the maze starts being built _automagically_
   * pressing 'S' will take a screenshot
   * after the maze is built, pressing 'F' will flood the maze with colour
   * pressing 'Q' will close the program at any time
 - `wilson_generator_bad.py` is the prototyped version of `wilson_generator.py`. It is less efficient and it starts flooding the maze as soon as the maze is built.
 - `wilson_generator_partial.py` is the same as `wilson_generator_bad.py` except that it only refreshes the image when you hit the spacebar
 
 In the `bin` you can find some sample mazes created by the two programs.
