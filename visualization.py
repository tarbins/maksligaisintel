try:
    from PIL import Image, ImageDraw, ImageFont
    pil_installed = True
except ModuleNotFoundError:
    print("PIL not installed.")
    pil_installed = False

import game
import minmax


vertical_spacing = 100
font20 = ImageFont.truetype("arial.ttf", 20)


def draw_rectangle(draw_src, x1, y1, x2, y2):
    draw_src.line((x1, y1, x1, y2), fill="black")
    draw_src.line((x1, y2, x2, y2), fill="black")
    draw_src.line((x2, y2, x2, y1), fill="black")
    draw_src.line((x2, y1, x1, y1), fill="black")


class GraphicNode:
    def __init__(self, node, positions, x: int, y: int):
        self.node = node
        self.positions = positions
        self.x = x
        self.y = y

        self.draw_src = None

        self.rectangles_pos = {
            "player1_points": tuple(),
            "player2_points": tuple(),
            "game_pos": tuple(),
            "value": tuple(),
        }

        self.text_pos = {
            "player1_points": tuple(),
            "player2_points": tuple(),
            "game_pos": tuple(),
            "value": tuple(),
        }

        self.digit_pos = {}  # by position in array

        self.game_pos = self.node.get_game_pos()
        self.node_id = str(node.id)

        if not self.game_pos:
            self.game_pos = ["-"]

        self.positions[self.node_id] = self

        self.height = 25
        self.width, self.center_x = self.calculate_positions()

        self.lower_center = (x+(self.width/2), y)
        self.upper_center = (x+(self.width/2), y + self.height)

    def calculate_positions(self):
        x = self.x
        y = self.y

        text_spacing = 20
        text_offset = int(text_spacing / 3)

        height = self.height

        self.rectangles_pos["player1_points"] = (x, y, x + height, y + height)
        self.text_pos["player1_points"] = (x + text_offset, y)
        cx = x + height  # cursor x

        text_x = cx + text_offset
        for mult, digit in enumerate(self.game_pos):
            self.digit_pos[mult] = (text_x, y)
            text_x += text_spacing + text_offset

        digit_pos_keys = list(self.digit_pos)
        dp_width = (self.digit_pos[digit_pos_keys[-1]][0] - self.digit_pos[digit_pos_keys[0]][0]) + text_spacing

        if len(self.game_pos) < 2:
            dp_width = text_spacing * 2
            self.digit_pos[0] = (cx + int(dp_width-text_spacing-text_offset), y)

        self.rectangles_pos["game_pos"] = (cx, y, cx + dp_width, y + height)
        self.text_pos["game_pos"] = (cx + text_offset, y)
        cx += dp_width

        self.rectangles_pos["player2_points"] = (cx, y, cx + height, y + height)
        self.text_pos["player2_points"] = (cx + text_offset, y)
        cx += height + 5

        self.rectangles_pos["value"] = (cx, y, cx + height, y + height)
        self.text_pos["value"] = (cx + text_offset, y)

        width = (cx + height) - x
        center_x = int((cx + height) - (width/2))

        return width, center_x

    def draw(self):
        for name, coords in self.rectangles_pos.items():
            draw_rectangle(self.draw_src, *coords)

        points = self.node.get_points()

        self.draw_src.text(self.text_pos["player1_points"], text=str(points[0]), fill="black", font=font20)
        self.draw_src.text(self.text_pos["player2_points"], text=str(points[1]), fill="black", font=font20)
        self.draw_src.text(self.text_pos["value"], text=str(self.node.value), fill="blue", font=font20)

        for pos, digit in enumerate(self.game_pos):
            self.draw_src.text(self.digit_pos[pos], text=str(digit), fill="red", font=font20)


def calculate_image_size(tree, positions):
    global vertical_spacing

    x = 75
    y = 50
    spacing = 50

    gnodes = []

    width = x
    height = y

    edge_x = width
    edge_y = height

    total_gen = 0
    for level, nodes in tree.items():
        total_gen += len(nodes)

    vertical_spacing += (total_gen % 100)*10

    for level, nodes in tree.items():
        node_x = x
        for mult, node in enumerate(nodes):

            gnode = GraphicNode(node, positions, node_x, y)
            node_x += gnode.width + spacing

            edge_x = gnode.x + gnode.width
            if edge_x > width:
                width = edge_x

            edge_y = gnode.y + gnode.height
            if edge_y > height:
                height = edge_y

            gnodes.append(gnode)

        y += vertical_spacing
        edge_y += vertical_spacing

    return width, height, gnodes


def draw_levels(tree, draw_src, positions):
    x = 0
    y = 50

    levels = minmax.get_level_names(tree)

    for level, nodes in tree.items():
        draw_src.text((x, y), text=f"[{level}] {levels[level]}", font=font20, fill="blue")
        for node in nodes:
            for child in node.children:
                node_id = str(node.id)
                child_id = str(child.id)

                breathing_room = 1
                from_x = positions[node_id].upper_center[0] + breathing_room
                from_y = positions[node_id].upper_center[1] + breathing_room
                to_x = positions[child_id].lower_center[0] - breathing_room
                to_y = positions[child_id].lower_center[1] - breathing_room

                if child.value == 1 and node.value == 1:
                    fill = "red"
                else:
                    fill = "black"

                draw_src.line((from_x, from_y, to_x, to_y), fill=fill, width=3)

        y += vertical_spacing


def visualize(game_tree=None):
    if not pil_installed:
        print("Lai izmantotu vizualizēšanas funkciju, nepieciešams instalēt PIL.")
        return

    if game_tree is None:
        game_tree = game.generate_tree(game.starting_pos)
        minmax.generate(game_tree)
    else:
        if game_tree[0][0].value is None:
            print("game_tree available, but isn't yet evaluated")
            game_tree = game.generate_tree(game.starting_pos)
            minmax.generate(game_tree)

    print("Visualizing")
    positions = {}

    w, h, gnodes = calculate_image_size(game_tree, positions)

    size = (w, h)

    im = Image.new('RGB', size, color="white")

    draw_src = ImageDraw.Draw(im)
    draw_src.text((im.size[0] / 2, 10), text="Spēles koks", font=font20, fill="black")

    for gnode in gnodes:
        gnode.draw_src = draw_src
        gnode.draw()

    draw_levels(game_tree, draw_src, positions)
    print("Pabeigts. aizvērt bildi, lai turpinātu darbu")
    im.show()
    # im.save("D:/Files/Python Projects/AI_Pirmais_praktiskais/image.png", "PNG")


if __name__ == "__main__":
    visualize()
