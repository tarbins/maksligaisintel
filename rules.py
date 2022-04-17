ADD = "pieskaitīt"
CONVERT = "pārvērst"
THIEF = "zagt"
LEECH = "uzņemt"


values = {
    ADD: {
        2: {"randomizer_limit": 1},
        3: {"randomizer_limit": None},
        1: {"randomizer_limit": None}
    },
    CONVERT: {
        2: {"p1_mod": 0, "p2_mod": 0, "spawn": ["*"], "randomizer_limit": 1},
    },
    THIEF: {
        "x": {"p1_mod": 0, "p2_mod": 0, "randomizer_limit": 1},
    },
    LEECH: {
        "*": {"punishment": 2, "randomizer_limit": 1}
    },
}


def rule(input_pos, pos, action):
    game_pos = [i for i in input_pos]

    p2_point_mod = 0
    p1_point_mod = 0

    value = game_pos[pos]

    if action == ADD:
        p1_point_mod = game_pos.pop(pos)

    elif action == CONVERT:
        p1_point_mod = values[action][value]["p1_mod"]
        p2_point_mod = values[action][value]["p2_mod"]

        game_pos.pop(pos)

        for spawn_value in values[action][value]["spawn"]:
            game_pos.insert(pos, spawn_value)

    elif action == THIEF:
        bonus = 0
        try:
            game_pos[pos+1] -= 1
            bonus += 1
            if game_pos[pos+1] < 1:
                game_pos.pop(pos+1)
                bonus += 2
        except IndexError:
            pass
        except TypeError:
            pass

        game_pos.pop(pos)
        p1_point_mod = values[action][value]["p1_mod"] + bonus
        p2_point_mod = values[action][value]["p2_mod"]

    elif action == LEECH:
        value = game_pos[pos]

        result_val = 0

        try:
            # left side
            if pos-1 < 0:
                raise IndexError
            result_val += game_pos[pos-1]
        except IndexError:
            result_val -= values[action][value]["punishment"]
        except TypeError:
            pass

        try:
            # right side
            result_val += game_pos[pos+1]
            if result_val > 3:
                result_val = 3
        except IndexError:
            if not result_val:  # blakus jābūt vismaz vienai vērtībai, savādāk uzliks sodu
                result_val -= values[action][value]["punishment"]
        except TypeError:
            pass

        game_pos.pop(pos)
        p1_point_mod = result_val

    return game_pos, p1_point_mod, p2_point_mod


def get_legal_moves(game_pos):
    # strādā ar pozīcijām, nevis vērtībām.
    possible_moves = []

    for pos, i in enumerate(game_pos):
        moves = []

        for action, parameters in values.items():
            if i in parameters:
                moves.append((pos, action))

        for move in moves:
            possible_moves.append(move)

    return possible_moves


# verify(values)
