# -*- coding: utf-8 -*-
#
# OpenCraft -- tools to aid developing and hosting free software projects
# Copyright (C) 2015-2017 OpenCraft <contact@opencraft.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
Mixins for the Account application.
"""

from rest_framework.permissions import IsAuthenticated

from accounting.account import models


class AccountViewMixin:
    """
    Mixin class adding common fields/functions for other account views to use.
    """

    lookup_field = 'user__username'
    queryset = models.Account.objects.all()
    permission_classes = (IsAuthenticated,)


class AddressViewMixin:
    """
    Mixin class adding common fields/functions for other address views to use.
    """

    lookup_field = 'accounts__user__username'
    queryset = models.Address.objects.all()
    permission_classes = (IsAuthenticated,)
