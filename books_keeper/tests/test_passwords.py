import sys
import os
address = os.environ.get("address")               # RUN IN DEBUG!!!
sys.path.append(address)                          # type: ignore
from user_manager import PasswordLogs             # type: ignore # noqa


assert PasswordLogs.validate_email("1,1@i") is False
assert PasswordLogs.validate_email("anonymous123@...uk") is False
assert PasswordLogs.validate_email("...@domain.us") is False
assert PasswordLogs.validate_email("anonymous123@yahoo.co.uk") is True
assert PasswordLogs.validate_email("name.surname@gmail.com") is True

assert PasswordLogs.validate_password("123") is False
assert PasswordLogs.validate_password("1234567890123456789012") is False
assert PasswordLogs.validate_password("_12fkG") is True
assert PasswordLogs.validate_password("5fk@#") is False
assert PasswordLogs.validate_password("sjn**") is True

assert type(PasswordLogs.u_hash("_12fkG")) == str
