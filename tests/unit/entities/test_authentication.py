import unittest, hashlib, base64, pytest
from exceptions.p2p_exception import P2PException
from unittest import mock
from client.authentication import Authentication


class AuthenticationTest(unittest.TestCase):

    @mock.patch("client.authentication.random.randrange")
    @mock.patch("client.authentication.datetime")
    def test_authentication_initialitation(self, mock_datetime, mock_randrange):
        mock_now = mock.Mock()
        mock_now.isoformat.return_value = "2024-10-22T04:39:18.810868+00:00"
        mock_datetime.datetime.now.return_value = mock_now
        mock_datetime.timezone.utc = mock.Mock()
        mock_randrange.return_value = 927342197

        config = {
            "login": "test_login",
            "tranKey": "test_tran_key",
        }
        auth = Authentication(config)

        digest_input = auth.auth["nonce"] + auth.auth["seed"] + auth.tran_key
        digest = hashlib.new(auth.algorithm, digest_input.encode("utf-8")).digest()

        expect_digets = base64.b64encode(digest).decode("utf-8")
        expect_seed = "2024-10-22T04:39:18.810868+00:00"
        expect_nonce = "AAAAAAAAAAAAAAAAN0YedQ=="
        expect_login = "test_login"
        expect_trankey = "test_tran_key"

        assert auth.get_seed() == expect_seed
        assert auth.digest() == expect_digets
        assert auth.auth["seed"] == expect_seed
        assert auth.auth["nonce"] == expect_nonce
        assert auth.algorithm == "sha256"
        assert auth.login == expect_login
        assert auth.tran_key == expect_trankey
        assert auth.additional == {}

        expected_dict = {
            "login": expect_login,
            "tranKey": expect_digets,
            "nonce": expect_nonce,
            "seed": expect_seed,
            "additional": {},
        }
        assert auth.as_dict() == expected_dict

    def test_fails_not_login_and_tran_key_provider(self):
        with pytest.raises(P2PException) as exc_info:
            Authentication({})

        assert str(exc_info.value) == "No login or tranKey provided for authentication"
