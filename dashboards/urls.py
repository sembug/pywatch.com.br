# -*- coding:utf-8 -*-

# Stdlib imports

# Core Django imports
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url, include
from django.core.urlresolvers import reverse_lazy
from django.conf import settings
# Third-party app imports

# Imports from your apps
from .views import (
    DashboardIndexTemplateView,
    TalkIndexTemplateView,
    TalkListView,
    ScreencastIndexTemplateView,
)

urlpatterns = patterns(
    'dashboards.views',
    url(
        r'^$',
        DashboardIndexTemplateView.as_view(),
        name='dashboard-index-view'
    ),
    url(
        r'^talks/$',
        TalkIndexTemplateView.as_view(),
        name='dashboard-talk-index-view'
    ),
    url(
        r'^talks/list/$',
        TalkListView.as_view(),
        name='dashboard-talk-list-view'
    ),
    url(
        r'^screencasts/$',
        ScreencastIndexTemplateView.as_view(),
        name='dashboard-screencast-index-view'
    ),
)
