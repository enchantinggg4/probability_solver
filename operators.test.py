import unittest
from logical_types import Condition, State, Card, prefix_pool

from operators import full_random_roll, prefix_reroll, roll_guarantee_red
from logical_types import any_state


class TestRandomRoll(unittest.TestCase):

    def test_full_random(self):
        s0, p = full_random_roll(
            State(
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
                ])
            )
        )
        self.assertEqual(s0, any_state())
        self.assertAlmostEqual(p, 0.08)

    def test_reroll_prefixes_single(self):
        s0, p = prefix_reroll(
            State(
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
                ])
            )
        )
        self.assertEqual(
            s0,
            State(
                Condition('or', prefix_pool),
                Condition("or", [
                    Card("10", "R"),
                    Card("10", "B"),

                    Card("9", "R"),
                    Card("9", "B"),

                    Card("8", "R"),
                    Card("8", "B"),

                    Card("7", "R"),
                    Card("7", "B"),
                ])
            )
        )
        self.assertAlmostEqual(p, 0.1)

    def test_reroll_prefixes_multiple(self):
        s0, p = prefix_reroll(
            State(
                Condition("or", [
                    Card("J", "R"),
                    Card("J", "B"),

                    Card("A", "R"),
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
                ])
            )
        )
        self.assertEqual(
            s0,
            State(
                Condition('or', prefix_pool),
                Condition("or", [
                    Card("10", "R"),
                    Card("10", "B"),

                    Card("9", "R"),
                    Card("9", "B"),

                    Card("8", "R"),
                    Card("8", "B"),

                    Card("7", "R"),
                    Card("7", "B"),
                ])
            )
        )
        self.assertAlmostEqual(p, 0.3)

    def test_reroll_prefixes_multiple_complex(self):
        s0, p = prefix_reroll(
            State(
                Condition("and", [
                    Card("A", "R"),

                    Condition('or', [
                        Card("J", "R"),
                        Card("J", "B"),
                    ])
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
                ])
            )
        )
        self.assertEqual(
            s0,
            State(
                Condition('or', prefix_pool),
                Condition("or", [
                    Card("10", "R"),
                    Card("10", "B"),

                    Card("9", "R"),
                    Card("9", "B"),

                    Card("8", "R"),
                    Card("8", "B"),

                    Card("7", "R"),
                    Card("7", "B"),
                ])
            )
        )
        self.assertAlmostEqual(p, 0.02)

    def test_guarantee_red_black(self):
        s0, p = roll_guarantee_red(
            State(
                Condition("and", [
                    Card("J", "B")
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
                ])
            )
        )

        self.assertAlmostEqual(p, 0.04)

    def test_guarantee_red_red(self):
        s0, p = roll_guarantee_red(
            State(
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
                ])
            )
        )

        self.assertAlmostEqual(p, 0.12)

    def test_guarantee_red_mult(self):
        s0, p = roll_guarantee_red(
            State(
                Condition("and", [
                    Card("J", "R"),
                    Card("J", "B")
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
                ])
            )
        )

        self.assertAlmostEqual(p, 0.004)

    def test_guarantee_red_big(self):
        print('alarm')
        s0, p = roll_guarantee_red(
            State(
                Condition("or", prefix_pool),

                Condition("or", [
                    Card("10", "R"),
                    Card("10", "B"),

                    Card("9", "R"),
                    Card("9", "B"),

                    Card("8", "R"),
                    Card("8", "B"),

                    Card("7", "R"),
                    Card("7", "B"),
                ])
            )
        )

        self.assertAlmostEqual(p, 0.8)


if __name__ == '__main__':
    unittest.main()
