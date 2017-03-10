TARGET=main

all: $(TARGET)

$(TARGET):
	time python3 sudoku.py -i grids/grid1 -s 1

clean:
