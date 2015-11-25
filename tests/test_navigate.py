#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest

from flask_navigate import (
    Navigator, PageState, Pager
)


class TestNavigator:

    @pytest.fixture
    def navigator(self, app):
        navigator = Navigator(app)
        return navigator

    def test_init(self, app, navigator):
        assert navigator.app is app
        assert navigator.pager_class is Pager

    def test_register_themself(self, app, navigator):
        assert app.extensions
        assert app.extensions['navigator'] is navigator

    def test_page(self, navigator):
        with navigator.app.test_request_context('?page=42'):
            assert navigator.page == 42

    def test_per_page(self, navigator):
        with navigator.app.test_request_context('?per_page=42'):
            assert navigator.per_page == 42

    @pytest.mark.options(navigate_per_page=7)
    def test_per_page_respects_app_config(self, navigator):
        assert navigator.per_page == 7

    def test_args(self, navigator):
        with navigator.app.test_request_context('/?foo=42&page=3'):
            assert navigator.args == {'foo': '42'}

    def test_list_in_args(self, navigator):
        with navigator.app.test_request_context('/?foo=42&foo=3&page=1'):
            assert navigator.args == {'foo': ['42', '3']}


class TestRequestParser(TestNavigator):

    def test_positive_number(self, app, navigator):
        with app.test_request_context('?foo=42'):
            assert navigator._parse_request_argument('foo') == 42

    def test_negative_number(self, app, navigator):
        with app.test_request_context('?foo=-1'):
            assert navigator._parse_request_argument('foo') == 1

    def test_invalid_number(self, app, navigator):
        with app.test_request_context('?foo=bar'):
            assert navigator._parse_request_argument('foo') == 1

    def test_default_value(self, app, navigator):
        with app.test_request_context('?foo=bar'):
            assert navigator._parse_request_argument('foo', 42) == 42

    def test_none_as_default(self, app, navigator):
        with app.test_request_context('?foo=bar'):
            assert navigator._parse_request_argument('foo', None) is None


class TestPageState:

    @pytest.fixture
    def state(self):
        state = PageState(page=2, per_page=10, total=42, pager_class=Pager)
        return state

    def test_init(self, state):
        assert state.page == 2
        assert state.per_page == 10
        assert state.total == 42
        assert state.total_pages == 5
        assert state.pager_class is Pager
        assert state.args is None
        assert state.items is None

    def test_has_next(self, state):
        assert state.has_next

        state.page = 5
        assert not state.has_next

    def test_has_prev(self, state):
        assert state.has_prev

        state.page = 1
        assert not state.has_prev

    def test_next_page(self, state):
        assert state.next_page == 3

    def test_prev_page(self, state):
        assert state.prev_page == 1

    def test_call(self, state):
        assert list(state()) == [1, 2, None, 5]

    def test_call_with_arguments(self, state):
        assert list(state(1, 0, 0)) == [1, 2]

    def test_custom_pager(self, state):
        class MyPager(Pager):
            def __iter__(self):
                for x in super(MyPager, self).__iter__():
                    yield (x, x)

        state.pager_class = MyPager
        assert list(state()) == [(1, 1), (2, 2), (None, None), (5, 5)]


class TestPager:

    @pytest.fixture
    def pager(self):
        pager = Pager(3, 17, 0, 2, 1)
        return pager

    def test_init(self, pager):
        assert pager.page == 3
        assert pager.pages == 17
        assert pager.left_threshold == 0
        assert pager.threshold == 2
        assert pager.right_threshold == 1

    def test_generator(self, pager):
        assert list(pager) == [1, 2, 3, 4, 5, None, 17]
