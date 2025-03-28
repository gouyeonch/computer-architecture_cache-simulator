#!/usr/bin/env python3

import unittest

from cachesimulator.table import Table

case = unittest.TestCase()


def test_init_default():
    """should initialize table with required parameters and default values"""
    table = Table(num_cols=5, width=78)
    case.assertEqual(table.num_cols, 5)
    case.assertEqual(table.width, 78)
    case.assertEqual(table.alignment, 'left')
    case.assertEqual(table.title, None)
    case.assertEqual(table.header, [])
    case.assertEqual(table.rows, [])


def test_init_optional():
    """should initialize table with optional parameters if supplied"""
    table = Table(num_cols=5, width=78, alignment='right', title='Cache')
    case.assertEqual(table.num_cols, 5)
    case.assertEqual(table.width, 78)
    case.assertEqual(table.alignment, 'right')
    case.assertEqual(table.title, 'Cache')


def test_get_separator():
    """should return the correct ASCII separator string"""
    table = Table(num_cols=5, width=78)
    case.assertEqual(table.get_separator(), '-' * 78)


def test_str_title():
    """should correctly display title"""
    table = Table(num_cols=5, width=12, title='Cache')
    case.assertRegex(
        ''.join(('Cache'.center(12), '\n', ('-' * 12))), str(table))


def test_str_no_title():
    """should not display title if not originally supplied"""
    table = Table(num_cols=5, width=12)
    case.assertEqual(str(table).strip(), '')


class TestAlignment(object):

    def _test_str_align(self, alignment, just):
        table_width = 16
        num_cols = 2
        col_width = table_width // num_cols
        table = Table(
            num_cols=num_cols, width=table_width, alignment=alignment)
        table.header = ['First', 'Last']
        table.rows.append(['Bob', 'Smith'])
        table.rows.append(['John', 'Earl'])
        case.assertEqual(str(table), '{}{}\n{}\n{}{}\n{}{}'.format(
            just('First', col_width), just('Last', col_width),
            '-' * table_width,
            just('Bob', col_width), just('Smith', col_width),
            just('John', col_width), just('Earl', col_width)))

    def test_str_align_left(self):
        """should correctly display table when left-aligned"""
        self._test_str_align(
            alignment='left', just=str.ljust)

    def test_str_align_center(self):
        """should correctly display table when center-aligned"""
        self._test_str_align(
            alignment='center', just=str.center)

    def test_str_align_right(self):
        """should correctly display table when right-aligned"""
        self._test_str_align(
            alignment='right', just=str.rjust)
