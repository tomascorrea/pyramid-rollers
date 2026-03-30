# -*- encoding: utf-8 -*-
import unittest
from unittest import mock

from pyramid_rollers import util


class TestDeprecatedUtils(unittest.TestCase):
    def test_extract_json_data_is_deprecated(self):
        with mock.patch("pyramid_rollers.util.warnings") as mocked:
            util.extract_json_data(mock.MagicMock())
            self.assertTrue(mocked.warn.called)

    def test_extract_form_urlencoded_data_is_deprecated(self):
        with mock.patch("pyramid_rollers.util.warnings") as mocked:
            util.extract_form_urlencoded_data(mock.MagicMock())
            self.assertTrue(mocked.warn.called)


class CurrentServiceTest(unittest.TestCase):
    def test_current_service_returns_the_service_for_existing_patterns(self):
        request = mock.MagicMock()
        request.matched_route.pattern = "/buckets"
        request.registry.pyramid_rollers_services = {"/buckets": mock.sentinel.service}

        self.assertEqual(util.current_service(request), mock.sentinel.service)

    def test_current_service_returns_none_for_unexisting_patterns(self):
        request = mock.MagicMock()
        request.matched_route.pattern = "/unexisting"
        request.registry.pyramid_rollers_services = {}

        self.assertEqual(util.current_service(request), None)
