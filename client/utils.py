#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from emoji import emojize


class Utils:

    @classmethod
    def build_matrix(self, control_matrix, pretty):
        pretty_chars = [':droplet:', ':cross_mark:',
                        ':fire:', ':sailboat:', ':speedboat:', ':ship:']
        chars = ['~', 'X', 'O', 'B']
        matrix = []
        if pretty:
            for control_row in control_matrix:
                row = []
                for cell in control_row:
                    row.append(emojize(pretty_chars[cell]))
                matrix.append(row)
            return matrix

        for control_row in control_matrix:
            row = []
            for cell in control_row:
                if cell > 2:
                    row.append(chars[3])
                else:
                    row.append(chars[cell])
            matrix.append(row)
        return matrix
