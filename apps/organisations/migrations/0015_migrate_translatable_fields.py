# Generated by Django 2.2.13 on 2020-07-07 06:21

from django.db import migrations
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist


def forwards_func(apps, schema_editor):
    MyModel = apps.get_model('a4_candy_organisations', 'Organisation')
    MyModelTranslation = apps.get_model('a4_candy_organisations', 'OrganisationTranslation')

    for object in MyModel.objects.all():
        MyModelTranslation.objects.create(
            master_id=object.pk,
            language_code=settings.DEFAULT_USER_LANGUAGE_CODE,
            description=object.description_untranslated,
            slogan = object.slogan_untranslated,
            information = object.information_untranslated
        )

def backwards_func(apps, schema_editor):
    MyModel = apps.get_model('a4_candy_organisations', 'Organisation')
    MyModelTranslation = apps.get_model('a4_candy_organisations', 'OrganisationTranslation')

    for object in MyModel.objects.all():
        translation = _get_translation(object, MyModelTranslation)
        object.description_untranslated = translation.description
        object.slogan_untranslated = translation.slogan
        object.information_untranslated = translation.information
        object.save()   # Note this only calls Model.save()

def _get_translation(object, MyModelTranslation):
    translations = MyModelTranslation.objects.filter(master_id=object.pk)
    try:
        # Try default translation
        return translations.get(language_code=settings.DEFAULT_USER_LANGUAGE_CODE)
    except ObjectDoesNotExist:
        try:
            # Try default language
            return translations.get(language_code=settings.LANGUAGE_CODE)
        except ObjectDoesNotExist:
            # Maybe the object was translated only in a specific language?
            # Hope there is a single translation
            return translations.get()


class Migration(migrations.Migration):

    dependencies = [
        ('a4_candy_organisations', '0014_add_translatable_fields_and_rename_old_fields'),
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]
