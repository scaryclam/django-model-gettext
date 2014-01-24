import os
import polib

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class TransMixin(object):
    def save(self):
        super(TransMixin, self).save()
        self.update_translations()

    def update_translations(self):
        interesting_types = getattr(
            settings, 'MODEL_GETTEXT_TYPES', ['CharField', 'TextArea'])
        fields_to_translate = []
        for field in self._meta.get_fields_with_model():
            if field[0].get_internal_type() in interesting_types:
                fields_to_translate.append(field[0])
                print "Added field", field[0]
        self.create_po_entries(fields_to_translate)

    def get_pofile(self):
        try:
            pofile_path = settings.MODEL_GETTEXT_POFILE
        except AttributeError:
            raise ImproperlyConfigured(
                "MODEL_GETTEXT_POFILE is missing from the settings")
        if os.path.exists(pofile_path):
            pofile = polib.pofile(pofile_path)
        else:
            pofile = polib.POFile()
            pofile.metadata = {
                'Project-Id-Version': '1.0',
                'Report-Msgid-Bugs-To': 'someone@example.com',
                'POT-Creation-Date': '2007-10-18 14:00+0100',
                'PO-Revision-Date': '2007-10-18 14:00+0100',
                'Last-Translator': 'you <you@example.com>',
                'Language-Team': 'English <yourteam@example.com>',
                'MIME-Version': '1.0',
                'Content-Type': 'text/plain; charset=utf-8',
                'Content-Transfer-Encoding': '8bit',
            }
        return pofile

    def create_po_entries(self, fields_to_translate):
        pofile = self.get_pofile()
        for field in fields_to_translate:
            trans_value = getattr(self, field.name)
            entry = pofile.find(trans_value)
            if not entry:
                entry = polib.POEntry(
                    msgid=trans_value,
                    msgstr=u'',
                    occurrences=[])
                pofile.append(entry)
            else:
                # See if the entry text has changed
                if trans_value != entry.msgid:
                    # Replace it
                    entry.msgid = trans_value
                    entry.msgstr = u''
            pofile.save(settings.MODEL_GETTEXT_POFILE)
