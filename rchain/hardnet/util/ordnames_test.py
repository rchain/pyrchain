import unittest

from .ordnames import OrdinalNames

class TestOrdinalNames(unittest.TestCase):

    def test_simple(self):
        names = OrdinalNames()
        self.assertEqual('Alfa', names[0])
        self.assertEqual('Bravo', names[1])
        self.assertEqual('Echo', names[4])
        self.assertEqual('Zulu', names[25])
        self.assertEqual('Alfa One', names[26])
        self.assertEqual('Alfa Two', names[52])
