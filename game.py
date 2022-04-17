from node import Node
import rules
import random


starting_pos = ["x", 1, "*", 2, 3]

saved_tree = None


def generate_tree(start_pos):
    global saved_tree
    if saved_tree is not None:
        if saved_tree[0][0].get_game_pos() == start_pos:
            print("Tree already saved")
            return saved_tree
        else:
            saved_tree = None

    game_tree = {}

    level = 0
    player = 0  # player 0 or 1

    start_node = Node(level)
    start_node.set_game_pos(start_pos)

    game_tree[level] = [start_node]

    checked_nodes = []
    checked_moves = {}
    node_ids = {}

    source_node = start_node

    while True:
        if source_node.level + 1 not in game_tree:
            game_tree[source_node.level + 1] = []

        game_pos = source_node.get_game_pos()

        possible_moves = rules.get_legal_moves(game_pos)

        for move in possible_moves:
            pos = move[0]
            action = move[1]

            result_pos, p1_point_mod, p2_point_mod = rules.rule(game_pos, pos, action)

            points = source_node.get_points()
            points[player] += p1_point_mod

            if player == 1:
                other_player = 0
            else:
                other_player = 1
            points[other_player] += p2_point_mod

            node = Node(source_node.level + 1)
            node.set_game_pos(result_pos)
            node.set_points(points)
            node.generate_id()

            if (source_node.level + 1) not in node_ids:
                node_ids[source_node.level + 1] = {}

            if node.id in node_ids[source_node.level + 1]:
                node = node_ids[source_node.level + 1][node.id]
            else:
                node_ids[source_node.level + 1][node.id] = node
                game_tree[source_node.level + 1].append(node)

            if node not in source_node.children:
                source_node.add_children(node)

            if node not in checked_moves:
                checked_moves[node] = []
            checked_moves[node].append(move)

        checked_nodes.append(source_node)

        # get a new source node
        level_done = True
        for node in game_tree[source_node.level]:
            if node not in checked_nodes:
                source_node = node
                level_done = False
                break

        if level_done:
            try:
                source_node = game_tree[source_node.level + 1][0]
                player = switch_players(player)
            except IndexError:
                game_tree.pop(source_node.level + 1)
                break

    print(f"Generated {len(checked_nodes)} nodes.")

    saved_tree = game_tree
    return game_tree


def match_node(game_tree, game_pos, points, level):
    for node in game_tree[level]:
        if node.get_game_pos() != game_pos:
            continue
        if node.get_points() != points:
            continue
        if node.level != level:
            continue
        return node


def switch_players(player):
    if player == 1:
        new_player = 0
    else:
        new_player = 1
    return new_player


def print_tree(game_tree):
    for level, nodes in game_tree.items():
        print(f"\n\n ======> Level: {level} ({len(nodes)}) <======\n")
        for node in nodes:
            print(" ")
            node.print()


def analyze_tree(game_tree):
    p1_wins = 0
    p2_wins = 0
    draws = 0

    for level, nodes in game_tree.items():
        for node in nodes:
            if node.children:
                continue
            if node.value == 1:
                p1_wins += 1
            elif node.value == -1:
                p2_wins += 1
            else:
                draws = 0

    return p1_wins, p2_wins, draws


def randomize_starting_pos(count):
    new_game_pos = []
    action_list = [action for action in rules.values]

    used_values = {}
    for action, values in rules.values.items():
        for value in values:
            used_values[value] = 0

    for i in range(0, count):
        while True:
            action = random.choice(action_list)
            value = random.choice(list(rules.values[action]))

            limit = rules.values[action][value]["randomizer_limit"]
            if limit is None:
                limit = 99999

            if used_values[value] < limit:
                new_game_pos.append(value)
                used_values[value] += 1
                break

    global starting_pos
    starting_pos.clear()
    starting_pos.extend(new_game_pos)


if __name__ == "__main__":

    tree = generate_tree(starting_pos)
    print_tree(tree)

    # tree = generate_game_tree(starting_pos)
    # minmax(tree)

    # find_playable_game()
