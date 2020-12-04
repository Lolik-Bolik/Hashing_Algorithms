from setuptools import setup, find_packages

packages = find_packages(exclude=["tests*"])

package_data = {
    "": ["*"],
}

install_requires = ["pycrypto==2.6.1"]

setup_kwargs = {
    "name": "hashing-algorithms",
    "version": "0.1.0",
    "description": "Implementation and comparison of several hashing algorithms",
    "long_description": None,
    "author": "LolikBolik",
    "packages": packages,
    "package_data": package_data,
    "python_requires": ">=3.7,<4.0",
    "install_requires": install_requires,
}


setup(**setup_kwargs)
