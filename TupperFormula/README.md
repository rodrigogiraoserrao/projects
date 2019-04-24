# Tupper's self-referential formula

This project is accompanyed by [this blog post](https://mathspp.blogspot.com/2019/04/the-formula-that-plots-itself.html).

---

The file `num_generator.py` (frozen as a Windows executable in `TupperNumGenerator`) gives you an interface to draw in, that will then create the number that is needed for the Tupper formula. The numbers generated are dumped in the file `numbers.txt`.

After you got a number to draw, dump it in the `number2draw.txt` file and run the `draw_numbers.py` file from the same directory (frozen as a Windows executable in `TupperNumDrawer`).

Both pieces of code need pygame installed and run with Python 3.
