from unittest.mock import mock_open, patch
from src.utils import load_operations


class TestLoadOperationsMocked:
    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1}]')
    def test_valid_data_via_mock(self, mock_file):
        result = load_operations("dummy_path.json")
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0]["id"] == 1

    @patch("builtins.open", side_effect=FileNotFoundError("No such file"))
    def test_file_not_found_via_mock(self, mock_file):
        result = load_operations("missing_file.json")
        assert isinstance(result, list)
        assert len(result) == 0
        mock_file.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="{\"total\": 10}")
    def test_json_not_list_via_mock(self, mock_file):
        result = load_operations("data.json")
        assert isinstance(result, list)
        assert len(result) == 0

    @patch("builtins.open", new_callable=mock_open, read_data="not json at all")
    def test_invalid_json_via_mock(self, mock_file):
        result = load_operations("bad.json")
        assert isinstance(result, list)
        assert len(result) == 0
