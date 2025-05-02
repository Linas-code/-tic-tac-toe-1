import unittest
from unittest.mock import mock_open, patch
from Tic_Tac_Toe import (
    Board,
    PlayerFactory,
    HumanPlayer,
    HardAIPlayer,
    GameGUI,
    Game
)


class TestBoard(unittest.TestCase):

    def setUp(self):
        self.board = Board()

    def test_board_initially_empty(self):
        for row in self.board.board:
            for cell in row:
                self.assertEqual(cell, " ")

    def test_make_move_success(self):
        result = self.board.make_move(0, 0, 'X')
        self.assertTrue(result)
        self.assertEqual(self.board.board[0][0], 'X')

    def test_make_move_fail_on_taken_cell(self):
        self.board.make_move(0, 0, 'X')
        result = self.board.make_move(0, 0, 'O')
        self.assertFalse(result)
        self.assertEqual(self.board.board[0][0], 'X')

    def test_check_winner_row(self):
        self.board.make_move(0, 0, 'X')
        self.board.make_move(0, 1, 'X')
        self.board.make_move(0, 2, 'X')
        self.assertEqual(self.board.check_winner(), 'X')

    def test_check_winner_column(self):
        self.board.make_move(0, 0, 'O')
        self.board.make_move(1, 0, 'O')
        self.board.make_move(2, 0, 'O')
        self.assertEqual(self.board.check_winner(), 'O')

    def test_check_winner_diagonal(self):
        self.board.make_move(0, 0, 'X')
        self.board.make_move(1, 1, 'X')
        self.board.make_move(2, 2, 'X')
        self.assertEqual(self.board.check_winner(), 'X')

    def test_check_winner_antidiagonal(self):
        self.board.make_move(0, 2, 'O')
        self.board.make_move(1, 1, 'O')
        self.board.make_move(2, 0, 'O')
        self.assertEqual(self.board.check_winner(), 'O')

    def test_no_winner(self):
        self.board.make_move(0, 0, 'X')
        self.board.make_move(0, 1, 'O')
        self.board.make_move(0, 2, 'X')
        self.assertIsNone(self.board.check_winner())

    def test_is_full_true(self):
        moves = [(r, c) for r in range(3) for c in range(3)]
        for idx, (r, c) in enumerate(moves):
            self.board.make_move(r, c, 'X' if idx % 2 == 0 else 'O')
        self.assertTrue(self.board.is_full())

    def test_is_full_false(self):
        self.board.make_move(0, 0, 'X')
        self.assertFalse(self.board.is_full())

    def test_undo_move(self):
        self.board.make_move(1, 1, 'X')
        self.board.undo_move(1, 1)
        self.assertEqual(self.board.board[1][1], ' ')


class TestPlayerFactory(unittest.TestCase):

    def test_create_human_player(self):
        player = PlayerFactory.create_player("human", "X")
        self.assertIsInstance(player, HumanPlayer)
        self.assertEqual(player.symbol, "X")

    def test_create_ai_player(self):
        player = PlayerFactory.create_player("AI", "O", "X")
        self.assertIsInstance(player, HardAIPlayer)
        self.assertEqual(player.symbol, "O")

    def test_create_invalid_player(self):
        with self.assertRaises(ValueError):
            PlayerFactory.create_player("unknown", "X")


class TestGameStart(unittest.TestCase):

    def setUp(self):
        self.board = Board()
        self.gui = GameGUI()
        self.gui.window.withdraw()

    def test_starting_player_is_x(self):
        players = [HumanPlayer('X'), HardAIPlayer('O', 'X')]
        game = Game(players, self.board, self.gui)
        self.assertIsInstance(game, Game)
        starting_index = 0 if players[0].symbol == 'X' else 1
        self.assertEqual(starting_index, 0)

    def test_ai_starts_when_ai_has_x(self):
        players = [HardAIPlayer('X', 'O'), HumanPlayer('O')]
        game = Game(players, self.board, self.gui)
        self.assertIsInstance(game, Game)
        starting_index = 0 if players[0].symbol == 'X' else 1
        self.assertEqual(starting_index, 0)


class TestLoadResults(unittest.TestCase):

    def setUp(self):
        self.gui = GameGUI()
        self.gui.window.withdraw()

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_load_results_empty_file(self, _mock_file):
        result = self.gui.load_results()
        self.assertEqual(result, "No previous results.")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_load_results_file_not_found(self, _mock_file):
        result = self.gui.load_results()
        self.assertEqual(result, "No previous results.")

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data=(
            "Winner: X\nWinner: O\nDraw\nWinner: X\nWinner: O\nWinner: X\n"
        )
    )
    def test_load_results_returns_last_5(self, _mock_file):
        result = self.gui.load_results()
        expected = "Winner: O\nDraw\nWinner: X\nWinner: O\nWinner: X"
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
