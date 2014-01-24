django-model-gettext
====================

This is a small app that adds a mixin for adding translations to Django models.
When a model is saved, the fields can be written into a .po file, ready for
translation along with the rest of the site.

Unlike other model translation approaches, this application does not
require any schema migrations. It allows translators access to the
translation strings, without requiring access to the admin site in order to
directly edit the model data.


Quickstart
----------

To use this app, simply import the Mixin into the models.py file that
requires it and then add the Mixin to the required models.

Then add the name of the po file you want to use into the MODEL_GETTEXT_POFILE
setting in your settings.py file. E.g:

  MODEL_GETTEXT_POFILE = 'models.po'

By default the CharField and TextField types will get translation entries. This
can be overridden by setting MODEL_GETTEXT_TYPES in settings.py. E.g.

  MODEL_GETTEXT_TYPES = ['CharField',]


Use with django-rosetta
-----------------------

By default, django-rosetta only uses the django.po and djangojs.po files.
As of writing, the develop branch of django-rosetta allows this to be changed
by setting ROSETTA_POFILENAMES in settings.py
