import unittest
from logical_types import Condition, State, Card, prefix_pool

from util import state_chance

class TestRandomRoll(unittest.TestCase):

    def test_uncond(self):
        s1 = State(
            Condition("and", [
                Card("J", "R")
            ]), 
            
            Condition("or", [
                Card("10", "R"),
                Card("10", "B"),
                
                Card("9", "R"),
                Card("9", "B"),
                
                Card("8", "R"),
                Card("8", "B"),
                
                Card("7", "R"),
                Card("7", "B"),
            ]))
        p = state_chance(s1.suffixes)
        self.assertAlmostEqual(p, 0.8)

        p = state_chance(s1.prefixes)
        self.assertAlmostEqual(p, 0.1)


    def test_smaller_pool(self):
        smaller_pool = [x for x in prefix_pool if x.color == 'R']
        p = state_chance(Condition("and", [
                Card("J", "R")
            ]), 
            _pp=smaller_pool
        )
        
        self.assertAlmostEqual(p, 0.2)

    def test_smaller_pool_exc(self):
        smaller_pool = [x for x in prefix_pool if x.color == 'R']
        p = state_chance(Condition("and", [
                Card("J", "B")
            ]), 
            _pp=smaller_pool
        )
        
        self.assertAlmostEqual(p, 0)

if __name__ == '__main__':
    unittest.main()