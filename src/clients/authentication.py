import base64
import datetime
import hashlib
import random
from typing import Dict

from exceptions.p2p_exception import P2PException


class Authentication:
    def __init__(self, config: Dict):
        """
        Initialize Authentication with the necessary configuration.

        :param config: Dictionary containing 'login' and 'tranKey'.
        """
        if "login" not in config or "tranKey" not in config:
            raise P2PException.for_data_not_provided("No login or tranKey provided for authentication")

        self.login: str = config["login"]
        self.tran_key: str = config["tranKey"]
        self.algorithm: str = config.get("algorithm", "sha256")
        self.auth: Dict = config.get("auth", {})
        self.additional: Dict = config.get("authAdditional", {})

        self.generate()

    def get_nonce(self) -> str:
        """
        Generate or retrieve the nonce.

        :param encoded: If True, returns the nonce base64 encoded.
        """
        if self.auth:
            return self.auth["nonce"]
        else:
            nonce = random.randrange(1000000, 10000000).to_bytes(16, byteorder="big")
            return base64.b64encode(nonce).decode("utf-8")

    def get_seed(self) -> str:
        """
        Generate or retrieve the seed (timestamp).

        :return: ISO formatted timestamp.
        """

        return self.auth.get("seed", datetime.datetime.now(datetime.timezone.utc).isoformat())

    def digest(self, encoded: bool = True) -> str:
        """
        Generate the digest based on nonce, seed, and tranKey.

        :param encoded: If True, returns the digest base64 encoded.
        :return: Digest string.
        """
        nonce = self.get_nonce()
        seed = self.get_seed()
        digest_input = nonce + seed + self.tran_key
        digest = hashlib.new(self.algorithm, digest_input.encode("utf-8")).digest()

        return base64.b64encode(digest).decode("utf-8") if encoded else digest

    def generate(self) -> None:
        """
        Generate the authentication data if not overridden.
        """
        self.auth = {
            "seed": self.get_seed(),
            "nonce": self.get_nonce(),
        }

    def as_dict(self) -> Dict:
        """
        Return the authentication data as a dictionary.

        :return: Authentication dictionary.
        """
        return {
            "login": self.login,
            "tranKey": self.digest(),
            "nonce": self.get_nonce(),
            "seed": self.get_seed(),
            "additional": self.additional,
        }
