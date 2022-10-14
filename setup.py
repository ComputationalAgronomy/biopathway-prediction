import setuptools

import site

if __name__ == "__main__":
    # https://github.com/pypa/pip/issues/7953
    site.ENABLE_USER_SITE = 1

    setuptools.setup()
