class Node:
    def __init__(self, level):
        self.level = level

        self.id = None

        self.player1_points = 0
        self.player2_points = 0

        self.children = []
        self._game_pos = []

        self.value = None

    def set_game_pos(self, array: list):
        self._game_pos = [i for i in array]

    def get_game_pos(self) -> list:
        return self._game_pos

    def set_points(self, points: list):
        self.player1_points = points[0]
        self.player2_points = points[1]

    def get_points(self) -> list:
        return [self.player1_points, self.player2_points]

    @staticmethod
    def _add_nodes(src, nodes):
        def add(_node):
            src.append(_node)

        if isinstance(nodes, list):
            for node in nodes:
                add(node)
        else:
            add(nodes)

    def add_children(self, children):
        self._add_nodes(self.children, children)

    def generate_id(self):
        self.id = f"{self.level}-{self.get_points()}-{str(self._game_pos)}"

    def print(self):
        print(f"game_pos: {self._game_pos}")
        print(f"points: {self.get_points()}")
        print(f"id: {self.id}")
        children = [f"\n  *  {str(id(i))} {i.id}" for i in self.children]
        print(f"children: {''.join(children)}")
        print(f"memory loc: {id(self)}")
        if self.value:
            print(f"value: {self.value}")

    def compare(self, node: 'Node'):
        if node.id != self.id:
            return False
        if node.level != self.level:
            return False
        return True
