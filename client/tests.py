#!/usr/bin/env python3


import unittest

from errors import InvalidRow, InvalidCol
from board import Board


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.dimension = 8
        self.board = Board(self.dimension)
        self.board.control_matrix[6][7] = 3

    def test_fire(self):
        self.assertEqual(self.board.fire('a', 0), 1)
        self.assertEqual(self.board.fire('a', 0), 0)
        self.assertEqual(self.board.fire(2, 1), 1)
        self.assertEqual(self.board.fire(2, 1), 0)
        self.assertEqual(self.board.fire(3, 'a'), 1)
        self.assertEqual(self.board.fire(3, 'a'), 0)
        self.assertEqual(self.board.fire(6, 7), 2)

        self.assertEqual(self.board.control_matrix[0][0], 1)
        self.assertEqual(self.board.control_matrix[2][1], 1)
        self.assertEqual(self.board.control_matrix[3][0], 1)
        self.assertEqual(self.board.control_matrix[6][7], 2)

        with self.assertRaises(InvalidRow):
            self.board.fire('i', 0)

        with self.assertRaises(InvalidRow):
            self.board.fire(-1, 0)

        with self.assertRaises(InvalidRow):
            self.board.fire(9, 0)

        with self.assertRaises(InvalidRow):
            self.board.fire('5', 0)

        with self.assertRaises(InvalidRow):
            self.board.fire('abc', 0)

        with self.assertRaises(InvalidCol):
            self.board.fire('a', 0)

        with self.assertRaises(InvalidCol):
            self.board.fire('a', 9)

        with self.assertRaises(InvalidCol):
            self.board.fire('a', 'k')

        with self.assertRaises(InvalidCol):
            self.board.fire('a', '5')

        with self.assertRaises(InvalidCol):
            self.board.fire('a', 'abc')


if __name__ == '__main__':
    unittest.main()
