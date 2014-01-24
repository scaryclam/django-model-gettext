import os
import glob
import polib


from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class TransMixin(object):
    def save(self, *args, **kwargs):
        super(TransMixin, self).save(*args, **kwargs)
        self.update_translations()

    def update_translations(self):
        interesting_types = getattr(
            settings, 'MODEL_GETTEXT_TYPES', ['CharField', 'TextField'])
        fields_to_translate = []
        for field in self._meta.get_fields_with_model():
            if field[0].get_internal_type() in interesting_types:
                fields_to_translate.append(field[0])
                print "Added field", field[0]
        self.create_po_entries(fields_to_translate)

    def get_pofile(self):
        locale_dir = os.path.abspath('locale')
        locale_dirs = filter(os.path.isdir, glob.glob('%s/*' % locale_dir))

        pofile_locations = {}

        try:
            pofile_name = settings.MODEL_GETTEXT_POFILE
        except AttributeError:
            raise ImproperlyConfigured(
                "MODEL_GETTEXT_POFILE is missing from the settings")

        for pofile_dir in locale_dirs:
            pofile_path = os.path.join(pofile_dir, 'LC_MESSAGES', pofile_name)
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
                pofile.save
            pofile_locations[pofile_path] = pofile
        return pofile_locations

    def create_po_entries(self, fields_to_translate):
        pofiles = self.get_pofile()
        for pofile_path, pofile in pofiles.iteritems():
            for field in fields_to_translate:
                trans_value = getattr(self, field.name)
                entry = pofile.find(trans_value)
                if not entry:
                    entry = polib.POEntry(
                        msgid=trans_value,
                        msgstr=u'',
                        occurrences=[('table:%s' % self._meta.db_table,
                                      'pk:%s' % self.pk)])
                    pofile.append(entry)
                else:
                    # See if the entry text has changed
                    if trans_value != entry.msgid:
                        # Replace it
                        entry.msgid = trans_value
                        entry.msgstr = u''
                pofile.save(pofile_path)
