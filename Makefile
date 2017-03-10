TARGET=main

all: $(TARGET)

$(TARGET):
	python3 sudoku.py <grids/grid1

clean:
