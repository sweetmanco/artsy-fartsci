from setuptools import find_packages
from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='artsyfartsci',
      version="0.0.12",
      description="Art Similarity Model (api_pred)",
      author="molpl",
      author_email="contact@lewagon.org",
      install_requires=requirements,
      packages=find_packages(),
      # include_package_data: to install data from MANIFEST.in
      include_package_data=True,
      zip_safe=False)
