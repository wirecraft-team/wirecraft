from wirecraft.client.ui.camera import WorldObjectBounds


def intersect_bounds(object1: WorldObjectBounds, object2: WorldObjectBounds):
    return (
        max(object1[0], object2[0]),
        min(object1[1], object2[1]),
        max(object1[2], object2[2]),
        min(object1[3], object2[3]),
    )
