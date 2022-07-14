"""
Departure Module
    The mode is executed from a function, starts startup
    This function will perform all other built-in functions
    It will call the other game modules, database, and GUI
"""

from game import data
from game import pao
from game import board
from data import database
from data import dataStorage
import datetime
from display import GUIGame

peoes_color = dict()
db_connection = None # DB connection to be made
pawns_update_graphic = []


def _create_match(colors):
    """
    Create a match. Returns your data.
    """
    global db_connection
    if db_connection is None:
        db_connection = database.start_connection()
    pawn.clean_peoes(connection_bd)
    board.clear_board(db_connection)
    peoes_cor.clear()
    board.configure_board(len(colors))

    for color in colors:
        temp = []
        for i in range(4):
            temp.append(paao.criar_paao(connection_db, color))
        board.add_pawns(db_connection, temp)

    data = {'creation_time': datetime.datetime.now().isoformat(),
             'time': '0:0',
             'colors': colors,
             'players': len(colors),
             'winners': []}

    return data


def _load_start():
    """Load a game. Returns its data, or -1 if there was no previous game."""
    global db_connection
    if db_connection is None:
        db_connection = database.start_connection()
    pawn.clean_peoes(connection_bd)
    board.clear_board(db_connection)

    data = data storage.recovers_complete_match(db_connection)
    if data is None:
        return -1

    board.configure_board((dice['players']))

    return data


def _round(color):
    """
    Do the _round.
    3 if you can play again.
    2 if win,
    1 if you did nothing,
    0 if successful,
    raises error if error.
    """
    global bd_connection, pawns_update_graphic

    pawns_update_graphic.clear()
    play_again = False
    # running data
    GUIJogo.update_screen(chat=('Throw the dice', color), dice=0)
    GUIGame.data_wheel()
    dice_value = dice.play_dice()
    if data_value == 6:
        play_again = True
    print("I ran the data: %d" % data_value)
    GUIGame.update_screen(chat=('I rotated the dice: %d' % data_value, color), data=data_value)
    GUIGame.play_sound(1)

    # finding possible values
    # pawns_list = pawns_color[color]
    pawn_list = pawn.accessar_peo(db_connection, cor=color)

    list_possible_pawns = []
    finished_pawns = 0
    for p in pawns_list:
        x = board.possible_movement(db_connection, p, data_value)
        if x == -1:
            raise Exception("IdDoes Not Exist")
        if x == 0:
            list_possible_peoes.append(p)
        if x == 2:
            # the pawn is already finished
            finished_pawns += 1

    if pawns_finished == 4:
        return 2 # if the guy has already won, say he already won, just in case

    print("Possible moves: %d" % len(list_possible_pawns))
    # GUIGame.update_screen(lock_destaque=True, chat=("Possible moves: %d" % len(list_possible_pawns), color))
    if not list_possible_peoes:
        return 1 if not play_again else 3

    # choosing the pawn to move
    # i = choose_pawn(list_possible_pawns)
    print(list_possible_peopers)
    GUIGame.update_screen(connection_db, highlight=list_possible_peoes)
    i = GUIGame.choice_pawn(connection_db, list_possible_pawns)
    pawn_to_mover = list_possible pawns[i]
    print("Choosed pawn %d" %i)
    peoes_atualizar_grafico.append(peoes_pra_mover)

    # moving the pawn
    final_position = board.mover_pawn(connection_db, pawn_to_move, value_data)
    if final_position == -1:
        raise Exception("IdNotExist2")

    if final_position == -2:
        if peoes_finalizados >= 3: # there were already three and another one is finished now
            return 2
        GUIGame.update_screen(chat=("Pawn finished!", color))
        print("You made it to the end with your pawn!")
        return 3 # can play again

    print("Pawn moved to position %d" % final_position)
    GUIGame.update_screen(chat=("Pawn moved", color))

    # check pawn eaten
    pawn_list_position = board.access_position(db_connection, final_position)
    if list_peoes_posicao == 0: # protected house, don't eat
        return 0 if not play_again else 3

    for p in position_pawns_list:
        p_cor = pawn.access_pawn(db_connection, p)
        if cor_p == color: # if it's the same color, forget it
            continues
        else:
            print("Pain eaten: %d" %p)
            GameGUI.update_screen(chat=("Pawn captured!", color))
            board.restart_pawn(db_connection, p) # ate the pawn
            pawns_update_graphic.append(p)
            play_again = True

    if play_again:
        return 3
    return 0


def _run_start(data):
    """Play a game. Returns 0 to its end."""

    colors = data

    ['Colors']
    minutes, seconds = data['time'].split(':')
    initial_elapsed_time = int(minutes) * 60 + int(seconds)
    start_time = datetime.datetime.now()

    while colors:
        color = colors.pop(0)
        print("Turn for %s" % color)
        GameGUI.update_screen(db_connection, chat=("Turn %s" % color, color))
        x = _round(color)
        if x == 2:
            GUIGame.play_sound(3)
            print("You won!")
            GUIGame.update_screen(chat=("You won!", color))
            # continue # color does not return to color list
            dice['winners'].append(color) # save the winning color to the dice

        elif x == 3:
            GUIGame.update_screen(chat=("Play again", color))
            GUIGame.play_sound(2)
            colors.insert(0, color)
        else:
            if x == 1:
                GUIGame.update_screen(chat=("No moves", color))
                print("You cannot make any moves.")
            else:
                GUIGame.play_sound(0)
            GameGUI.update_screen(chat=("Round finished", color))
            colors.append(color)

        GameGUI.update_screen(c=db_connection, update=peons_update_graphic, chat=("", color)) # to skip a line

        elapsed_time = (datetime.datetime.now() - start_time).total_seconds() + start_elapsed_time
        data['time'] = "%d:%d" % (elapsed_time // 60, elapsed_time % 60)

        datastorage.savar_complete_match(db_connection, data)

        GameGUI.wait_time(500) # delay the next round a little

    # ended up here
    GameGUI.display_final_screen_and_close(data['winners'])
    datastorage.excludes_complete_match()

    return 0


def start_game(color_list):
    """
    Start a match.
    Receives the match colors and creates it.
    If it's an empty list, it recovers an old game.
        If no match, return False.
    And then rotate.
    """
    global db_connection
    db_connection = database.start_connection()

    print("Creating/Loading the game.")
    if len(color_list) == 0:
        if not datastorage.detects_complete_match():
            return False
        data = _load_start()
    else:
        data = _create_match(list_colors)

    print("Starting game created at %s, played for %s minutes" % (data['creation_time'], data['time']))
    GUIGame.initialize(db_connection)
    _run_start(data)
    database.close_connection(db_connection)
    print("Closing connection.")
    return