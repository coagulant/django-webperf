Django Web Performance
======================

A collection of stuff to improve django web performance.

Domain sharding
---------------
`Domain sharding`_ is an optimization technique for parallelization of resource loading.
If you have a lot of media files on your page you might want them to be downloaded from
different domains, as web browsers have limits on how many files they can grab at once.
Domain sharding reduces the overall page load time and is widley used on rich media sites,
like Facebook, Youtube, etc.

It works as a customized `django file storage`_, overriding standard url method.

.. _domain sharding: http://www.stevesouders.com/blog/2009/05/12/sharding-dominant-domains/
.. _django file storage: https://docs.djangoproject.com/en/dev/ref/files/storage/

Installation & setup
--------------------

Recommended way to install is pip::

    pip install django-webperf


Make sure to change your ``DEFAULT_FILE_STORAGE`` in ``settings.py`` to use sharding site-wide::

    DEFAULT_FILE_STORAGE = 'web_performance.storage.DomainShardingStorage'

Settings
--------

WEBPERF_MEDIA_TEMPLATE
^^^^^^^^^^^^^^^^^^^^^^

:Default: ``''`` (empty string)

A pattern to generate media_urls with a standard format placeholder.
E.g. `http://img{0}.example.com/media/`

WEBPERF_DOMAINS_NUMBER
^^^^^^^^^^^^^^^^^^^^^^

:Default: ``2``

Number of domains you want to use to split your media content.

    Don't use too many domains, becasue it will increase DNS lookup time.
