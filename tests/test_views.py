from __future__ import absolute_import

from mock.mock import MagicMock

from sentry.models import AuthProvider
from sentry.testutils import TestCase

from sentry_auth_authsch.constants import DATA_VERSION
from sentry_auth_authsch.views import FetchUser

from fixtures import EXAMPLE_USERPROFILE_BELAVAGYOK, EXAMPLE_USERDATA_BELAVAGYOK


class AuthSCHFetchUserTest(TestCase):
    def setUp(self):
        self.org = self.create_organization(owner=self.user)
        self.user = self.create_user('foo@example.com')
        self.auth_provider = AuthProvider.objects.create(
            provider='authsch',
            organization=self.org,
        )

        self.fetchuser = FetchUser(version=DATA_VERSION)
        self.fetchuser.get_user_profile = MagicMock(return_value=EXAMPLE_USERPROFILE_BELAVAGYOK.copy())

        super(AuthSCHFetchUserTest, self).setUp()

    def test_dispatch_happy_path(self):
        helper = MagicMock()
        request = MagicMock()

        self.fetchuser.dispatch(helper=helper, request=request)

        self.fetchuser.get_user_profile.assert_called_once()
        helper.bind_state.assert_called_with('user', EXAMPLE_USERDATA_BELAVAGYOK)
        helper.next_step.assert_called_once()

    def test_dispatch_bad_response_1(self):
        helper = MagicMock()
        request = MagicMock()
        self.fetchuser.get_user_profile.side_effect = Exception()

        self.fetchuser.dispatch(helper=helper, request=request)

        assert not helper.next_step.called

    def test_dispatch_bad_response_2(self):
        helper = MagicMock()
        request = MagicMock()
        self.fetchuser.populate_userdata = MagicMock(side_effect=Exception())

        self.fetchuser.dispatch(helper=helper, request=request)

        assert not helper.next_step.called


class AuthSCHFetchUserUserDataTest(AuthSCHFetchUserTest):
    def setUp(self):
        super(AuthSCHFetchUserUserDataTest, self).setUp()
        self.userdata = self.fetchuser.populate_userdata(EXAMPLE_USERPROFILE_BELAVAGYOK.copy())

    def test_populating_userdata_raw_profile_is_intact(self):
        assert self.userdata['raw_profile'] == EXAMPLE_USERPROFILE_BELAVAGYOK

    def test_populating_userdata_schacc(self):
        assert self.userdata['schacc'] == "belavagyok"

    def test_populating_userdata_iid(self):
        assert self.userdata['iid'] == "9DA3D9BE04CDFD26CB87BAF34B0367F8"

    def test_populating_userdata_schmail(self):
        assert self.userdata['schmail'] == "belavagyok@sch.bme.hu"

    def test_populating_userdata_secondary_mail(self):
        assert self.userdata['secondary_mail'] == "bela@tesztel.ek"

    def test_populating_userdata_full_name(self):
        assert self.userdata['full_name'] == "Teszt Bela"
