django-model-gettext
====================

This is a small app that adds a mixin for adding translations to Django models.
When a model is saved, the fields can be written into a .po file, ready for
translation along with the rest of the site.

Unlike other model translation approaches, this application does not
require any schema migrations. It allows translators access to the
translation strings, without requiring access to the admin site in order to
directly edit the model data.

