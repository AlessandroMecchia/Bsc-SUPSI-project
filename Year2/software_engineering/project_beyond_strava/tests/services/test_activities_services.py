import pytest
from unittest.mock import patch
import client_lib.services.activities_services as service
from client_lib.exception import ApiException


class TestActivityServices:

    @patch.object(service.client, "get")
    def test_get_activity(self, mock_get):
        mock_get.return_value = {"id": 1, "name": "Run"}
        result = service.get_activity(1)
        mock_get.assert_called_once_with("/activities/1")
        assert result == {"id": 1, "name": "Run"}

    @patch.object(service.client, "get")
    def test_get_all_activities(self, mock_get):
        mock_get.return_value = [{"id": 1}, {"id": 2}]
        result = service.get_all_activities()
        mock_get.assert_called_once_with("/activities")
        assert result == [{"id": 1}, {"id": 2}]

    @patch.object(service.client, "post")
    def test_add_activity(self, mock_post):
        activity_data = {"name": "Bike"}
        mock_post.return_value = {"id": 3}
        result = service.add_activity(activity_data)
        mock_post.assert_called_once_with("/activities", data=activity_data)
        assert result == {"id": 3}

    @patch.object(service.client, "put")
    def test_update_activity(self, mock_put):
        update_data = {"name": "Swim"}
        mock_put.return_value = {"id": 1, "name": "Swim"}
        result = service.update_activity(1, update_data)
        mock_put.assert_called_once_with("/activities/1", data=update_data)
        assert result["name"] == "Swim"

    @patch.object(service.client, "delete")
    def test_delete_activity(self, mock_delete):
        mock_delete.return_value = {"status": "deleted"}
        result = service.delete_activity(1)
        mock_delete.assert_called_once_with("/activities/1")
        assert result["status"] == "deleted"

    @patch.object(service.client, "get")
    def test_get_activity_api_exception(self, mock_get):
        mock_get.side_effect = ApiException(404, "Not Found")
        with pytest.raises(ApiException):
            service.get_activity(999)

    @patch.object(service.client, "post")
    def test_add_activity_api_exception(self, mock_post):
        mock_post.side_effect = ApiException(400, "Bad Request")
        with pytest.raises(ApiException):
            service.add_activity({"invalid": "data"})