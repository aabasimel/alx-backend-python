#!/usr/bin/env python3
"""

Unit tests for utils.py
"""
import unittest
from unittest.mock import patch, Mock
from typing import Mapping
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map."""

    @parameterized.expand(
        [
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
        ]
    )
    def test_access_nested_map(self, nested_map: Mapping, path, expected):
        """Test correct return values."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand(
        [
            (
                {},
                ("a",),
            ),
            ({"a": 1}, ("a", "b")),
        ]
    )
    def test_access_nested_map_exception(self, nested_map: Mapping, path):
        """Test that KeyError is raised for invalid paths."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for get_json function."""

    @parameterized.expand(
        [
            ("example", "http://example.com", {"payload": True}),
            ("holberton", "http://holberton.io", {"payload": False}),
        ]
    )
    @patch("utils.requests.get")
    def test_get_json(self, name, test_url, test_payload, mock_get):
        """Test that get_json returns the expected payload"""
        # configure the mock to return a response with .json()=test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)
        mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """Test case for the memoize decorator."""

    def test_memoize(self):
        """Test that memoize caches the result of a method."""

        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        # Patch a_method so we can track calls
        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            obj = TestClass()

            # Call a_property twice
            result1 = obj.a_property
            result2 = obj.a_property

            # Both calls should return the same value
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # But a_method should have only been called once
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()
