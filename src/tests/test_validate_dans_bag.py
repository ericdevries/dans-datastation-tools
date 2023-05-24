from io import StringIO
from unittest.mock import patch, Mock

from datastation.common.result_writer import JsonResultWriter
from datastation.dans_bag.validate_dans_bag import ValidateDansBag


class TestValidateDansBag:

    def test_post_not_called_when_dry_run(self):
        with patch('requests.post') as mock_post:
            config = {'service_baseurl': 'http://service-base-url'}
            validator = ValidateDansBag(config)
            validator.validate_dans_bag('some/path', 'SIP', None, dry_run=True)
            mock_post.assert_not_called()

    def test_post_called_when_not_dry_run(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value.text = '{}'
            config = {'service_baseurl': 'http://service-base-url'}
            validator = ValidateDansBag(config)
            validator.validate_dans_bag('some/path', 'SIP', JsonResultWriter(StringIO()))
            mock_post.assert_called_once()

    def test_post_called_with_expected_url(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value.text = '{}'
            config = {'service_baseurl': 'http://service-base-url'}
            validator = ValidateDansBag(config)
            validator.validate_dans_bag('some/path', 'SIP', JsonResultWriter(StringIO()))
            mock_post.assert_called_once_with('http://service-base-url/validate', data=mock_post.call_args[1]['data'],
                                              headers=mock_post.call_args[1]['headers'])

    def test_raises_exception_when_accept_type_is_unknown(self):
        with patch('requests.post'):
            config = {'service_baseurl': 'http://service-base-url'}
            validator = ValidateDansBag(config, accept_type='unknown')
            try:
                validator.validate_dans_bag('some/path', 'SIP', JsonResultWriter(StringIO()))
            except Exception as e:
                assert str(e) == "Unknown accept type: unknown"
            else:
                assert False, "Exception expected"

    def test_post_called_with_expected_headers(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value.text = '{}'
            config = {'service_baseurl': 'http://service-base-url'}
            validator = ValidateDansBag(config)
            validator.validate_dans_bag('some/path', 'SIP', JsonResultWriter(StringIO()))
            assert mock_post.call_args[1]['headers']['Accept'] == 'application/json'

    def test_command_contains_bag_location(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value.text = '{}'
            config = {'service_baseurl': 'http://service-base-url'}
            validator = ValidateDansBag(config)
            validator.validate_dans_bag('some/path', 'SIP', JsonResultWriter(StringIO()))
            assert 'bagLocation' in mock_post.call_args[1]['data']
            assert 'some/path' in mock_post.call_args[1]['data']

    def test_json_used_for_loading_result_when_accept_type_is_json(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value.text = '{"some": "json"}'
            config = {'service_baseurl': 'http://service-base-url'}
            validator = ValidateDansBag(config, accept_type='application/json')
            mock_result_writer = Mock()
            with patch('json.loads') as mock_json_loads:
                validator.validate_dans_bag('some/path', 'SIP', mock_result_writer)
                mock_json_loads.assert_called_once_with('{"some": "json"}')

    def test_yaml_used_for_loading_result_when_accept_type_is_yaml(self):
        with patch('requests.post') as mock_post:
            mock_post.return_value.text = 'some: yaml'
            config = {'service_baseurl': 'http://service-base-url'}
            validator = ValidateDansBag(config, accept_type='text/plain')
            mock_result_writer = Mock()
            with patch('yaml.safe_load') as mock_yaml_safe_load:
                validator.validate_dans_bag('some/path', 'SIP', mock_result_writer)
                mock_yaml_safe_load.assert_called_once_with('some: yaml')
