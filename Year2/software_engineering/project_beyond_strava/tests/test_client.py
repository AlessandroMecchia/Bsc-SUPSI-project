import pytest
from unittest.mock import patch, Mock
from client_lib.client import APIClient
from client_lib.exception import ApiException, NetworkError
from requests.exceptions import RequestException


@pytest.fixture
def client():
    return APIClient(base_url="http://mockserver")


def mock_response(status=200, json_data=None, text_data="Error"):
    mock_resp = Mock()
    mock_resp.ok = (200 <= status < 300)
    mock_resp.status_code = status
    mock_resp.text = text_data
    mock_resp.json = Mock(return_value=json_data if json_data else {})
    return mock_resp


class TestAPIClient:

    # ---- GET ----

    @patch("client_lib.client.requests.Session.get")
    def test_get_success(self, mock_get, client):
        mock_get.return_value = mock_response(json_data={"key": "value"})
        result = client.get("test-endpoint")
        assert result == {"key": "value"}

    @patch("client_lib.client.requests.Session.get")
    def test_get_network_error(self, mock_get, client):
        mock_get.side_effect = RequestException("Connection error")
        with pytest.raises(NetworkError):
            client.get("fail-endpoint")

    @patch("client_lib.client.requests.Session.get")
    def test_get_api_error(self, mock_get, client):
        mock_get.return_value = mock_response(status=404)
        with pytest.raises(ApiException) as exc_info:
            client.get("not-found")
        assert exc_info.value.status_code == 404

    @patch("client_lib.client.requests.Session.get")
    def test_get_invalid_json(self, mock_get, client):
        mock_get.return_value = mock_response()
        mock_get.return_value.json.side_effect = ValueError("Invalid JSON")
        with pytest.raises(ApiException):
            client.get("bad-json")

    # ---- POST ----

    @patch("client_lib.client.requests.Session.post")
    def test_post_success(self, mock_post, client):
        mock_post.return_value = mock_response(json_data={"result": "ok"})
        result = client.post("post-endpoint", data={"name": "test"})
        assert result == {"result": "ok"}

    @patch("client_lib.client.requests.Session.post")
    def test_post_api_error(self, mock_post, client):
        mock_post.return_value = mock_response(status=400)
        with pytest.raises(ApiException):
            client.post("bad-request", data={"name": "bad"})

    @patch("client_lib.client.requests.Session.post")
    def test_post_invalid_json(self, mock_post, client):
        mock_post.return_value = mock_response()
        mock_post.return_value.json.side_effect = ValueError("Invalid JSON")
        with pytest.raises(ApiException):
            client.post("bad-json", data={"name": "test"})

    @patch("client_lib.client.requests.Session.post")
    def test_post_network_error(self, mock_post, client):
        mock_post.side_effect = RequestException("Connection error")
        with pytest.raises(NetworkError):
            client.post("post-endpoint", data={"key": "value"})

    # ---- PUT ----

    @patch("client_lib.client.requests.Session.put")
    def test_put_success(self, mock_put, client):
        mock_put.return_value = mock_response(json_data={"updated": True})
        result = client.put("put-endpoint", data={"key": "value"})
        assert result == {"updated": True}

    @patch("client_lib.client.requests.Session.put")
    def test_put_invalid_json(self, mock_put, client):
        mock_put.return_value = mock_response()
        mock_put.return_value.json.side_effect = ValueError()
        with pytest.raises(ApiException):
            client.put("bad-json", data={"key": "value"})

    @patch("client_lib.client.requests.Session.put")
    def test_put_network_error(self, mock_put, client):
        mock_put.side_effect = RequestException("Connection error")
        with pytest.raises(NetworkError):
            client.put("put-endpoint", data={"key": "value"})

    # ---- DELETE ----

    @patch("client_lib.client.requests.Session.delete")
    def test_delete_success(self, mock_delete, client):
        mock_delete.return_value = mock_response(json_data={"deleted": True})
        result = client.delete("delete-endpoint")
        assert result == {"deleted": True}

    @patch("client_lib.client.requests.Session.delete")
    def test_delete_error(self, mock_delete, client):
        mock_delete.return_value = mock_response(status=500)
        with pytest.raises(ApiException):
            client.delete("fail-endpoint")

    @patch("client_lib.client.requests.Session.delete")
    def test_delete_network_error(self, mock_delete, client):
        mock_delete.side_effect = RequestException("Connection error")
        with pytest.raises(NetworkError):
            client.delete("delete-endpoint")
