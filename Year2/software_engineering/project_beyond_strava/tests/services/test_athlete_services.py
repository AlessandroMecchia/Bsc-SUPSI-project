import pytest
from unittest.mock import patch
import client_lib.services.athlete_services as service
from client_lib.exception import ApiException


class TestAthleteServices:

    @patch.object(service.client, "get")
    def test_get_athlete(self, mock_get):
        mock_get.return_value = {"_id": 1, "name": "Paolo"}
        result = service.get_athlete(1)
        mock_get.assert_called_once_with("/athletes/1")
        assert result == {"_id": 1, "name": "Paolo"}

    @patch.object(service.client, "get")
    def test_get_all_athletes(self, mock_get):
        mock_get.return_value = [{"_id": 1}, {"_id": 2}]
        result = service.get_all_athletes()
        mock_get.assert_called_once_with("/athletes")
        assert result == [{"_id": 1}, {"_id": 2}]

    @patch.object(service.client, "post")
    def test_add_athlete(self, mock_post):
        athlete_data = {"_id": 123, "name": "Paolo", "last_name": "Rossi"}
        mock_post.return_value = {"_id": 123}
        result = service.add_athlete(athlete_data)
        mock_post.assert_called_once_with("/athletes", data=athlete_data)
        assert result == {"_id": 123}

    @patch.object(service.client, "put")
    def test_update_athlete(self, mock_put):
        update_data = {"name": "Giovanni"}
        mock_put.return_value = {"_id": 1, "name": "Giovanni"}
        result = service.update_athlete(1, update_data)
        mock_put.assert_called_once_with("/athletes/1", data=update_data)
        assert result == {"_id": 1, "name": "Giovanni"}

    @patch.object(service.client, "delete")
    def test_delete_athlete(self, mock_delete):
        mock_delete.return_value = {"status": "deleted"}
        result = service.delete_athlete(1)
        mock_delete.assert_called_once_with("/athletes/1")
        assert result == {"status": "deleted"}

    @patch.object(service.client, "get")
    def test_get_summary_athlete(self, mock_get):
        mock_get.return_value = {"summary": "details"}
        result = service.get_summary_athlete(1)
        mock_get.assert_called_once_with("/athletes/1/summary")
        assert "summary" in result

    @patch.object(service.client, "get")
    def test_get_athlete_api_exception(self, mock_get):
        mock_get.side_effect = ApiException(404, "Not Found")
        with pytest.raises(ApiException):
            service.get_athlete(999)
