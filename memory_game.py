
import logging
import os
import random

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def main():
    memory_game()


def memory_game():
    board_row, board_column = getBoardDimensions()
    player_one, player_two = getPlayers()
    logger.debug(f"Row Column : {board_row} {board_column}")
    logger.debug(f"Players: {player_one} {player_two}")
    empty_board = generate_empty_board(board_row, board_column, [])
    shuffled_cell_values = get_shuffled_cell_values(board_row, board_column)
    game_board = generate_game_board(
        board_row,
        board_column,
        board_column,
        empty_board,
        shuffled_cell_values
    )
    print(game_board)



def getPlayers():
    player_one = input(f"Enter the name of player one: ")
    player_two = input(f"Enter the name of player two: ")
    if player_two != player_one:
        return player_one, player_two
    else:
        print("Invalid inputs, player names cannot be the same, try again!")
        return getPlayers()


def getBoardDimensions():
    print("What are the dimensions of the board?")
    dimension_str = input("Enter two even integers from 2 to 10 separated by a "
                          "space (row/column, e.g. 4 10): ")
    dimensions = dimension_str.split()
    if len(dimensions) == 2:
        is_int = list(map(lambda x: 
                        x.isdigit and 
                        int(x) > 0 and 
                        int(x) <= 10 and
                        int(x) % 2 == 0,
                      dimensions))
        if all(is_int):
            row, column = dimensions
            return int(row), int(column)
        else:
            logger.debug(is_int)
            print('Invalid inputs, try again!')
            return getBoardDimensions()       
    else:
        logger.debug(dimensions)
        print('Invalid inputs, try again!')
        return getBoardDimensions()


def printBoard(row, column, board):
    pass


def generate_empty_line(columns: int, line: list):
    if columns > 0:
        return generate_empty_line(columns - 1, line + [''])
    elif columns == 0:
        return line


def generate_empty_board(rows: int, columns: int, board: list):
    if rows > 0:
        return generate_empty_board(
            rows - 1,
            columns,
            board + [generate_empty_line(columns, [])]
        )
    elif rows == 0:
        return board


def update_line(line: list, column: int, value: str):
    # column starts from 1, i.e. index + 1
    first_half = line[:column - 1]
    second_half = line[column:len(line)]
    return first_half + [value] + second_half


def update_board(board: list, row: int, column: int, value: str):
    # row and column starts from 1
    first_half = board[:row - 1]
    second_half = board[row:len(board)]
    updated_row = update_line(board[row - 1], column, value)
    return first_half + [updated_row] + second_half


def get_shuffled_cell_values(rows, columns):
    cell_vals = [x + 1 for x in range(int(rows * columns / 2))]
    cell_vals = cell_vals + cell_vals
    return sorted(cell_vals, key=lambda k: random.random())


def generate_game_board(rows, columns, total_columns, board, cell_vals):
    if rows == 0:
        return board
    elif rows > 0 and columns > 0:
        return generate_game_board(
            rows,
            columns - 1,
            total_columns,
            update_board(board, rows, columns, cell_vals[-1]),
            cell_vals[:-1])
    elif rows > 0 and columns == 0:
        columns = total_columns
        return generate_game_board(
            rows - 1,
            columns,
            total_columns,
            board,
            cell_vals)


if __name__ == "__main__":
    main()