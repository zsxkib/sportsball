"""Tests for the catboost trainer."""
import unittest

from sportsball.strategy.trainers.catboost import CatboostTrainer


class TestCatboostTrainer(unittest.TestCase):

    def setUp(self):
        self._trainer = CatboostTrainer("", [], [])

    def test_not_null(self):
        self.assertIsNotNone(self._trainer)
