"""
Board Module.
initials_position_list
safe_position_list
final_position_list
table_pawns:
    id <id> -> pawns id
    pos <int> -> current pawn position
    initial_pos <int> -> original pawn position
    eh_finished <bool> -> if it has gone to the end
    eh_inicio <bool> -> is at the origin

House numbering scheme:
    normal houses: 0 .. 13*n - 1

    # starting places: 100*i + j
    i (player): 1..n, j: 0..m

    final squares: 1000*n + j
    i (player): 1 .. n, j: 0 .. 5 (where 5 is the final square)

    safe houses: 13*i and 13*i + 8, i: 0 .. 3

"""

from data import database

N_CORES = 4 # setting the default number of players to 4
N_PEOES = 4 # setting the default number of pawns per player to 4
FINAL_HOUSE ID = 1000 # final houses start at a multiple of 1000
INITIAL_HOUSE_ID = 100 if N_CORES > 2 else 200 # initial houses start in a multiple of 100 or 200
initials_position_list = [[x * INITIAL_HOUSE_ID + y for y in range(N_PEOES)] for x in range(1, N_COLORS + 1)]
safe_position_list = [0, 8, 13, 21, 26, 34, 39, 47] # list of places where you can't eat
final_position_list = [FINAL_HOUSE_ID * n + 5 for n in range(1, N_COLOURS + 1)] # list of final board positions

added_colors = 0 # counter to add pawns. +1 for each color added.


def _find_pawn(c, id_paao):
    """
    Receives an id, returns its information, -1 if it doesn't exist.
    """
    # for i, p in enumerate(table_peoes):
    # if p['id'] == pawn_id:
    # return i

    returndatabase.select_tray(c, pawn=pawn_id)


def clear_board(c):
    # table_peoes.clear()
    database.clear_tray(c)
    return 0


def configure_tray(n=N_COLOURS):
    """Sets the board and prepares it. Returns 0"""
    global added_colors, N_COLORS
    added_colors = 0
    N_COLOR = n
    return 0


def add_peo(c, list_id, list_position=None):
    """
    Receives a pawn list and a list of current positions and saves it in the table.
    Returns 0 if successful,
    1 if repeated id,
    2 if list of positions is invalid,
    3 if all colors have already been added,
    """

    global colors_added
    # different list sizes
    if list_positions is not None and len(list_ids) != len(list_positions):
        return 2

    # already added all colors
    if added_colors == N_COLOURS:
        return 3

    # amount of a team different from defined amount of pawns
    if len(list_ids) != N_PEOES:
        return 2

    for i, id_peo in enumerate(list_ids):
        # for p in pawn_table:
        # if id_peao == p['id']:
        # return 1
        ifdatabase.select_tray(c, peon_id) != -1:
            return 1

        d = dict()
        d['id'] = id_peao
        d['init_pos'] = initial_position_list[added_colors][i]
        if list_positions is not None:
            d['pos'] = list_positions[i]
            d['eh_finished'] = list_positions[i] in list_position_finals
            d['eh_start'] = list_positions[i] in list_position_initials
        else:
            d['pos'] = d['initial_pos']
            d['eh_finished'] = False
            d['eh_start'] = True

        # table_peoes.append(d)
        baseData.add_tray(c, d['id'], d['pos'], d['init_pos'], d['eh_start'], d['eh_finished'])

    added_colors += 1

    return 0


def access_position(c, pos):
    """Returns a list of the ids at that position, 0 if the house is safe."""
    if pos in safe_position_list:
        return 0
    # get the id of x from the table if x is in position 'pos'
    # return [x['id'] for x in pawn_table if x['pos'] == pos]

    return [x['id'] for x in database.select_tray(c, pos=pos)]


def reset_pawn(c, id_pao):
    """
    Relocates the pawn to the starting position, resetting its dice.
    0 if successful,
    -1 if there is no such id.
    """
    # i = _find_pawn(id_paao)
    # if i == -1:
    # return -1

    p = database.select_tray(c, pawn=pawn_id)
    if p == -1:
        return -1

    # p = pawn_table[i]
    p['pos'] = p['initial_pos']
    p['eh_finished'] = False
    p['eh_start'] = True

    database.modify_tray(c, peon_id, p['pos'], p['start_pos'], p['eh_start'], p['eh_finished'])
    return 0


def possible_movement(c, pawn_id, mov):
    """
    Returns if it is possible to move the pawn.
    0 if possible,
    1 if impossible,
    2 if finished
    -1 if there is no such id.
    """
    # i = _find_pawn(id_paao)
    # if i == -1:
    # return -1
    # p = pawn_table[i]

    p = database.select_tray(c, pawn=pawn_id)
    if p == -1:
        return -1

    pos = p['pos']
    eh_start = p['eh_start']
    eh_finished = p['eh_finished']

    if eh_finalizado or (pos >= 1000 and pos % 1000 == 5): # if he has already finished the game
        # this position check again was placed
        # because an improper closing may end up not saving the state of the pawn. So it's a redundancy
        return 2

    if eh_inicio: # if it is still in the base
        return 0 if mov == 6 else 1 # if you didn't get a 6, you can't move

    if pos >= 1000: # if it is in the final squares
        x = 5 - (pos % 1000)
        return 1 if mov > x else 0 # if mov > when left, can't move

    # in any other case the pawn can be moved
    return 0


def move_pawn(c, pawn_id, mov):
    """
    Move the pawn. It is assumed that the movement has already been validated. Returns:
    position if the move was successful,
    -1 if the id does not exist,
    -2 if the pawn reached the last square.

    NOTE: it will never return to the position of the last house.
    """

    # i = _find_pawn(id_paao)
    # if i == -1:
    # return -1
    # p = pawn_table[i]

    p = database.select_tray(c, pawn=pawn_id)
    if p == -1:
        return -1

    pos = p['pos']
    initial_pos = p['initial_pos']
    time = initial_pos // 100 # says if the team ("color") is 1, 2, 3 or 4.

    if p['eh_inicio']: # it will put in the output box
        p['eh_start'] = False
        new_pos = 13*(time-1)
        p['pos'] = new_pos
        database.modify_tray(c, peon_id, p['pos'], p['start_pos'], p['eh_start'], p['eh_finished'])
        return new_pos

    if pos >= 1000: # final straight. Check if the pawn finished
        new_pos = pos + mov
        p['pos'] = new_pos
        if new_pos % 1000 == 5:
            p['eh_finished'] = True
            database.modify_tray(c, peon_id, p['pos'], p['start_pos'], p['eh_start'], p['eh_finished'])
            return -2

        database.modify_tray(c, peon_id, p['pos'], p['start_pos'], p['eh_start'], p['eh_finished'])
        return new_pos

    # first calculate the house to enter the home straight
    house_entry = (13*(time-1) + 50) % 52 # first house + 50, going around
    new_pos = (pos + mov) # first see without going around
    if pos <= home_entrance < new_pos: # it must enter the final stretch
        new_pos = (new_pos - house_entrance - 1) + time*1000
    else:
        new_pos = new_pos % 52 # otherwise, just correct the position

    p['pos'] = new_pos # save and return

    database.modify_tray(c, peon_id, p['pos'], p['start_pos'], p['eh_start'], p['eh_finished'])
    return new_pos

