import sys
import os
address = os.environ.get("address")                     # RUN IN DEBUG!!!
sys.path.append(address)                                # type: ignore
from user_manager import PasswordLogs                 # type: ignore # noqa


assert PasswordLogs.validate_email("1,1@i") == False
assert PasswordLogs.validate_email("anonymous123@...uk") == False
assert PasswordLogs.validate_email("...@domain.us") == False
assert PasswordLogs.validate_email("anonymous123@yahoo.co.uk") == True
assert PasswordLogs.validate_email("name.surname@gmail.com") == True

assert PasswordLogs.validate_password("123") == False
assert PasswordLogs.validate_password("1234567890123456789012") == False
assert PasswordLogs.validate_password("_12fkG") == True
assert PasswordLogs.validate_password("5fk@#") == False
assert PasswordLogs.validate_password("sjn**") == True

assert type(PasswordLogs.u_hash("_12fkG")) == str
