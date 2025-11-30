import pytest
import requests
from unittest.mock import Mock, patch
from src.papdzvcl import PapdzVCL, Ok1, Ok2, Ok3
from src.papdzvcl.exceptions import Ok1Exception, Ok2Exception, Ok3Exception


class TestPapdzVCL:
    """Test cases for PapdzVCL class"""

    def test_init_with_base_url(self):
        """Test khởi tạo với base_url"""
        client = PapdzVCL("https://api.example.com")
        assert client.base_url == "https://api.example.com"
        assert client.timeout == 30

    def test_init_without_base_url(self):
        """Test khởi tạo không có base_url"""
        client = PapdzVCL()
        assert client.base_url == ""
        assert client.timeout == 30

    def test_init_with_custom_timeout(self):
        """Test khởi tạo với timeout tuỳ chỉnh"""
        client = PapdzVCL(timeout=60)
        assert client.timeout == 60

    def test_default_headers(self):
        """Test headers mặc định"""
        client = PapdzVCL()
        assert 'User-Agent' in client.session.headers
        assert 'Accept' in client.session.headers
        assert client.session.headers['Accept'] == 'application/json'

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok1_success(self, mock_session):
        """Test Ok1 thành công"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": "test"}
        
        # Mock session
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        response = client.Ok1("/users")

        assert response.status_code == 200
        assert response.json() == {"data": "test"}
        mock_session_instance.get.assert_called_once_with(
            "https://api.example.com/users",
            timeout=30
        )

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok1_with_params(self, mock_session):
        """Test Ok1 với query parameters"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        response = client.Ok1("/users", params={"page": 1, "limit": 10})

        mock_session_instance.get.assert_called_once_with(
            "https://api.example.com/users",
            timeout=30,
            params={"page": 1, "limit": 10}
        )

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok2_success(self, mock_session):
        """Test Ok2 thành công"""
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 1, "name": "test"}
        
        mock_session_instance = Mock()
        mock_session_instance.post.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        data = {"name": "test"}
        response = client.Ok2("/users", json=data)

        assert response.status_code == 201
        mock_session_instance.post.assert_called_once_with(
            "https://api.example.com/users",
            data=None,
            json={"name": "test"},
            timeout=30
        )

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok2_with_form_data(self, mock_session):
        """Test Ok2 với form data"""
        mock_response = Mock()
        mock_response.status_code = 201
        
        mock_session_instance = Mock()
        mock_session_instance.post.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        form_data = {"username": "test", "password": "123"}
        response = client.Ok2("/login", data=form_data)

        mock_session_instance.post.assert_called_once_with(
            "https://api.example.com/login",
            data={"username": "test", "password": "123"},
            json=None,
            timeout=30
        )

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok3_success(self, mock_session):
        """Test Ok3 thành công"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"updated": True}
        
        mock_session_instance = Mock()
        mock_session_instance.put.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        update_data = {"name": "updated_name"}
        response = client.Ok3("/users/1", json=update_data)

        assert response.status_code == 200
        mock_session_instance.put.assert_called_once_with(
            "https://api.example.com/users/1",
            data=None,
            json={"name": "updated_name"},
            timeout=30
        )

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok1_with_full_url(self, mock_session):
        """Test Ok1 với full URL (không dùng base_url)"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        response = client.Ok1("https://other-api.com/data")

        mock_session_instance.get.assert_called_once_with(
            "https://other-api.com/data",
            timeout=30
        )

    def test_set_header(self):
        """Test thiết lập header"""
        client = PapdzVCL()
        client.set_header("X-API-Key", "secret-key")
        
        assert client.session.headers["X-API-Key"] == "secret-key"
        assert client.default_headers["X-API-Key"] == "secret-key"

    def test_set_auth(self):
        """Test thiết lập authentication"""
        client = PapdzVCL()
        client.set_auth("my-token-123")
        
        assert client.session.headers["Authorization"] == "Bearer my-token-123"

    def test_set_auth_custom_type(self):
        """Test thiết lập authentication với loại tuỳ chỉnh"""
        client = PapdzVCL()
        client.set_auth("my-token", "Token")
        
        assert client.session.headers["Authorization"] == "Token my-token"

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok1_timeout(self, mock_session):
        """Test Ok1 với timeout"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = PapdzVCL(timeout=10)
        response = client.Ok1("/test")

        mock_session_instance.get.assert_called_once_with(
            "/test",
            timeout=10
        )

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok1_network_error(self, mock_session):
        """Test Ok1 với lỗi mạng"""
        mock_session_instance = Mock()
        mock_session_instance.get.side_effect = requests.ConnectionError("Network error")
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        
        with pytest.raises(Ok1Exception) as exc_info:
            client.Ok1("/users")
        
        assert "Ok1 failed" in str(exc_info.value)
        assert "Network error" in str(exc_info.value)

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok2_network_error(self, mock_session):
        """Test Ok2 với lỗi mạng"""
        mock_session_instance = Mock()
        mock_session_instance.post.side_effect = requests.Timeout("Timeout error")
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        
        with pytest.raises(Ok2Exception) as exc_info:
            client.Ok2("/users", json={"name": "test"})
        
        assert "Ok2 failed" in str(exc_info.value)

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok3_network_error(self, mock_session):
        """Test Ok3 với lỗi mạng"""
        mock_session_instance = Mock()
        mock_session_instance.put.side_effect = Exception("Random error")
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        
        with pytest.raises(Ok3Exception) as exc_info:
            client.Ok3("/users/1", json={"name": "test"})
        
        assert "Ok3 failed" in str(exc_info.value)

    def test_build_url_with_base_url(self):
        """Test xây dựng URL với base_url"""
        client = PapdzVCL("https://api.example.com")
        
        # Test với endpoint có slash
        url1 = client._build_url("/users")
        assert url1 == "https://api.example.com/users"
        
        # Test với endpoint không có slash
        url2 = client._build_url("users")
        assert url2 == "https://api.example.com/users"
        
        # Test với endpoint nested
        url3 = client._build_url("/v1/users/profile")
        assert url3 == "https://api.example.com/v1/users/profile"

    def test_build_url_without_base_url(self):
        """Test xây dựng URL không có base_url"""
        client = PapdzVCL()
        
        # Test với full URL
        url1 = client._build_url("https://api.example.com/users")
        assert url1 == "https://api.example.com/users"
        
        # Test với relative URL (sẽ giữ nguyên)
        url2 = client._build_url("/users")
        assert url2 == "/users"

    def test_build_url_with_full_url(self):
        """Test xây dựng URL với full URL (bỏ qua base_url)"""
        client = PapdzVCL("https://api.example.com")
        
        url = client._build_url("https://other-api.com/data")
        assert url == "https://other-api.com/data"


class TestStandaloneFunctions:
    """Test cases for standalone functions"""

    @patch('src.papdzvcl.core.PapdzVCL')
    def test_ok1_standalone(self, mock_client_class):
        """Test hàm Ok1 độc lập"""
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_client_instance.Ok1.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client_instance

        response = Ok1("https://api.example.com/users")

        assert response == mock_response
        mock_client_instance.Ok1.assert_called_once_with("https://api.example.com/users")

    @patch('src.papdzvcl.core.PapdzVCL')
    def test_ok2_standalone(self, mock_client_class):
        """Test hàm Ok2 độc lập"""
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_client_instance.Ok2.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client_instance

        data = {"name": "test"}
        response = Ok2("https://api.example.com/users", json=data)

        assert response == mock_response
        mock_client_instance.Ok2.assert_called_once_with(
            "https://api.example.com/users",
            json=data
        )

    @patch('src.papdzvcl.core.PapdzVCL')
    def test_ok3_standalone(self, mock_client_class):
        """Test hàm Ok3 độc lập"""
        mock_client_instance = Mock()
        mock_response = Mock()
        mock_client_instance.Ok3.return_value = mock_response
        mock_client_class.return_value.__enter__.return_value = mock_client_instance

        data = {"name": "updated"}
        response = Ok3("https://api.example.com/users/1", json=data)

        assert response == mock_response
        mock_client_instance.Ok3.assert_called_once_with(
            "https://api.example.com/users/1",
            json=data
        )


class TestIntegration:
    """Test cases tích hợp (cần kết nối mạng)"""

    def test_ok1_with_real_api(self):
        """Test Ok1 với API thật (JSONPlaceholder)"""
        client = PapdzVCL("https://jsonplaceholder.typicode.com")
        
        try:
            response = client.Ok1("/users/1")
            assert response.status_code == 200
            
            data = response.json()
            assert "id" in data
            assert "name" in data
            assert "email" in data
            assert data["id"] == 1
            
        except requests.ConnectionError:
            pytest.skip("No internet connection")

    def test_ok2_with_real_api(self):
        """Test Ok2 với API thật (JSONPlaceholder)"""
        client = PapdzVCL("https://jsonplaceholder.typicode.com")
        
        try:
            new_post = {
                "title": "PAPDZ VCL Test",
                "body": "Testing Ok2 method",
                "userId": 1
            }
            
            response = client.Ok2("/posts", json=new_post)
            assert response.status_code == 201
            
            data = response.json()
            assert "id" in data
            assert data["title"] == "PAPDZ VCL Test"
            
        except requests.ConnectionError:
            pytest.skip("No internet connection")


class TestEdgeCases:
    """Test các trường hợp đặc biệt"""

    def test_empty_base_url(self):
        """Test với base_url rỗng"""
        client = PapdzVCL("")
        url = client._build_url("/test")
        assert url == "/test"

    def test_base_url_with_trailing_slash(self):
        """Test với base_url có trailing slash"""
        client = PapdzVCL("https://api.example.com/")
        url = client._build_url("users")
        assert url == "https://api.example.com/users"

    @patch('src.papdzvcl.core.requests.Session')
    def test_ok1_with_custom_headers(self, mock_session):
        """Test Ok1 với headers tuỳ chỉnh"""
        mock_response = Mock()
        mock_response.status_code = 200
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance

        client = PapdzVCL("https://api.example.com")
        custom_headers = {"X-Custom": "value"}
        response = client.Ok1("/users", headers=custom_headers)

        # Kiểm tra headers được merge
        call_args = mock_session_instance.get.call_args
        called_headers = call_args[1].get('headers', {})
        
        assert 'X-Custom' in called_headers
        assert called_headers['X-Custom'] == 'value'
        assert 'User-Agent' in called_headers  # Header mặc định vẫn tồn tại

    def test_context_manager(self):
        """Test sử dụng client với context manager"""
        with PapdzVCL("https://api.example.com") as client:
            assert isinstance(client, PapdzVCL)
            # Client vẫn hoạt động bình thường trong context


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
