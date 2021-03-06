# Run the memory game program with the python command using python 3.8.5.
# For example: "python3 memory_game.py", "python memory_game.py".
# Python 3.8.5 is the version I am using, so I am sure it should work.
# I'm pretty sure any python 3 version would work as well,
# but please use 3.8.5 if they don't.
# This program only uses standard packages, so you shouldn't need to pip
# install anything.

# I attempted to implement functional programming into this program by using
# no loops, no explicit state changes, functional methods such as map and
# filter, lambdas and higher order functions.

# Some clarifications to avoid confusion:
# A board is a 2D list with each element/cell indicating a card.
# For consistency, board rows and cells will be accessed using row and column
# as the index, e.g. board[row][column]. Rows and columns start from 1 as
# opposed to typical indices that start at 0. Hence, you might see a lot of
# row - 1 and column - 1, e.g. board[row - 1][column - 1] when retrieving a card.
# Sorry for choosing to start at 1 instead of 0. There were some top down
# recursions that confused me when starting from row - 1 and switching between
# index from 0 and index from 1 confused me even more.
import logging
import random

logging.basicConfig()
logger = logging.getLogger()
# set to DEBUG for testing to see the board content
logger.setLevel(logging.INFO)


def main():
    # Run the memory game
    memory_game()


def memory_game():
    # This function starts the memory game.
    # First, get the board dimensions from the user. Board dimensions have to be
    # integers that are even and between 1 and 10 inclusively.
    # Then, get the player names.
    # Next, generate the game board with (board cells / 2) matching cards that
    # are randomly placed.
    # Finally, have the players take turns flipping cards until all cards
    # are fixed (fixed cards are permanently flipped cards due to being matched
    # as opposed to flipped cards which could be temporarily flipped during
    # the player's turn).
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
    shuffled_card_values = get_shuffled_cards(board_rows, board_columns)
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
    # This function handles the game play. I.e. players taking turns to flip
    # cards until all cards are fixed. An updated board and player scores
    # are printed at the beginning of every turn. When all cards are fixed,
    # the game is considered over, and the player with more matches wins. If
    # both players have the same number of matches then it is a tie.
    # If there was a match during the turn, the player gets another turn until
    # they fail to get a match.
    # We can see the board when the logging level is set to DEBUG for testing.
    logger.debug(board)
    logger.debug(fixed_cards)
    print('\nName: Points')
    print_players_info(list(players.items()))
    print_board(board, fixed_cards)
    opponent_player_name = list(
        get_opponent_player(players, cur_player_name).keys()
    )[0]
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
    players, new_fixed_cards, matched = play_turn(
        board, fixed_cards, players, cur_player_name
    )
    if matched:
        play_game(board, cur_player_name, players, new_fixed_cards)
    else:
        play_game(board, opponent_player_name, players, new_fixed_cards)


def play_turn(board, fixed_cards, players, cur_player_name):
    # This function handles a player's turn.
    # It prompts the player to select two cards and checks to make sure
    # the two cards are valid.
    # Once the player selects two valid cards, it checks if it is match.
    # If it is a match, the player points are incremented, the matched
    # cards are marked as fixed, and the game is signaled to let the current
    # player have another turn. If it isn't a match, then the game state remains
    # the same and the current player's turn ends.
    print(f'player {cur_player_name}, flip two cards that are facing down.')
    card_one_row, card_one_column = select_card(board, fixed_cards)
    temp_fixed_cards_one = update_board(
        fixed_cards, card_one_row, card_one_column, True
    )
    print_board(board, temp_fixed_cards_one)
    card_two_row, card_two_column = select_card(board, temp_fixed_cards_one)
    temp_fixed_cards_two = update_board(
        temp_fixed_cards_one, card_two_row, card_two_column, True
    )
    print_board(board, temp_fixed_cards_two)

    card_one = board[card_one_row - 1][card_one_column - 1]
    card_two = board[card_two_row - 1][card_two_column - 1]
    if card_one == card_two:
        print('You got matching cards, it is your turn again!')
        cur_points = players[cur_player_name]
        new_players = update_player(players, cur_player_name, cur_points + 1)
        return new_players, temp_fixed_cards_two, True
    else:
        print('Your turn is over, no matches!')
        return players, fixed_cards, False


def update_player(players, player_name, points):
    # This function updates the current player's point by returning a new
    # players object
    return {player_name: points, **get_opponent_player(players, player_name)}


def get_opponent_player(players, player_name):
    # This function gets the opponent player key/value pair using the current
    # player's name.
    # The x in "lambda x" is a player name/point key value pair; filter
    # returns the player key value pair that matches the condition as a filter
    # object, so we have to convert the filter object back into a dict object
    return dict(filter(lambda x: x[0] != player_name, players.items()))


def select_card(board, fixed_cards):
    # This function gets a card on the board from user input.
    # The user is prompted to select a card until they select a valid card.
    # A valid card is two integers (row/column) separated by a space that are
    # not out of the board's boundaries and are not fixed/flipped.
    row, column = get_board_inputs(
        "Enter two integers (row/column) separated by a space: ",
        lambda x:
        x.isdigit(),
        "Which card would you like to flip?"
    )
    if row > len(board) or row < 1:
        print('Invalid row, try again!')
        return select_card(board, fixed_cards)
    elif column > len(board[0]) or column < 1:
        print('Invalid column, try again!')
        return select_card(board, fixed_cards)
    elif fixed_cards[row - 1][column - 1]:
        print('That card is already flipped, please pick another card!')
        return select_card(board, fixed_cards)

    return row, column


def get_players():
    # This function gets the two player names.
    # The two players are prompted to enter names again if their names are
    # the same.
    player_one = input("Enter the name of player one: ")
    player_two = input("Enter the name of player two: ")
    if player_two != player_one:
        return player_one, player_two
    else:
        print("Invalid inputs, player names cannot be the same, try again!")
        return get_players()


def get_board_inputs(input_prompt, valid_func, extra_prompt=None):
    # This function gets board inputs from the player.
    # Board inputs are always two integers (row/column), it could be the
    # dimensions or a certain card/cell, we pass in a function
    # that defines what is a valid integer input.
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
    # This function prints the players' name and points.
    if not len(players):
        return
    player = players[0]
    print(f'{player[0]}: {player[1]}')
    print_players_info(players[1:])


def print_row(row, num_columns, fixed_row, row_num):
    # This function prints a row of the board onto the screen.
    # It's iterating through the list recursively in a fashion more similar
    # to the haskell list recursion (I think). I believe the performance isn't
    # great since the python list is more like an array instead of a linked
    # list. Hence, you'll see more index recursing further below in the code.
    if not len(row):
        return
    if len(row) == num_columns:
        print(f'{row_num:>2} |', end='')
    print(f'{row[0] if fixed_row[0] else "":>2}', end='|')
    print_row(row[1:], num_columns, fixed_row[1:], row_num)


def print_lines(column, num_columns):
    # This function prints a line based on the column numbers purely to make
    # the printed board look nicer.
    if not column:
        return
    elif column == num_columns:
        print('   |', end='')
    print('--|', end='')
    print_lines(column - 1, num_columns)


def print_column_nums(column, num_columns):
    # This function prints a line of column numbers purely to make the printed
    # board look better and to help the players see column numbers easier.
    if not column:
        return
    elif column == num_columns:
        print('    ', end='')
    print_column_nums(column - 1, num_columns)
    print(f'{column:>2} ', end='')


def print_board(board, fixed_cards, index=0):
    # This function prints the board onto the screen.
    # It iterates through every row using recusion on index instead of a loop.
    # Index has a default of 0, so we can print the entire board by default
    # without adding a confusing third parameter of 0 or an additional wrapper
    # function. You will see more default index parameters for other functions
    # below, and it serves for the same purposes.
    if index == len(board):
        return
    row = board[index]
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
    print_board(board, fixed_cards, index + 1)


def generate_empty_row(columns, line):
    # This function generates an empty line with column number of elements.
    # An empty element is represented by a null/None value.
    if columns > 0:
        return generate_empty_row(columns - 1, line + [None])
    elif columns == 0:
        return line


def generate_empty_board(rows, columns, board):
    # This function generates an empty board.
    # An empty element is represented by a null/None value.
    if rows > 0:
        return generate_empty_board(
            rows - 1,
            columns,
            board + [generate_empty_row(columns, [])]
        )
    elif rows == 0:
        return board


def update_row(row, column, value):
    # This function updates the value of a row element at the given column by
    # returning a new updated row.
    # We construct the new row by putting the columns before
    # the column to update, the updated element at the given column, and the
    # columns after the column to update together. If the given column is
    # at the start or end of the row, then the elements before or after
    # respectively would be an empty list
    first_half = row[:column - 1]
    second_half = row[column:len(row)]
    return first_half + [value] + second_half


def update_board(board, row, column, value):
    # This function updates the value on the board at the given column and row
    # by returning a new board.
    # We construct the new board by putting the rows before the row to update,
    # the updated row, and the rows after the row to update together.
    # If the given row is at the start or end of the board, then the rows before
    # or after respectively would be an empty list
    first_half = board[:row - 1]
    second_half = board[row:len(board)]
    updated_row = update_row(board[row - 1], column, value)
    return first_half + [updated_row] + second_half


def get_shuffled_cards(rows, columns):
    # This function gets all the cards to be placed on the board in a
    # random order.
    def generate_card_values_list(cur_value, max_card_value, cur_list=[]):
        # This inner function generates a list of all possible card values
        if cur_value > max_card_value:
            return cur_list
        return generate_card_values_list(
            cur_value + 1,
            max_card_value,
            cur_list + [cur_value]
        )

    card_vals = generate_card_values_list(1, int(rows * columns / 2))
    card_vals = card_vals + card_vals
    return sorted(card_vals, key=lambda k: random.random())


def generate_game_board(rows, columns, total_columns, board, card_vals):
    # This function generates the game board. It takes in a list of cards
    # to be placed on the board, and then places them on the board one at a
    # time recursively.
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


def game_is_over(fixed_cards, index=0):
    # This function checks if the game is over recursively. The game is over if
    # all the cards on the board are fixed.
    if index == len(fixed_cards):
        return True
    if not all(fixed_cards[index]):
        return False
    return game_is_over(fixed_cards, index + 1)


if __name__ == "__main__":
    main()
