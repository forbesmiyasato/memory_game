
import logging
import os
import random

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def main():
    memory_game()


def memory_game():
    board_rows, board_columns = get_board_inputs(
        "Enter two even integers from 2 to 10 separated by a space "
        "(row/column, e.g. 4 10): ",
        lambda x: 
        x.isdigit and 
        int(x) > 0 and 
        int(x) <= 10 and
        int(x) % 2 == 0,
        "What are the dimensions of the board?"
    )
    player_one, player_two = get_players()
    logger.debug(f"Row Column : {board_rows} {board_columns}")
    logger.debug(f"Players: {player_one} {player_two}")
    empty_board = generate_empty_board(board_rows, board_columns, [])
    shuffled_card_values = get_shuffled_card_values(board_rows, board_columns)
    game_board = generate_game_board(
        board_rows,
        board_columns,
        board_columns,
        empty_board,
        shuffled_card_values
    )
    fixed_cards = empty_board
    logger.debug(game_board)
    players = {player_one: 0, player_two: 0}
    play_game(game_board, players, fixed_cards)


def play_game(board, players, fixed_cards):
    for name, points in players.items():
        print_player_info(name, points)
    print_board(board, fixed_cards)
    for name, points in players.items():
        players, new_fixed_cards = play_turn(board, fixed_cards, players, name)
    play_game(board, players, new_fixed_cards)


def play_turn(board, fixed_cards, players, name):
    print(f'player {name}, flip two cards that are facing down.')
    card_one_row, card_one_column = select_card(board, fixed_cards)
    temp_fixed_cards = update_board(fixed_cards, card_one_row, card_one_column, True)
    print_board(board, temp_fixed_cards)
    card_two_row, card_two_column = select_card(board, temp_fixed_cards)

    logger.debug(f'card one: {card_one_row}, {card_one_column}\n'
                 f'card two: {card_two_row}, {card_two_column}')
    card_one = board[card_one_row][card_one_column]
    card_two = board[card_two_row][card_two_column]
    if card_one == card_two:
        players[name]+=1
        new_fixed_cards = update_board(temp_fixed_cards, card_two_row, card_two_column, True)
    else:
        new_fixed_cards = fixed_cards
    return players, new_fixed_cards


def select_card(board, fixed_cards):
    row, column = get_board_inputs(
        "Enter two integers (column/row) separated by a space: ",
        lambda x:
        x.isdigit(),
        "Which card would you like to flip?"
    )
    if row > len(board) or row < 1:
        print('Invalid row, try again!')
        select_card(board, fixed_cards)
    elif column > len(board[0]) or column < 1:
        print('Invalid column, try again!')
        select_card(board, fixed_cards)
    elif fixed_cards[row][column]:
        print('That card is already matched, please pick another card!')
        select_card(board, fixed_cards)
    
    return row, column


def get_players():
    player_one = input(f"Enter the name of player one: ")
    player_two = input(f"Enter the name of player two: ")
    if player_two != player_one:
        return player_one, player_two
    else:
        print("Invalid inputs, player names cannot be the same, try again!")
        return get_players()


def get_board_inputs(input_prompt, valid_func, prompt_question=None):
    print(prompt_question)
    input_str = input(input_prompt)
    inputs = input_str.split()
    if len(inputs) == 2:
        is_valid = list(map(valid_func, inputs))
        if all(is_valid):
            row, column = inputs
            return int(row), int(column)
        else:
            logger.debug(is_valid)
            print('Invalid inputs, try again!')
            return get_board_inputs(input_prompt, valid_func)       
    else:
        logger.debug(inputs)
        print('Invalid inputs, try again!')
        return get_board_inputs(input_prompt, valid_func)


def print_player_info(name, points):
    print(f'{name}: {points}')


def print_row(row, num_columns, matched_row, row_num):
    if not len(row):
        return
    if len(row) == num_columns:
        print(f'{row_num:>2} |', end='')
    print(f'{row[0] if matched_row[0] else "":>2}', end='|')
    print_row(row[1:], num_columns, matched_row[1:], row_num)


def print_lines(column, num_columns):
    if not column:
        return
    elif column == num_columns:
        print(f'   |', end='')
    print('--|', end='')
    print_lines(column - 1, num_columns)


def print_column_nums(column, num_columns):
    if not column:
        return
    elif column == num_columns:
        print(f'    ', end='')
    print_column_nums(column - 1, num_columns)
    print(f'{column:>2} ', end='')


def print_board(board, fixed_cards):
    for index, row in enumerate(board):
        num_columns = len(row)
        if index == 0:
            print_column_nums(num_columns, num_columns)
            print()
            print_lines(num_columns, num_columns)
            print()
        print_row(row, num_columns, fixed_cards[index], index + 1)
        print()
        print_lines(num_columns, num_columns)
        print()


def generate_empty_line(columns: int, line: list):
    if columns > 0:
        return generate_empty_line(columns - 1, line + [None])
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
    first_half = line[:column]
    second_half = line[column:len(line)]
    return first_half + [value] + second_half


def update_board(board: list, row: int, column: int, value):
    # row and column starts from 1
    first_half = board[:row - 1]
    second_half = board[row:len(board)]
    updated_row = update_line(board[row - 1], column, value)
    return first_half + [updated_row] + second_half


def get_shuffled_card_values(rows, columns):
    card_vals = [x + 1 for x in range(int(rows * columns / 2))]
    card_vals = card_vals + card_vals
    return sorted(card_vals, key=lambda k: random.random())


def generate_game_board(rows, columns, total_columns, board, card_vals):
    if rows == 0:
        return board
    elif rows > 0 and columns > 0:
        return generate_game_board(
            rows,
            columns - 1,
            total_columns,
            update_board(board, rows, columns, card_vals[-1]),
            card_vals[:-1])
    elif rows > 0 and columns == 0:
        columns = total_columns
        return generate_game_board(
            rows - 1,
            columns,
            total_columns,
            board,
            card_vals)


if __name__ == "__main__":
    main()