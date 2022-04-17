import game


def get_level_names(game_tree):
    levels = {}
    mname = "max"
    for level in game_tree:
        levels[level] = mname
        if mname == "max":
            mname = "min"
        else:
            mname = "max"
    return levels


def generate(game_tree):
    if game.saved_tree:
        if game_tree[0][0].id == game.saved_tree[0][0].id:
            if game.saved_tree[0][0].value is not None:
                print("Minmax already checked")
                return

    levels = get_level_names(game_tree)

    node_values = {}

    # piešķirt visām strupceļa virsotnēm sākuma vērtību

    for level, nodes in game_tree.items():
        for node in nodes:
            if node.children:
                continue
            else:
                if node.player1_points > node.player2_points:
                    val = 1
                elif node.player1_points < node.player2_points:
                    val = -1
                else:
                    val = 0

                node_values[node] = val
                node.value = val

    level = list(levels)[-1]
    while level >= 0:
        nodes = game_tree[level]

        for node in nodes:
            max_val = float("-inf")
            min_val = float("inf")

            for child in node.children:
                val = node_values[child]
                if val >= max_val:
                    max_val = val
                if val <= min_val:
                    min_val = val

                if levels[level] == "max":
                    assigned_val = max_val
                else:
                    assigned_val = min_val

                node.value = assigned_val
                node_values[node] = assigned_val

        level -= 1


if __name__ == "__main__":
    tree = game.generate_tree(game.starting_pos)
    generate(tree)
