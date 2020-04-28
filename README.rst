===============
Silence Remover
===============


.. image:: https://img.shields.io/pypi/v/av_slice.svg
        :target: https://pypi.python.org/pypi/av_slice

.. image:: https://img.shields.io/travis/Hixan/av_slice.svg
        :target: https://travis-ci.org/Hixan/av_slice

.. image:: https://readthedocs.org/projects/av-slice/badge/?version=latest
        :target: https://av-slice.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




An automated video editing tool that removes lengths of silence.


* Free software: MIT license
* Documentation: https://av-slice.readthedocs.io.

Important to note, I don't /really/ know what I'm doing in terms of a lot of the
packaging environment, so pull requests are very welcome.


Features
--------

* Automatically edit audio or video clips to remove silent or quiet sections

Installation
------------
Install with pip:

```
pip install av_slice
```

or clone and install from source:

```
git clone https://github.com/hixan/av_slice.git
cd av_slice
make install
```

Use
----
automatically remove silence from `video.mp4`:

```
python -m av_slice video.mp4 --output_file=shorter_video.mp4
```

the script will run for a while calculating changes and composing the video.
When it is finished, `shorter_video.mp4` will be saved to the disk. If
`--output_file` is omitted it will be saved to `video_modified.mp4`.

Credits
-------
Heavily inspired by Carkyhs Jumpcutter_ library.

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _Jumpcutter: https://github.com/carykh/jumpcutter

Todo
----

* testing (get a good example video)
* get ffmpeg installed on travis to enable proper testing
* GUI interface
* PY2EXE implementation?

Wishlist
--------
* automatic detection of appropriate threshold
