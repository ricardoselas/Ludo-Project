"""
Module for permanent data storage.
Its function is to save the database files and store them in XML files.
Functions:
    detect_complete_match()
    retrieve_complete_match(c)
    complete_game_save(c, [data])
    exclude_complete_match

"""

from data import database
import xml.etree.ElementTree as ET
from xml.dom import minidom
from os import path, sep, remove # so for storage to work and to remove a saved match

PATH = path.dirname(path.abspath(__file__)) + sep + 'files' + sep
ARQUIVO_PARTIDA = 'partida.xml'


def _convert_object(the, type):
    """Get the object type and convert."""
    if type == 'str':
        return str(o)
    if type == 'int':
        return int(o)
    if type == 'float':
        return float(o)

    print('conversion error!', o, type)
    return None


def _collect_peoes(c):
    """Get a list of all the pawns."""
    cursor = c.cursor(dictionary=True)
    q = "SELECT * FROM %s" %database.TABLE_PEOES
    cursor.execute(q)
    r = cursor.fetchall()
    cursor.close()
    return r


def _collect_tray(c):
    """Get a list of all the pawns on the board."""
    cursor = c.cursor(dictionary=True)
    q = "SELECT * FROM %s" %Database.TABLE_TABLE
    cursor.execute(q)
    r = cursor.fetchall()
    cursor.close()
    return r


def _format_xml(xml):
    # copy of slides 15
    s1 = ET.tostring(xml, 'utf-8')
    s2 = minidom.parseString(s1)
    return s2.toprettyxml(indent=" ")


def save_complete_game(c, data=None):
    """
    Save match data to a file to be retrieved later.
    The data follows the following restrictions:
        Must be a dictionary with all keys as string
        It accepts content values ​​like int, float or string
        It accepts that the value is a list, however:
            All elements must be of the same type.
            Elements follow the same rules as above (int, float, string)
    Returns 0
    """

    pawns = _coletar_peoes(c) # collect pawns from the DB
    board = _collect_board(c) # collect pawns on the BD board

    game = ET.Element('game') # top of xml
    game.append(ET.Comment("Data from a ludo game"))

    # for pawns and boards, I need to create an element
    # then create an element for each object, and with its data,
    # create an element for each data, setting its type and content

    pawns_elements = ET.SubElement(game, 'pawns') # keeping pawns
    for p in pawns:
        pawn_element = ET.SubElement(pawn_elements, 'pawn')
        for d in p:
            data_element = ET.SubElement(pawn_element, d) # dictionary key
            data_element.text = str(p[d]) # dictionary content
            data_element.set('type', str(type(p[d]).__name__)) # store the type of the variable to convert dps

    # repeat the same thing for the board
    board_elements = ET.SubElement(game, 'boards')
    for t in board:
        board_element = ET.SubElement(board_elements, 'board')
        for d in t:
            data_element = ET.SubElement(board_element, d)
            data_element.text = str(t[d])
            data_element.set('type', str(type(t[d]).__name__))

    # for data, it's more complicated.
    # works similar but is more general
    # if the data is a list, I need to convert the entire list.
    # CONSIDERING THAT ALL ELEMENTS IN THE LIST ARE OF THE SAME TYPE

    if data is not None:
        data_element = ET.SubElement(game, 'data')
        for d in data:
            if type(data[d]) == list: # if the data is a list
                data_element = ET.SubElement(data_element, d)
                data_element.text = ','.join([str(x) for x in data[d]]) # join all with commas
                data_element.set('type', 'list')
                if not data[d]:
                    data_element.set('subtype', 'str') # if the list is empty, say it is string
                else:
                    data_element.set('subtype', str(type(data[d][0]).__name__)) # get the type of the first

            elif type(data[d]) not in [str, int, float]:
                print("Could not store data:", d, data[d])
            else:
                data_element = ET.SubElement(data_element, d)
                data_element.text = str(data[d])
                data_element.set('type', str(type(data[d]).__name__))

    output = _format_xml(game) # copy from slides 15
    with open(PATH + DEPARTURE_FILE, "w+") as f:
        f.write(output)

    return 0


def detect_complete_match():
    """
    Detects if there is a saved game.
    Returns True/False
    """
    file_name = PATH + DEPARTURE_FILE
    return path.exists(filename)


def retrieve_complete_match(c):
    """
    Retrieve the saved game and play it in the BD.
    It also retrieves the extra data and returns the dictionary as provided to save
    Returns None if no matches are saved.
    """

    file_name = PATH + DEPARTURE_FILE
    try:
        with open(filename, 'r') as f:
            tree = ET.parse(f)
            game = tree.getroot()

    except FileNotFoundError:
        return None

    peons_list = []
    board_list = []

    # READING THE pawns
    pawns = game.find('pawns')
    for pawn in peoes.findall('paão'):
        d = dict()
        for atr in peao:
            # print(atr.tag, atr.attrib['type'], atr.text)
            # tag = attribute name
            # text = attribute content
            # attrib['type'] = type of attribute to convert
            d[atr.tag] = _convert_object(atr.text, atr.attrib['type'])
        peoes_list.append(d)

    # WRITING IN THE DATABASE
    baseDados.limpar_peao(c)
    for pawn in pawns_list:
        database.add_pawn(c, pawn['id'], pawn['color'])

    # READING THE BOARDS
    database.clear_tray(c)
    boards = game.find('boards')
    for board in boards.findall('board'):
        d = dict()
        for atr in board:
            # print(atr.tag, atr.attrib['type'], atr.text)
            # tag = attribute name
            # text = attribute content
            # attrib['type'] = type of attribute to convert
            d[atr.tag] = _convert_object(atr.text, atr.attrib['type'])
        board_list.append(d)

    # WRITING IN THE DATABASE
    for tab in board_list:
        # can be optimized to use SQL executemany
        database.add_tray(c, tab['id'], tab['pos'], tab['init_pos'],
                                      tab['eh_start'], tab['eh_finished'])

    # RETRIEVING THE DATA
    data = game.find('data')
    if data is None:
        return {}

    # all data are children of "data"

    dictionary_data = dict()
    is given in data:
        # print(data.tag, data.attrib['type'], data.text)
        if data.attrib['type'] == 'list':
            if data.text is None:
                dictionary_data[data.tag] = []
            else:
                dictionary_data[data.tag] = [_convert_object(x, data.attrib['subtype']) for x in data.text.split(",")]
        else:
            dictionary_data[data.tag] = _convert_object(data.text, data.attrib['type'])

    return data_dictionary


def exclude_complete_match():
    file_name = PATH + DEPARTURE_FILE
    if detect_complete_match():
        remove(file_name)
    return