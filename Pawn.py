"""
Peao module

clean_parts()
create_pawn()
pawn_access()

Starting over (deleting classes)
pawn movement
Remaking pawn (pawn only contains color)
Updating pawn_access
"""

of data import baseData

# people = []
current_pea_id = 0


def clear_peoes(c):
     """Clears all saved pawns. Returns 0."""
     global current_pea_id
     # pawns.clear()
     baseDados.limpar_peao(c)
     current_pea_id = 0
     return 0


def create_pawn(c, color):
     """Creates a pawn. Returns its id."""
     global current_pea_id
     pawn = dict()

     pawn['id'] = current_pawn_id
     current_pea_id += 1
     pawn['color'] = color
     # pawns.append(peo)
     database.add_pawn(c, pawn['id'], pawn['color'])
     return pawn['id']


def pawn_access(c, pawn_id=None, color=None):
     """Access the pawn color.
     color
     empty string if there is no such id.
     """
     # for p in people:
     # if p['id'] == pawn_id:
     # return p['color']
     return database.select_pawn(c, pawn_id, color)