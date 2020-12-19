import unittest


def get_clicked_pos(pos, rows, width):
    node_w = width // rows
    y, x = pos
    row = y // node_w
    col = x // node_w
    return row, col


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


class TestGetpos(unittest.TestCase):
    def test_getpos(self):
        self.assertEqual(get_clicked_pos((44, 11), 5, 50), (4, 1))
        self.assertEqual(get_clicked_pos((67, 78), 20, 100), (13, 15))
        self.assertEqual(get_clicked_pos((9, 456), 56, 474), (1, 57))


class TestHfunc(unittest.TestCase):
    def test_hfunc(self):
        self.assertEqual(h((60, 23), (44, 12)), 27)
        self.assertEqual(h((20, 20), (20, 20)), 0)
        self.assertEqual(h((1, 2), (3, 4)), 4)


if __name__ == '__main__':
    unittest1.main()
