# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
import logging
from functools import partial

from importlib.metadata import version as _get_version

from pyramid.events import NewRequest
from pyramid.httpexceptions import HTTPForbidden, HTTPNotFound
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.settings import asbool, aslist

from pyramid_rollers.errors import Errors  # NOQA
from pyramid_rollers.pyramidhook import (
    handle_exceptions,
    register_resource_views,
    register_service_views,
    wrap_request,
)
from pyramid_rollers.renderer import PyramidRollersRenderer
from pyramid_rollers.service import Service  # NOQA
from pyramid_rollers.util import ContentTypePredicate, current_service


logger = logging.getLogger("pyramid_rollers")
__version__ = _get_version(__package__)


def set_localizer_for_languages(event, available_languages, default_locale_name):
    """
    Sets the current locale based on the incoming Accept-Language header, if
    present, and sets a localizer attribute on the request object based on
    the current locale.

    To be used as an event handler, this function needs to be partially applied
    with the available_languages and default_locale_name arguments. The
    resulting function will be an event handler which takes an event object as
    its only argument.
    """
    request = event.request
    if request.accept_language:
        accepted = request.accept_language.lookup(available_languages, default=default_locale_name)
        request._LOCALE_ = accepted


def setup_localization(config):
    """
    Setup localization based on the available_languages and
    pyramid.default_locale_name settings.

    These settings are named after suggestions from the "Internationalization
    and Localization" section of the Pyramid documentation.
    """
    settings = config.get_settings()
    available_languages = aslist(settings["available_languages"])
    default_locale_name = settings.get("pyramid.default_locale_name", "en")
    set_localizer = partial(
        set_localizer_for_languages,
        available_languages=available_languages,
        default_locale_name=default_locale_name,
    )
    config.add_subscriber(set_localizer, NewRequest)


def includeme(config):
    """Include the pyramid-rollers definitions"""
    # attributes required to maintain services
    config.registry.pyramid_rollers_services = {}

    settings = config.get_settings()

    # localization request subscriber must be set before first call
    # for request.localizer (in wrap_request)
    if settings.get("available_languages"):
        setup_localization(config)

    config.add_directive("add_pyramid_rollers_service", register_service_views)
    config.add_directive("add_pyramid_rollers_resource", register_resource_views)
    config.add_subscriber(wrap_request, NewRequest)
    config.add_renderer("pyramid_rollersjson", PyramidRollersRenderer())
    config.add_view_predicate("content_type", ContentTypePredicate)
    config.add_request_method(current_service, reify=True)

    if asbool(settings.get("handle_exceptions", True)):
        config.add_view(handle_exceptions, context=Exception, permission=NO_PERMISSION_REQUIRED)
        config.add_view(handle_exceptions, context=HTTPNotFound, permission=NO_PERMISSION_REQUIRED)
        config.add_view(
            handle_exceptions, context=HTTPForbidden, permission=NO_PERMISSION_REQUIRED
        )
