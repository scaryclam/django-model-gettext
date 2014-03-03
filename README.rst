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

Then add the top level directory that you wish to use into the MODEL_GETTEXT_LOCALE
setting in your settings.py file. E.g:

  MODEL_GETTEXT_LOCALE = 'models_locale'

You will also need to set this directory in Django's LOCALE_PATHS:

  LOCALE_PATHS = (
      ...
      os.path.join('/path/to/directory/', MODEL_GETTEXT_LOCALE),
  )

By default the CharField and TextField types will get translation entries. This
can be overridden by setting MODEL_GETTEXT_TYPES in settings.py. E.g.

  MODEL_GETTEXT_TYPES = ['CharField',]

Currently, the project level locale directory is used, so it should be present
for this app to work!


Use with django-rosetta
-----------------------

Django rosetta should work with this library out of the box.

