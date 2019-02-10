import sys
from cx_Freeze import setup, Executable

setup(
    name = "Maze Generator",
    version = "1",
    description = "A program that generates random mazes with variable width and height, based on Wilson's algorithm for uniform spanning tree generation.",
    executables = [Executable("wilson_generator.py", base = "Win32GUI")]
    )