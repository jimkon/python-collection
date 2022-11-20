import unittest
from unittest.mock import patch, mock_open


class Test(unittest.TestCase):
    def test_open_read(self):
        with patch("builtins.open", mock_open(read_data="data")) as mock_file:
            assert open("path/to/open", 'r').read() == "data"
        mock_file.assert_called_with("path/to/open", 'r')



