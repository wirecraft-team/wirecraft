class Graph:
    def get_shortest_path(
        self, id: int, to: int | None = None, output: str = "vpath"
    ) -> list[int]: ...
    def __init__(
        self,
        n: int,
        edges: list[tuple[int, int]],
    ) -> None: ...
