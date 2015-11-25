#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Flask-Navigate
    ~~~~~~~~~~~~~~

    A dead simple navigation for your Flask application.

    :copyright: (c) 2015 by Vital Kudzelka <vital.kudzelka@gmail.com>
    :license: MIT
"""
from math import ceil
from flask import (
    current_app, request
)
from flask_navigate.compat import xrange


__version__ = '0.0.1'


class Pager(object):
    """Page number generator.

    The three parameters control the thresholds how many numbers should be
    produced from the sides. Skipped page numbers are represented as `None`.
    This is how you could render such a pagination in the templates:

    .. sourcecode:: html+jinja

        {% macro render_pagination(pages, endpoint) %}
          <div class="pagination">
            {%- for page in pages() %}
              {% if page %}
                {% if page == pages.page %}
                  <a href="{{ url_for(endpoint, page=page, **pages.args) }}">{{ page }}</a>
                {% else %}
                  <span>{{ page }}</span>
                {% endif %}
              {% else %}
                <span class="ellipsis">‥.</span>
              {% endif %}
            {%- endfor %}
          </div>
        {% endmacro %}
    """

    left_threshold = 2
    threshold = 0
    right_threshold = 1

    def __init__(self, page=None, pages=None, left_threshold=None,
                 threshold=None, right_threshold=None):
        self.page = page
        self.pages = pages

        if threshold is not None:
            self.threshold = threshold

        if left_threshold is not None:
            self.left_threshold = left_threshold

        if right_threshold is not None:
            self.right_threshold = right_threshold

    def __iter__(self):
        threshold = self.threshold
        left_threshold = self.left_threshold
        right_threshold = self.right_threshold

        ellipsis_at = 0
        for num in xrange(1, self.pages + 1):
            if ((num <= left_threshold) or
                (abs(self.page - num) <= threshold) or
                ((self.pages - num) < right_threshold)):
                if ellipsis_at + 1 != num:
                    yield None
                yield num
                ellipsis_at = num
        raise StopIteration()


class PageState(object):

    def __init__(self, page=None, per_page=None, total=None,
                 pager_class=None, args=None, items=None):
        self.page = page
        self.per_page = per_page
        self.total = total
        self.total_pages = int(ceil(total / float(per_page)))
        self.pager_class = pager_class
        self.args = args
        self.items = items

    @property
    def has_next(self):
        return self.page < self.total_pages

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def next_page(self):
        if self.has_next:
            return self.page + 1

    @property
    def prev_page(self):
        if self.has_prev:
            return self.page - 1

    def __call__(self, left_threshold=None, threshold=None, right_threshold=None):
        return self.pager_class(self.page, self.total_pages, left_threshold,
                                threshold, right_threshold)


class Navigator(object):
    """Navigate your Flask application easily."""

    pager_class = Pager

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('NAVIGATE_PER_PAGE', 10)

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['navigator'] = self

    def paginate(self, page=None, per_page=None, **extra):
        page = page or self.page
        per_page = per_page or self.per_page
        return PageState(
            page=page,
            per_page=per_page,
            pager_class=self.pager_class,
            args=self.args,
            **extra
        )

    @property
    def page(self):
        return self._parse_request_argument('page')

    @property
    def per_page(self):
        return self._parse_request_argument(
            'per_page',
            current_app.config['NAVIGATE_PER_PAGE']
        )

    @classmethod
    def _parse_request_argument(cls, name, default=1):
        try:
            value = int(request.args.get(name, default))

            if value < 1:
                value = default

        except (TypeError, ValueError):
            value = default

        return value

    @property
    def args(self):
        request_args = request.args.items(multi=True)
        view_args = request.view_args.items()

        args = {}
        for k, value in list(request_args) + list(view_args):
            if k == 'page':
                continue
            if k not in args:
                args[k] = value
            elif not isinstance(args[k], list):
                args[k] = [args[k], value]
            else:
                args[k].append(value)

        return args


class SQLAlchemyNavigator(Navigator):
    """Uses SQLAlchemy query object to create navigation."""

    def paginate(self, query, page=None, per_page=None):
        page = page or self.page
        per_page = per_page or self.per_page
        items = query.offset((page - 1) * per_page).limit(per_page).all()

        # No need to count if we're on the first page and there are fewer
        # items than we expected.
        if page == 1 and len(items) < per_page:
            total = len(items)
        else:
            total = query.order_by(None).count()

        return super(SQLAlchemyNavigator, self).paginate(
            page=page,
            per_page=per_page,
            total=total,
            items=items
        )
