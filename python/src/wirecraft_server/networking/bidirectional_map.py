from __future__ import annotations

from pydantic import RootModel


class BidirectionalMap[K, V](RootModel[dict[K, V]]):
    def __init__(self, _revert_reference: BidirectionalMap[V, K] | None = None):
        super().__init__({})  # type: ignore

        if _revert_reference is None:
            self._inverse = BidirectionalMap(self)
        else:
            self._inverse = _revert_reference

    def __repr__(self):
        return f"BidirectionalMap({self.root})"

    @property
    def inverse(self) -> BidirectionalMap[V, K]:
        """
        Get the inverse of this bidirectional map.
        This allows you to look up keys by their values.
        """
        return self._inverse

    def __getitem__(self, key: K) -> V:
        return self.root[key]

    def __setitem__(self, key: K, value: V):
        self.set(key, value)

    def set(self, key: K, value: V):
        self.root[key] = value
        self._inverse.root[value] = key

    def get(self, key: K):
        return self.root.get(key)

    def keys(self):
        return self.root.keys()

    def values(self):
        return self._inverse.root.keys()

    def items(self):
        return self.root.items()

    def __iter__(self):  # type: ignore
        return iter(self.root)
