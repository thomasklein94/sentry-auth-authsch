from __future__ import absolute_import

import pytest

from sentry.auth.exceptions import IdentityNotValid
from sentry.models import AuthIdentity, AuthProvider
from sentry.testutils import TestCase

from fixtures import EXAMPLE_USERDATA_BELAVAGYOK, EXAMPLE_IDENTITY_BELAVAGYOK


class AuthSCHProviderTest(TestCase):
    def setUp(self):
        self.org = self.create_organization(owner=self.user)
        self.user = self.create_user('foo@example.com')
        self.auth_provider = AuthProvider.objects.create(
            provider='authsch',
            organization=self.org,
        )
        super(AuthSCHProviderTest, self).setUp()

    def test_building_identity(self):
        auth_identity = AuthIdentity.objects.create(
            auth_provider=self.auth_provider,
            user=self.user,
            data={'access_token': 'access_token', 'token_type': 'code'}
        )
        state = {
            'data': auth_identity.data,
            'user': EXAMPLE_USERDATA_BELAVAGYOK,
        }

        expected_identity = EXAMPLE_IDENTITY_BELAVAGYOK.copy()
        expected_identity['data'] = {'access_token': 'access_token', 'token_type': 'code'}

        provider = self.auth_provider.get_provider()

        assert expected_identity == provider.build_identity(state)

    def test_refresh_identity_without_refresh_token(self):
        auth_identity = AuthIdentity.objects.create(
            auth_provider=self.auth_provider,
            user=self.user,
            data={'access_token': 'access_token'}
        )

        provider = self.auth_provider.get_provider()

        with pytest.raises(IdentityNotValid):
            provider.refresh_identity(auth_identity)
