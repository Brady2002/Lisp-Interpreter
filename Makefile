PYTHON = python3
SRC = Parser.py
TARGET = parse

all: $(TARGET)

$(TARGET): $(SRC)
    $(PYTHON) $(SRC) $(ARGS) > $@

clean:
    rm -f $(TARGET)

