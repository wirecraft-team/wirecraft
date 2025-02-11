from wirecraft.client.ui.camera import ObjectBounds


def intersect_bounds(object1: ObjectBounds, object2: ObjectBounds):
    return (
        max(object1[0], object2[0]),
        min(object1[1], object2[1]),
        max(object1[2], object2[2]),
        min(object1[3], object2[3]),
    )
