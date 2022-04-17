import tkinter as tk
import config as cfg
import game
import minmax
import rules
import visualization


class MainApplication:
    def __init__(self, parent):
        self.parent = parent

        self.parent.configure(bg=cfg.bgcolor)

        self.menu = Menu(self.parent, self.start_game)
        self.menu.load()

    def start_game(self, first_move):
        self.menu.unload()
        GameUI(self.parent, first_move, self.menu.setup.game_pos, self.menu)


class Menu:
    def __init__(self, parent, start_game_func):
        self.parent = parent
        self.widgets = []
        self.start_game_func = start_game_func

        self.setup_frame = tk.Frame(master=self.parent, bg=cfg.bgcolor)
        self.setup = None

        self.play_frame = tk.Frame(master=self.parent, bg=cfg.bgcolor)

        self.play_label = tk.Label(master=self.play_frame, text="Spēli uzsāk:", font=f"{cfg.font} 14", bg=cfg.bgcolor)

        self.start_player_button = tk.Button(master=self.play_frame, text="Cilvēks", font=f"{cfg.font} 14", bg=cfg.button_bgcolor, command=lambda: self.start_game("player"))

        self.start_computer_button = tk.Button(master=self.play_frame, text="Dators", font=f"{cfg.font} 14", bg=cfg.button_bgcolor, command=lambda: self.start_game("computer"))

    def start_game(self, first_move):
        self.start_game_func(first_move)

    def load(self):
        self.setup = SetupScreen(self.setup_frame, game.starting_pos)
        self.setup_frame.grid(row=0, column=0)
        self.widgets.append(self.setup_frame)

        self.play_frame.grid(row=1, column=0, padx=5, pady=10)
        self.widgets.append(self.play_frame)

        self.play_label.grid(row=0, column=0, columnspan=2)
        self.widgets.append(self.play_label)

        self.start_player_button.grid(row=1, column=0, padx=10, pady=5)
        self.widgets.append(self.start_player_button)

        self.start_computer_button.grid(row=1, column=1, padx=10, pady=5)
        self.widgets.append(self.start_computer_button)

    def unload(self):
        self.setup.unload()

        for widget in self.widgets:
            widget.grid_forget()


class PointCounter:
    def __init__(self, parent, row, col, text):
        self.parent = parent

        self.canvas, self.text, self.box = self.draw(row, col, text)
        self.points = 0

    def draw(self, row, col, text):
        canvas = tk.Canvas(master=self.parent, width=80, height=100, bg=cfg.bgcolor, highlightthickness=0)
        canvas.grid(row=row, column=col)

        text = canvas.create_text(45, 20, text=text, font=f"{cfg.font} 15")

        box = DigitBox(canvas, 15, 39, "0", size=60, width=2, fontsize=20, outline=cfg.pointbox_outline_col)

        return canvas, text, box

    def update_points(self, point_modifier):
        self.points += point_modifier
        self.canvas.itemconfigure(self.box.text, text=self.points)

    def set_points(self, points):
        self.points = points
        self.canvas.itemconfigure(self.box.text, text=self.points)

    def unload(self):
        self.canvas.grid_forget()


class Options:
    def __init__(self, parent, action_processor_func):
        self.parent = parent
        self.action_processor_func = action_processor_func

        self.buttons = {}
        for action in rules.values:
            self.buttons[action] = tk.Button(master=self.parent, width=7, font=f"{cfg.font} 12", bg=cfg.button_bgcolor, text=action)

        self.buttons[rules.ADD]["command"] = lambda: self.process(rules.ADD)
        self.buttons[rules.CONVERT]["command"] = lambda: self.process(rules.CONVERT)
        self.buttons[rules.THIEF]["command"] = lambda: self.process(rules.THIEF)
        self.buttons[rules.LEECH]["command"] = lambda: self.process(rules.LEECH)

        # self.add_button = tk.Button(master=self.parent, width=7, font=f"{cfg.font} 12", bg=cfg.button_bgcolor, text="Add", command=lambda: self.process(rules.ADD))
        # self.divide_button = tk.Button(master=self.parent, width=7,  font=f"{cfg.font} 12", bg=cfg.button_bgcolor, text="Divide", command=lambda: self.process(rules.DIVIDE))
        # self.magic_button = tk.Button(master=self.parent, width=7, font=f"{cfg.font} 12", bg=cfg.button_bgcolor, text="Magic", command=lambda: self.process(rules.THIEF))

    def process(self, action):
        self.action_processor_func(action)
        self.hide()

    def show(self, selected_value):
        col = 0
        for action, values in rules.values.items():
            if selected_value in values:
                self.buttons[action].grid(row=0, column=col, padx=5, pady=5)
                col += 1
        # if selected_value in rules.values[rules.ADD]:
        #     self.add_button.grid(row=0, column=0, padx=5, pady=5)
        #
        # if selected_value in rules.values[rules.DIVIDE]:
        #     self.divide_button.grid(row=0, column=1, padx=5, pady=5)
        #
        # if selected_value in rules.values[rules.THIEF]:
        #     self.magic_button.grid(row=0, column=2, padx=5, pady=5)

    def hide(self):
        for action, button in self.buttons.items():
            button.grid_forget()
        # self.add_button.grid_forget()
        # self.divide_button.grid_forget()
        # self.magic_button.grid_forget()


class EndScreen:
    def __init__(self, parent, play_again_func, menu_func):
        self.parent = parent
        self.play_again_func = play_again_func
        self.menu_func = menu_func

        self.playagain_button = tk.Button(master=self.parent, width=12, font=f"{cfg.font} 12", bg=cfg.button_bgcolor, text="Spēlēt vēlreiz", command=self.first_move_choice)
        self.menu_button = tk.Button(master=self.parent, width=8, font=f"{cfg.font} 12", bg=cfg.button_bgcolor, text="Izvēlne", command=self.menu)

        # choices
        self.start_player_button = tk.Button(master=self.parent, text="Cilvēks", font=f"{cfg.font} 12", bg=cfg.button_bgcolor, command=lambda: self.play_again("player"))
        self.start_computer_button = tk.Button(master=self.parent, text="Dators", font=f"{cfg.font} 12", bg=cfg.button_bgcolor, command=lambda: self.play_again("computer"))

    def play_again(self, first_move):
        self.start_player_button.grid_forget()
        self.start_computer_button.grid_forget()

        self.play_again_func(first_move)

    def first_move_choice(self):
        self.hide()
        self.start_player_button.grid(row=0, column=0, padx=5, pady=5)
        self.start_computer_button.grid(row=0, column=1, padx=5, pady=5)

    def menu(self):
        self.menu_func()

    def show(self):
        self.playagain_button.grid(row=0, column=0, padx=5, pady=5)
        self.menu_button.grid(row=0, column=1, padx=5, pady=5)

    def hide(self):
        self.playagain_button.grid_forget()
        self.menu_button.grid_forget()


class GameUI:
    def __init__(self, parent, first_move, game_pos, menu):
        self.parent = parent
        self.current_turn = first_move
        self.first_move = first_move
        self.game_pos = [i for i in game_pos]
        self.menu = menu

        self.level = 0
        self.game_tree = game.generate_tree(game_pos)
        minmax.generate(self.game_tree)
        # self.alphabeta = alphabeta.AlphaBeta(self.game_tree)
        # self.alphabeta.run()

        self.game_frame = tk.Frame(self.parent, bg=cfg.bgcolor)
        self.game_frame.grid(row=0, column=0)

        self.digit_frame = DigitFrame(self.game_frame, game_pos, row=0, col=1, selection_callback=self.process_click)

        self.turn_label = tk.Label(master=self.parent, text="...", font=f"{cfg.font} 12", bg=cfg.bgcolor)
        self.turn_label.grid(row=1, column=0, columnspan=2)

        self.options_frame = tk.Frame(master=self.parent, bg=cfg.bgcolor)
        self.options_frame.grid(row=2, column=0)
        self.options = Options(self.options_frame, self.process_option)

        self.endscreen_frame = tk.Frame(master=self.parent, bg=cfg.bgcolor)
        self.endscreen_frame.grid(row=3, column=0)
        self.endscreen = EndScreen(self.endscreen_frame, self.play_again, self.load_menu)

        self.points = {
            "player": PointCounter(self.game_frame, row=0, col=0, text="Tavs"),
            "computer": PointCounter(self.game_frame, row=0, col=2, text="Datora")
        }

        self.selection: list = []

        self.click_locked = False
        self.running = True

        self.next_turn()

    def load_menu(self):
        self.unload()
        self.menu.load()

    def unload(self):
        self.game_frame.grid_forget()
        self.turn_label.grid_forget()
        self.endscreen_frame.grid_forget()
        self.options_frame.grid_forget()

        for name, point_counter in self.points.items():
            point_counter.unload()

        self.digit_frame.unload()

    def next_turn(self):
        if not self.running:
            self.endscreen.show()
            return

        if self.current_turn == "player":
            self.turn_label["text"] = "Tava kārta!"
        elif self.current_turn == "computer":
            self.turn_label["text"] = "Datora kārta."
            self.parent.after(250, self.computer_move)

    def play_again(self, first_move):
        self.first_move = first_move
        self.current_turn = first_move
        self.level = 0
        self.selection = []

        for player, point_counter in self.points.items():
            point_counter.set_points(0)

        self.game_pos = [i for i in self.game_tree[0][0].get_game_pos()]
        self.digit_frame.update(self.game_pos)
        self.running = True

        self.next_turn()

    def process_click(self, selected):
        if self.click_locked:
            return

        # if clicked box is empty
        if len(self.game_pos)-1 < selected[0]:
            return

        if self.selection:
            if self.selection == selected:
                # hide
                self.digit_frame.canvas.itemconfigure(selected[1], outline=cfg.outline_col)
                self.options.hide()
                self.selection.clear()
                return
            else:
                self.options.hide()
                self.digit_frame.canvas.itemconfigure(self.selection[1], outline=cfg.outline_col)

        selected_value = self.game_pos[selected[0]]
        self.options.show(selected_value)
        self.process_selection(selected)

    def process_selection(self, selected):
        pos = selected[0]
        box_id = selected[1]

        self.digit_frame.canvas.itemconfigure(box_id, outline=cfg.selected_col)
        self.parent.update()
        self.selection = selected

    def process_game(self, action):
        if not self.running:
            return

        pos = self.selection[0]
        res_pos, p1_point_mod, p2_point_mod = rules.rule(self.game_pos, pos, action)
        self.level += 1

        self.points[self.current_turn].update_points(p1_point_mod)
        if self.current_turn == "player":
            other_player = "computer"
        else:
            other_player = "player"
        self.points[other_player].update_points(p2_point_mod)

        self.game_pos.clear()
        self.game_pos.extend(res_pos)

        self.current_turn = other_player

        self.parent.after(250, self.update_screen)

    def update_screen(self):
        self.digit_frame.canvas.itemconfigure(self.selection[1], outline=cfg.outline_col)
        self.selection.clear()

        self.digit_frame.update(self.game_pos)

        if len(self.game_pos) < 1:
            if self.points["player"].points > self.points["computer"].points:
                self.turn_label["text"] = "Tu uzvarēji!"
            elif self.points["player"].points < self.points["computer"].points:
                self.turn_label["text"] = "Uzvarēja dators. Tu zaudēji!"
            else:
                self.turn_label["text"] = "Neizšķirts!"

            self.running = False

        self.next_turn()

    def process_option(self, action):
        self.process_game(action)

    def computer_move(self):
        moves = rules.get_legal_moves(self.game_pos)

        if self.first_move == "player":
            secpl = "computer"
        else:
            secpl = "player"

        points = [self.points[self.first_move].points, self.points[secpl].points]
        current_node = game.match_node(self.game_tree, self.game_pos, points, self.level)

        if self.first_move == "player":
            modifier = 1
            lookfor = -1
        else:
            modifier = -1
            lookfor = 1

        goal_node = None
        while goal_node is None:
            for child in current_node.children:
                if child.value == lookfor:
                    goal_node = child
                    break
            lookfor += modifier

        for move in moves:
            pos = move[0]
            action = move[1]
            res_pos, p1_point_mod, p2_point_mod = rules.rule(self.game_pos, pos, action)

            player1_points = self.points[self.first_move].points
            player2_points = self.points[secpl].points

            if self.first_move == "computer":
                player1_points += p1_point_mod
                player2_points += p2_point_mod
            else:
                player2_points += p1_point_mod
                player1_points += p2_point_mod

            points = [player1_points, player2_points]
            match = game.match_node(self.game_tree, res_pos, points, self.level+1)

            if goal_node.compare(match):
                break

        selected_moveset = move

        pos = selected_moveset[0]
        action = selected_moveset[1]
        box_id = self.digit_frame.digit_boxes[pos].box

        selection = [pos, box_id]

        self.parent.after(200, self.process_selection(selection))
        self.parent.after(400, self.process_game(action))


class Analyze:
    def __init__(self, parent):
        self.parent = parent

        self.visualize_button = tk.Button(master=self.parent, width=9, height=1, text="Vizualizēt", font=f"{cfg.font} 10", bg=cfg.button_bgcolor, command=self.visualize)
        self.visualize_button.grid(row=0, column=0, padx=5)

        self.analyze_button = tk.Button(master=self.parent, width=9, height=1, text="Statistika", font=f"{cfg.font} 10", bg=cfg.button_bgcolor, command=self.analyze_tree)
        self.analyze_button.grid(row=0, column=1, padx=10)

        self.analysis_label = tk.Label(master=self.parent, text="", font=f"{cfg.font} 14", bg=cfg.bgcolor)

    def analyze_tree(self):
        self.analyze_button["text"] = "Apstrādā..."
        self.analyze_button["bg"] = cfg.selected_col
        self.analyze_button["state"] = tk.DISABLED
        self.parent.update()

        game_tree = game.generate_tree(game.starting_pos)
        minmax.generate(game_tree)
        analysis = game.analyze_tree(game_tree)

        if game_tree[0][0].value == 1:
            win_str = "Max uzvar"
        elif game_tree[0][0].value == -1:
            win_str = "Min uzvar"
        else:
            win_str = "Neizšķirts"

        self.analysis_label["text"] = f"P1: {analysis[0]} | P2: {analysis[1]} | Draw: {analysis[2]} | {win_str}"
        self.analysis_label.grid(row=0, column=2)

        self.analyze_button["text"] = "Statistika"
        self.analyze_button["bg"] = cfg.button_bgcolor
        self.analyze_button["state"] = tk.NORMAL

    def visualize(self):
        self.visualize_button["text"] = "Apstrādā..."
        self.visualize_button["bg"] = cfg.selected_col
        self.visualize_button["state"] = tk.DISABLED
        self.parent.update()

        visualization.visualize()

        self.visualize_button["text"] = "Vizualizēt"
        self.visualize_button["bg"] = cfg.button_bgcolor
        self.visualize_button["state"] = tk.NORMAL
        self.parent.update()

    def unload(self):
        self.analyze_button.grid_forget()
        self.analysis_label.grid_forget()


class SetupScreen:
    def __init__(self, parent, game_pos=None):
        self.parent = parent

        if not game_pos:
            game_pos = []
        self.game_pos = game_pos

        self.widgets = []

        self.label = tk.Label(master=self.parent, text="Izstrādāja: 201RDB194", font=f"{cfg.font} 12", bg=cfg.bgcolor)
        self.label.grid(row=0, column=0, columnspan=1)
        self.widgets.append(self.label)

        self.digit_frame = DigitFrameEditable(self.parent, game_pos, row=1, col=0)

        self.analysis_frame = tk.Frame(master=self.parent, bg=cfg.bgcolor)
        self.analysis_frame.grid(row=2, column=0)
        self.analyze = Analyze(self.analysis_frame)
        self.widgets.append(self.analysis_frame)

        self.rule_frame = tk.Frame(master=self.parent, bg=cfg.bgcolor)
        self.rule_frame.grid(row=3, column=0, pady=15)
        self.widgets.append(self.rule_frame)

        self.rule_labels = self.load_rules()

    def load_rules(self):
        header_text = "Skaitļu spēles noteikumi\n"
        rule_text = [
            "Spēlētāji gājienus (darbības ar vērtībām) izpilda secīgi.",
            "Spēle beidzās, kad uz laukuma vairs nav vērtību.",
            "Uzvarētājs ir spēlētājs ar lielāko punktu skaitu.",
            "\nIespējamās vērtības:",
            "1 - var pieskaitīt savam punktu skaitam.\n",
            "2 - var pieskaitīt savam punktu skaitam vai pārvērst par * (zvaigznīti).\n",
            "3 - var pieskaitīt savam punktu skaitam.\n",
            "* - (zvaigznīte) - uzņem (kopē) skaitliskās vērtības, kas ir zvaigznītes sānos un tās",
            "     pieskaita punktu skaitam (līdz max 3 punktiem).",
            "     Ja zvaigznītei vienā vai abos sānos nav vērtība, tad no punktu skaita noņem 2.\n",
            "x - (zaglītis) - no labās puses skaitliskās vērtības atņem viens un to pieskaita ",
            "     punktu skaitam.",
            "     Ja tiek atņemts no vieninieka, tas vieninieks dzēšas un tiek pieskaitīti vēl",
            "     divi papildus punkti par dzēšanu.",
            "     Ja labajā pusē nav vērtības vai vērtība nav skaitliska, tad netiek iegūti punkti.",
        ]

        header = tk.Label(master=self.rule_frame, text=header_text, font=f"{cfg.font} 14", bg=cfg.bgcolor)
        header.grid(row=0, column=0, sticky=tk.W)

        rule_labels = [header]

        # Rule labels
        pos = 1
        for text in rule_text:
            label = tk.Label(master=self.rule_frame, text=text, font=f"{cfg.font} 12", bg=cfg.bgcolor)
            label.grid(row=pos, column=0, sticky=tk.W)
            rule_labels.append(label),
            pos += 1

        return rule_labels

    def unload(self):
        self.digit_frame.unload()
        self.analyze.unload()

        for widget in self.widgets:
            widget.grid_forget()

        for widget in self.rule_labels:
            widget.grid_forget()


class DigitFrame:
    def __init__(self, parent, game_pos, row, col, selection_callback=None):
        self.parent = parent
        self.game_pos = [i for i in game_pos]
        self.selection_callback = selection_callback

        self.min_box_count = 4

        self.box_coords = {}
        self.digit_boxes = []
        self.widgets = []

        self.frame = tk.Frame(master=self.parent, bg=cfg.bgcolor)
        self.frame.grid(row=row, column=col)
        self.widgets.append(self.frame)

        w, h = self.get_canvas_dimensions()
        self.canvas = tk.Canvas(master=self.frame, width=w, height=h, bg=cfg.bgcolor, highlightthickness=0)
        self.canvas.grid(row=0, column=1)
        self.widgets.append(self.canvas)

        if self.selection_callback:
            self.canvas.bind("<Button-1>", self.click_callback)

        for digit in self.game_pos:
            self.add_box(digit)

    def click_callback(self, click_pos):
        # get the clicked box and call the callback function with the selection
        for pos, box_coords in self.box_coords.items():
            if box_coords[0] < click_pos.x < box_coords[2] and box_coords[1] < click_pos.y < box_coords[3]:
                box_id = self.digit_boxes[pos].box
                return self.selection_callback([pos, box_id])

    def get_canvas_dimensions(self):
        # old
        box_count = self.min_box_count

        w = (cfg.digitbox_size * box_count) + (cfg.digitbox_spacing * (box_count+1))
        h = cfg.digitbox_size + (cfg.digitbox_spacing * 2)

        return w, h

    def add_box(self, digit):
        dbox_count = len(self.digit_boxes)

        if dbox_count >= 8:
            return

        if dbox_count >= self.min_box_count:
            cw = int(self.canvas["width"])
            self.canvas.config(width=cw + cfg.digitbox_spacing + cfg.digitbox_size)

        x = cfg.digitbox_spacing + ((cfg.digitbox_size * dbox_count) + (cfg.digitbox_spacing * dbox_count))
        y = cfg.digitbox_spacing

        digit_box = DigitBox(self.canvas, x, y, digit)
        self.box_coords[len(self.digit_boxes)] = self.canvas.coords(digit_box.box)
        self.digit_boxes.append(digit_box)

    def update_box(self, box_pos, new_val):
        self.canvas.itemconfigure(self.digit_boxes[box_pos].text, text=new_val)

    def update(self, new_game_pos):
        new_game_pos = [i for i in new_game_pos]
        if len(new_game_pos) > len(self.digit_boxes):
            self.add_box(new_game_pos[-1])

        self.game_pos.clear()
        self.game_pos.extend(new_game_pos)

        for pos, box in enumerate(self.digit_boxes):
            try:
                new_val = self.game_pos[pos]
                self.update_box(pos, new_val)
            except IndexError:
                self.update_box(pos, "")

    def unload(self):
        for widget in self.widgets:
            widget.grid_forget()


class DigitFrameEditable(DigitFrame):
    def __init__(self, *args, **kw):
        super().__init__(selection_callback=self.edit, *args, **kw)
        self.input_box = None
        self.selection = None

        self.randomizer_button = self.add_randomizer_button()
        self.plus_button = self.add_plus_button()

        self.allowed_chars = []
        for action, valueinfo in rules.values.items():
            for value in list(valueinfo):
                if str(value) not in self.allowed_chars:
                    self.allowed_chars.append(str(value))

    def unload(self):
        super().unload()
        self.plus_button.grid_forget()

    def add_randomizer_button(self):
        randomizer_button = tk.Button(master=self.frame, width=3, height=1, text="?", font=f"{cfg.font} 20", bg=cfg.button_bgcolor, command=self.randomize)
        randomizer_button.grid(row=0, column=0, padx=15)
        return randomizer_button

    def add_plus_button(self):
        plus_button = tk.Button(master=self.frame, width=3, height=1, text="+", font=f"{cfg.font} 20", bg=cfg.button_bgcolor, command=lambda: self.add_box(""))
        plus_button.grid(row=0, column=2, padx=15)
        return plus_button

    def randomize(self):
        game.randomize_starting_pos(len(self.digit_boxes))
        self.update(game.starting_pos)

    def edit(self, selection):
        if self.input_box:
            return

        self.selection = selection
        pos = selection[0]
        box_id = selection[1]

        vcmd = (window.register(self.validate_input), "%d", "%P")
        self.input_box = tk.Entry(window, width=1, bd=0, relief=tk.FLAT,
                                  bg="#91ffb8", validate="key", validatecommand=vcmd,
                                  justify="center", font=f"{cfg.font} 75")
        try:
            self.input_box.insert(0, self.game_pos[pos])
        except IndexError:
            self.input_box.insert(0, "")

        offset_x = self.canvas.winfo_rootx() - self.parent.winfo_rootx()
        offset_y = self.canvas.winfo_rooty() - self.parent.winfo_rooty()

        self.input_box.place(width=cfg.digitbox_size, height=cfg.digitbox_size, x=self.digit_boxes[pos].x + offset_x, y=self.digit_boxes[pos].y + offset_y)
        self.input_box.bind("<Return>", self.save_edit)
        self.input_box.bind("<Escape>", self.quit_edit)
        self.input_box.focus()

    def quit_edit(self, event=None):
        self.input_box.destroy()
        self.input_box = None
        self.selection = None

    def save_edit(self, event=None):
        inp_digit = self.input_box.get()

        if not inp_digit:
            self.game_pos.pop(self.selection[0])
            game.starting_pos.pop(self.selection[0])
        else:
            if inp_digit.isdigit():
                digit = int(inp_digit)
            else:
                digit = str(inp_digit)

            try:
                game.starting_pos[self.selection[0]] = digit
                self.game_pos[self.selection[0]] = digit
            except IndexError:
                game.starting_pos.append(digit)
                self.game_pos.append(digit)

        self.update(self.game_pos)

        self.quit_edit()

    def validate_input(self, action, P):
        if len(P) <= 1:
            if action == "1":
                if P in self.allowed_chars:
                    return True
                else:
                    window.bell()
                    return False
            return True
        else:
            window.bell()
            return False


class DigitBox:
    def __init__(self, canvas, x, y, digit=None, outline=cfg.outline_col, width=2, fill="#ffffff", size=cfg.digitbox_size, fontsize=75):
        self.canvas = canvas
        self.x = x
        self.y = y
        if not digit:
            digit = ""
        self.digit = digit

        self.box = self.canvas.create_rectangle(self.x, self.y, self.x + size, self.y + size, outline=outline, width=width, fill=fill)

        center_x = int(self.x + (size/2))
        center_y = int(self.y + (size/2))
        self.text = self.canvas.create_text(center_x, center_y, text=self.digit, font=f"{cfg.font} {fontsize}")


if __name__ == "__main__":
    window = tk.Tk()
    window.title("1. praktiskais darbs AI")
    window.configure(bg=cfg.bgcolor)
    window.resizable(False, False)
    main_app = MainApplication(window)
    window.mainloop()

