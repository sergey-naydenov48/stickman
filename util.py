
def strict_between(q, qmin, qmax):
    """
    >>> strict_between(2, 1, 3)
    True
    >>> strict_between(2, 3, 1)
    True
    >>> strict_between(4, 1, 3)
    False
    >>> strict_between(4, 3, 1)
    False
    >>> strict_between(0, 1, 3)
    False
    >>> strict_between(0, 1, 3)
    False
    >>> strict_between(1, 1, 3)
    False
    >>> strict_between(3, 1, 3)
    False
    """
    q, qmin, qmax = int(q), int(qmin), int(qmax)
    if qmin > qmax:
        qmin, qmax = qmax, qmin
    return qmin < q and q < qmax


def between(q, qmin, qmax):
    """
    >>> between(2, 1, 3)
    True
    >>> between(1, 1, 3)
    True
    >>> between(3, 1, 3)
    True
    >>> between(0, 1, 3)
    False
    >>> between(4, 1, 3)
    False
    """
    q, qmin, qmax = int(q), int(qmin), int(qmax)
    return strict_between(q, qmin, qmax) or q in (qmin, qmax)


def segments_overlap(a1, a2, b1, b2):
    """
    >>> segments_overlap(10, 15, 16, 20)
    False
    >>> segments_overlap(1, 7, 10, 15)
    False
    >>> segments_overlap(10, 15, 15, 20)
    False
    >>> segments_overlap(1, 10, 10, 15)
    False
    >>> segments_overlap(10, 15, 14, 20)
    True
    >>> segments_overlap(1, 11, 10, 15)
    True
    >>> segments_overlap(10, 15, 11, 14)
    True
    >>> segments_overlap(10, 15, 9, 16)
    True
    >>> segments_overlap(10, 15, 10, 15)
    True
    >>> segments_overlap(10, 15, 11, 15)
    True
    >>> segments_overlap(10, 15, 10, 14)
    True
    >>> segments_overlap(15, 10, 9, 16)
    True
    >>> segments_overlap(10, 15, 16, 9)
    True
    """
    a1, a2, b1, b2 = int(a1), int(a2), int(b1), int(b2)
    if a1 > a2:
        a1, a2 = a2, a1
    if b1 > b2:
        b1, b2 = b2, b1
    return (
        strict_between(a1, b1, b2)
        or strict_between(a2, b1, b2)
        or (a1 <= b1 and b2 <= a2)
    )


class Coords(object):
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def __str__(self):
        return "Coords(x1={}, y1={}, x2={}, y2={})".format(
                self.x1, self.y1, self.x2, self.y2
                )


def within_x(a, b):
    return segments_overlap(a.x1, a.x2, b.x1, b.x2)


def within_y(a, b):
    return segments_overlap(a.y1, a.y2, b.y1, b.y2)


def collided_left(a, b):
    return within_y(a, b) and strict_between(a.x1, b.x1, b.x2)


def collided_right(a, b):
    return within_y(a, b) and strict_between(a.x2, b.x1, b.x2)


def collided_top(a, b):
    return within_x(a, b) and strict_between(a.y1, b.y1, b.y2)


def collided_bottom(y, a, b):
    if within_x(a, b):
        y_calc = a.y2 + y
        if strict_between(y_calc, b.y1, b.y2):
            return True
    return False
