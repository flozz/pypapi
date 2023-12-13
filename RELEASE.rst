Things to do when releasing a new version
=========================================

This file is a memo for the maintainer.


1. Release
----------

* Update version number in ``setup.py``
* Edit / update changelog in ``README.rst``
* Commit / tag (``git commit -m vX.Y.Z.ZZ && git tag vX.Y.Z.ZZ && git push && git push --tags``)


2. Publish PyPI package
-----------------------

Publish source dist and wheels on PyPI.

→ Automated :)


3. Publish Github Release
-------------------------

* Make a release on Github
* Add changelog
