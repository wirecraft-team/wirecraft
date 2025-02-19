from typing import Any

from wirecraft.client.ui.camera import ObjectBounds


class SingletonMeta(type):
    """
    This is a Metaclass to transform a class into a Singleton.

    A Singleton is a class that can only have one instance at a time.

    For example:
    ```py
    class MyClass(metaclass=SingletonMeta):
        pass

    a = MyClass()
    b = MyClass()
    assert a is b  # True
    ```
    """

    def __call__(cls, *args: Any, **kwargs: Any):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


def intersect_bounds(object1: ObjectBounds, object2: ObjectBounds):
    return (
        max(object1[0], object2[0]),
        min(object1[1], object2[1]),
        max(object1[2], object2[2]),
        min(object1[3], object2[3]),
    )
