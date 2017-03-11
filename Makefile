TARGET=main

all: $(TARGET)

$(TARGET):
	time python3 sudoku.py <grids/grid1

clean:
