from unittest.mock import patch 

from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):

	def test_wait_for_db_ready(self):
		"""Test waiting for db when db is available"""
		with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
			gi.return_value = True
			call_command('wait_for_db')
			self.assertEqual(gi.call_count, 1)
	
	# This patch is for fast and remove delay of running test_wait_for_db
	@patch('time.sleep', return_value=True)
	def test_wait_for_db(self, ts):
		"""Test waiting for db"""
		with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
			# This means that the five time you call this getitem 
			# And its going to raise the OperationalError
			# 5 time call this and the last time(6th) retuen True
			gi.side_effect = [OperationalError] * 5 + [True]
			call_command('wait_for_db')
			self.assertEqual(gi.call_count, 6)
