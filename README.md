# password_keychain
Terminal based password manager written in Python

## Setup
Only external library to install should be termcolor:

```
pip3 install termcolor
```
You will also need to create a database to store your password data. This can be done using SQLite DB Browser (https://sqlitebrowser.org). There should be one table named *data* with the following items:
| account | email | password | username | pin |
| ------- | ----- | -------- | -------- | --- |

Finally, you will need to store the SHA256 hash of your master password in file titled *master* in the appropriate key folder


Once set up, you can just run `python3 keychain.py`

![Not Maintained](https://img.shields.io/badge/Maintenance%20Level-Not%20Maintained-yellow.svg)
