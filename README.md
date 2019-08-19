# MarkLogic client
*MarkLogic is a trademark of MarkLogic Corporation. We are not affiliated with MarkLogic Corporation.*

TODO: Write readme.

## How to use this in another Python project

Install using `pip`:
```bash
pip install git+https://github.com/quangis/marklogic_client.git@master
```

(TODO: Build releases and distribute them archived and versioned. This is much faster than using `git`.)


## How to run the tests

1. First, run the setup script:

```bash
./setup.sh
```
This will make a file, `.env`, where you'll have to fill in the credentials of the MarkLogic Server that you want to use.

2. Fill in the credentials:
   * `MARKLOGIC_URL`: Replace `{address}` and `{port}` with the correct address and port, and either remove `[s]` or replace it with `s`.
   * `MARKLOGIC_USERNAME`: Replace `{username}` with the username.
   * `MARKLOGIC_PASSWORD`: Replace `{password}` with the password.

3. Run the tests:
```bash
python setup.py pytest  # Or `python3 setup.py pytest` if `python` is version 2.
```


If all went well, you should see something along the lines of this:
```
running pytest
running egg_info
writing marklogic_client.egg-info/PKG-INFO
writing dependency_links to marklogic_client.egg-info/dependency_links.txt
writing requirements to marklogic_client.egg-info/requires.txt
writing top-level names to marklogic_client.egg-info/top_level.txt
reading manifest file 'marklogic_client.egg-info/SOURCES.txt'
writing manifest file 'marklogic_client.egg-info/SOURCES.txt'
running build_ext
============================= test session starts =============================
platform linux -- Python 3.6.8, pytest-5.0.1, py-1.8.0, pluggy-0.12.0
rootdir: /home/han/Projects/marklogic_client
collected 3 items                                                             

tests/test_marklogic_client.py ...                                      [100%]

========================== 3 passed in 0.38 seconds ===========================
```
