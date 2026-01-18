from dataclasses import dataclass, field

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


@dataclass
class Argon2:
    """
    Argon2 Flask integration helper.
    This class wraps argon2-cffi's PasswordHasher and provides a simple,
    Flask-friendly interface to configure, initialize, and use Argon2 password
    hashing within a Flask application.
    Usage
    - Create an Argon2 instance (defaults are chosen for reasonable security).
    - Call init_app(app) to read optional Flask config overrides and attach the
        initialized Argon2 instance to app.extensions["argon2"].
    - Use generate_hash_password(password) to create a password hash.
    - Use check_has_password(hash, password) to verify a password against a hash.
    Configuration (Flask app.config)
    - ARGON2_TIME_COST (int): Number of iterations (default: 3). Minimum: 2.
    - ARGON2_MEMORY_COST (int): Memory usage in KiB (default: 64 * 1024, i.e. 64 MiB).
        Minimum: 32 * 1024 (32 MiB).
    - ARGON2_PARALLELISM (int): Degree of parallelism (default: 4). Minimum: 1.
    - ARGON2_HASH_LEN (int): Length of the generated hash in bytes (default: 32).
        Minimum: 16.
    - ARGON2_SALT_LEN (int): Salt length in bytes (default: 16). Minimum: 16.
    Attributes
    - time_cost (int): Argon2 time cost parameter.
    - memory_cost (int): Argon2 memory cost parameter (in KiB).
    - parallelism (int): Argon2 parallelism parameter.
    - hash_len (int): Length of produced hash in bytes.
    - salt_len (int): Salt length in bytes.
    - ph (PasswordHasher | None): Underlying argon2-cffi PasswordHasher instance
        after initialization; None (or falsy) before init_app() is called.
    Behavior and errors
    - init_app(app): Reads configuration overrides from the Flask app, validates
        parameters, initializes the PasswordHasher, and stores this Argon2 object in
        app.extensions["argon2"]. Raises ValueError if any parameter is below the
        documented minimums.
    - generate_hash_password(password): Returns an encoded Argon2 hash for the
        provided password. Raises RuntimeError if init_app() has not been called.
    - check_has_password(hash, password): Verifies a password against an encoded
        Argon2 hash. Returns True on successful verification, False if the password
        does not match. Raises RuntimeError if init_app() has not been called.
        Verification mismatches are handled and reported as False (does not raise).
    Notes
    - The underlying PasswordHasher is provided by argon2-cffi and must be
        available in the environment.
    - The class performs basic parameter validation to encourage secure defaults,
        but you should choose parameters appropriate to your deployment environment
        (available memory and required performance).
    """

    time_cost: int = 3
    memory_cost: int = 64 * 1024
    parallelism: int = 4
    hash_len: int = 32
    salt_len: int = 16

    ph: PasswordHasher | None = field(init=False, default=False)

    def _validate(self) -> None:
        if self.time_cost < 2:
            raise ValueError("Argon2 time_cost is insecure (minimum 2)")
        if self.memory_cost < 32 * 1024:
            raise ValueError("Argon2 memory_cost is insecure (minimum 32MB)")
        if self.parallelism < 1:
            raise ValueError("Argon2 parallelism is invalid")
        if self.hash_len < 16:
            raise ValueError("Argon2 hash_len is insecure")
        if self.salt_len < 16:
            raise ValueError("Argon2 salt_len is insecure")

    def init_app(self, app) -> None:
        " Initialize Argon2 with Flask app configuration."
        
        config_map = {
            "time_cost": "ARGON2_TIME_COST",
            "memory_cost": "ARGON2_MEMORY_COST",
            "parallelism": "ARGON2_PARALLELISM",
            "hash_len": "ARGON2_HASH_LEN",
            "salt_len": "ARGON2_SALT_LEN",
        }

        for attr, key in config_map.items():
            setattr(self, attr, app.config.get(key, getattr(self, attr)))

        self._validate()

        self.ph = PasswordHasher(
            time_cost=self.time_cost,
            memory_cost=self.memory_cost,
            parallelism=self.parallelism,
            hash_len=self.hash_len,
            salt_len=self.salt_len,
        )
        
        app.extensions["argon2"] = self


    def generate_hash_password(self, password: str) -> str:
        if self.ph is None:
            raise RuntimeError("Argon2 is not initialized. Call init_app() first")
        return self.ph.hash(password)

    def check_hash_password(self, hash: str, password: str) -> bool:
        if self.ph is None:
            raise RuntimeError("Argon2 is not initialized. Call init_app() first")
        try:
            return self.ph.verify(hash, password)
        except VerifyMismatchError:
            return False
