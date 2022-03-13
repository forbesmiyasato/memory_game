
import logging
import random
import time

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
    players = {player_one: 0, player_two: 0}
    play_game(game_board, player_one, players, fixed_cards)


def play_game(board, cur_player_name, players, fixed_cards):
    logger.debug(board)
    logger.debug(fixed_cards)
    print('\nName: Points')
    print_players_info(list(players.items()))
    print_board(board, fixed_cards)
    opponent_player_name = list(get_opponent_player(players, cur_player_name).keys())[0]
    if game_is_over(fixed_cards):
        player_one = cur_player_name
        player_two = opponent_player_name
        player_one_points = players[player_one]
        player_two_points = players[player_two]
        if player_one_points > player_two_points:
            print(f'Player {player_one} won with {player_one_points} matches!')
        elif player_one_points < player_two_points:
            print(f'Player {player_two} won with {player_two_points} matches!')
        else:
            print(f'Game tied at {player_one_points} matches!')
        return
    players, new_fixed_cards, matched = play_turn(board, fixed_cards, players, cur_player_name)
    if matched:
        play_game(board, cur_player_name, players, new_fixed_cards)
    else:
        play_game(board, opponent_player_name, players, new_fixed_cards)


def play_turn(board, fixed_cards, players, cur_player_name):
    print(f'player {cur_player_name}, flip two cards that are facing down.')
    card_one_row, card_one_column = select_card(board, fixed_cards)
    temp_fixed_cards_one = update_board(fixed_cards, card_one_row, card_one_column, True)
    print_board(board, temp_fixed_cards_one)
    card_two_row, card_two_column = select_card(board, temp_fixed_cards_one)
    temp_fixed_cards_two = update_board(temp_fixed_cards_one, card_two_row, card_two_column, True)
    print_board(board, temp_fixed_cards_two)

    card_one = board[card_one_row - 1][card_one_column - 1]
    card_two = board[card_two_row - 1][card_two_column - 1]
    if card_one == card_two:
        print('You got matching cards, it is your turn again!')
        cur_points = players[cur_player_name]
        new_players = update_player(players, cur_player_name, cur_points + 1)
        return new_players, temp_fixed_cards_two, True
        # return play_turn(board, new_fixed_cards, players, name)
    else:
        print('Your turn is over, no matches!')
        return players, fixed_cards, False


def update_player(players, player_name, points):
    return {player_name: points, **get_opponent_player(players, player_name)}


def get_opponent_player(players, player_name):
    return dict(filter(lambda x: x[0] != player_name, players.items()))


def select_card(board, fixed_cards):
    row, column = get_board_inputs(
        "Enter two integers (row/column) separated by a space: ",
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
    elif fixed_cards[row - 1][column - 1]:
        print('That card is already flipped, please pick another card!')
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


def get_board_inputs(input_prompt, valid_func, extra_prompt=None):
    if extra_prompt:
        print(extra_prompt)
    input_str = input(input_prompt)
    inputs = input_str.split()
    if len(inputs) == 2:
        is_valid = list(map(valid_func, inputs))
        if all(is_valid):
            row, column = inputs
            return int(row), int(column)
        else:
            print('Invalid inputs, try again!')
            return get_board_inputs(input_prompt, valid_func)       
    else:
        print('Invalid inputs, try again!')
        return get_board_inputs(input_prompt, valid_func)


def print_players_info(players):
    if not len(players):
        return
    player = players[0]
    print(f'{player[0]}: {player[1]}')
    print_players_info(players[1:])


def print_row(row, num_columns, fixed_row, row_num):
    if not len(row):
        return
    if len(row) == num_columns:
        print(f'{row_num:>2} |', end='')
    print(f'{row[0] if fixed_row[0] else "":>2}', end='|')
    print_row(row[1:], num_columns, fixed_row[1:], row_num)


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
    first_half = line[:column - 1]
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


def game_is_over(fixed_cards):
    for row in fixed_cards:
        if not all(row):
            return False
    return True


if __name__ == "__main__":
    main()