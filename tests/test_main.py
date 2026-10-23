import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import main


class GenerateEquationTests(unittest.TestCase):
    def test_equation_answers_for_each_equation_type(self):
        cases = [
            (1, [10, 20], 30),
            (2, [10, 5], 5),
            (3, [2, 3], 6),
            (4, [2, 5], 9),
            (5, [3], 9),
            (6, [4], 4),
            (7, [3], 27),
            (8, [4, 5], 11),
            (9, [3, 4], 36),
            (10, [4], 0.25),
            (11, [20, 30], 50),
        ]

        for equation_type, random_values, expected_answer in cases:
            with self.subTest(equation_type=equation_type):
                with patch(
                    "main.rand",
                    side_effect=[equation_type, *random_values],
                ):
                    equation, answer, _ = main.generate_equation({})

                self.assertTrue(equation)
                self.assertEqual(answer, expected_answer)

    def test_equation_can_use_stored_memory_variable(self):
        with (
            patch("main.rand", side_effect=[1, 20, 100, 5]),
            patch("main.choice", return_value="A"),
        ):
            equation, answer, signature = main.generate_equation({"A": 7})

        self.assertEqual(equation, "A + 5")
        self.assertEqual(answer, 12)
        self.assertEqual(signature, ("add_var", "A", 5))


class MainLoopTests(unittest.TestCase):
    def test_status_commands_do_not_use_answer_attempts_and_score_resets(self):
        equations = [
            ("2 + 2", 4, ("add", 2, 2)),
            ("3 + 3", 6, ("add", 3, 3)),
        ]
        answers = ["help", "count", "vars", 4, "exit"]
        output = io.StringIO()
        main._current_score = 99

        with patch("main.signal.signal"):
            with patch("main.generate_equation", side_effect=equations):
                with patch("main.get_user_input", side_effect=answers):
                    with redirect_stdout(output):
                        main.main()

        self.assertEqual(main._current_score, 1)
        self.assertIn("Correct!", output.getvalue())
        self.assertIn("Score: 1 equations solved correctly.", output.getvalue())
        self.assertIn("GAME INSTRUCTIONS", output.getvalue())

    def test_memory_variables_rotate_after_each_configured_interval(self):
        equations = [
            (f"{value} + 0", value, ("add", value, 0))
            for value in (1, 2, 3, 4)
        ]
        answers = [1, 2, 3, "exit"]
        output = io.StringIO()

        with patch("main.signal.signal"):
            with patch("main.generate_equation", side_effect=equations):
                with patch("main.get_user_input", side_effect=answers):
                    with patch("main.get_next_interval", return_value=1):
                        with redirect_stdout(output):
                            main.main()

        self.assertIn("variable 'A' stored with value: 1", output.getvalue())
        self.assertIn("variable 'B' stored with value: 2", output.getvalue())
        self.assertIn("variable 'A' stored with value: 3", output.getvalue())


if __name__ == "__main__":
    unittest.main()
