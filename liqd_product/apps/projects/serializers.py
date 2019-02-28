from functools import lru_cache

from django.utils import timezone
from django.utils.translation import ugettext as _
from easy_thumbnails.files import get_thumbnailer
from rest_framework import serializers

from adhocracy4.phases.models import Phase
from adhocracy4.projects.models import Project
from liqd_product.apps.projects import get_project_type


class CommonFields:

    def get_district(self, instance):
        city_wide = _('City wide')
        district_name = str(city_wide)
        if instance.administrative_district:
            district_name = instance.administrative_district.name
        return district_name

    def get_point(self, instance):
        point = instance.point
        if not point:
            point = ''
        return point

    def get_organisation(self, instance):
        return instance.organisation.name

    def get_created_or_modified(self, instance):
        if instance.modified:
            return str(instance.modified)
        return str(instance.created)


class ProjectSerializer(serializers.ModelSerializer, CommonFields):
    type = serializers.SerializerMethodField()
    subtype = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    point = serializers.SerializerMethodField()
    point_label = serializers.SerializerMethodField()
    cost = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    participation = serializers.SerializerMethodField()
    participation_display = serializers.SerializerMethodField()
    participation_active = serializers.SerializerMethodField()
    participation_string = serializers.SerializerMethodField()
    future_phase = serializers.SerializerMethodField()
    active_phase = serializers.SerializerMethodField()
    past_phase = serializers.SerializerMethodField()
    tile_image = serializers.SerializerMethodField()
    tile_image_copyright = serializers.SerializerMethodField()
    plan_url = serializers.SerializerMethodField()
    plan_title = serializers.SerializerMethodField()
    published_projects_count = serializers.SerializerMethodField()
    created_or_modified = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        self.now = kwargs.pop('now')
        super().__init__(args, kwargs)

    class Meta:
        model = Project
        fields = ['type', 'subtype', 'title', 'url',
                  'organisation', 'tile_image',
                  'tile_image_copyright',
                  'point', 'point_label', 'cost',
                  'district', 'topics', 'is_public',
                  'status',
                  'participation_string',
                  'participation_active',
                  'participation', 'participation_display', 'description',
                  'future_phase', 'active_phase',
                  'past_phase', 'plan_url', 'plan_title',
                  'published_projects_count', 'created_or_modified']

    @lru_cache(maxsize=1)
    def _get_participation_status_project(self, instance):
        if hasattr(instance, 'projectcontainer') and instance.projectcontainer:
            if instance.projectcontainer.active_project_count > 0:
                return _('running'), True
            elif instance.projectcontainer.future_project_count > 0:
                return _('starts in the future'), True
            else:
                return _('done'), False
        else:
            project_phases = instance.phases

            if project_phases.active_phases():
                return _('running'), True

            if project_phases.future_phases():
                try:
                    return (_('starts at {}').format
                            (project_phases.future_phases().first().
                             start_date.date().strftime('%d.%m.%Y')),
                            True)
                except AttributeError as e:
                    print(e)
                    return (_('starts in the future'),
                            True)
            else:
                return _('done'), False

    def get_type(self, instance):
        return 'project'

    def get_subtype(self, instance):
        subtype = get_project_type(instance)
        if subtype in ('external', 'bplan'):
            return 'external'
        return subtype

    def get_title(self, instance):
        return instance.name

    def get_url(self, instance):
        if get_project_type(instance) in ('external', 'bplan'):
            return instance.externalproject.url
        return instance.get_absolute_url()

    def get_tile_image(self, instance):
        image_url = ''
        if instance.tile_image:
            image = get_thumbnailer(instance.tile_image)['project_tile']
            image_url = image.url
        elif instance.image:
            image = get_thumbnailer(instance.image)['project_tile']
            image_url = image.url
        return image_url

    def get_tile_image_copyright(self, instance):
        if instance.tile_image:
            return instance.tile_image_copyright
        elif instance.image:
            return instance.image_copyright
        else:
            return None

    def get_status(self, instance):
        project_phases = instance.phases
        if project_phases.active_phases() or project_phases.future_phases():
            return 0
        return 1

    def get_participation(self, instance):
        return 0

    def get_participation_display(self, instance):
        return _('Yes')

    def get_future_phase(self, instance):
        if (instance.future_phases and
                instance.future_phases.first().start_date):
            return str(
                instance.future_phases.first().start_date.date())
        return False

    def get_active_phase(self, instance):
        if instance.active_phase:
            progress = instance.active_phase_progress
            time_left = instance.time_left
            end_date = str(instance.active_phase.end_date)
            return [progress, time_left, end_date]
        return False

    def get_past_phase(self, instance):
        project_phases = instance.phases
        if (project_phases.past_phases() and
                project_phases.past_phases().first().end_date):
            return str(
                project_phases.past_phases().first().end_date.date())
        return False

    def get_participation_string(self, instance):
        participation_string, participation_active = \
            self._get_participation_status_project(instance)
        return str(participation_string)

    def get_participation_active(self, instance):
        participation_string, participation_active = \
            self._get_participation_status_project(instance)
        return participation_active

    def get_plan_url(self, instance):
        if instance.plans.exists():
            return instance.plans.first().get_absolute_url()
        return None

    def get_plan_title(self, instance):
        if instance.plans.exists():
            return instance.plans.first().title
        return None

    def get_published_projects_count(self, instance):
        return 0

    def get_point_label(self, instance):
        return ''

    def get_cost(self, instance):
        return ''


class ActiveProjectSerializer(ProjectSerializer):

    def active_phases(self):
        return Phase.objects\
            .filter(start_date__lte=self.now,
                    end_date__gt=self.now)\
            .order_by('start_date')

    def seconds_in_units(self, seconds):
        unit_totals = []

        unit_limits = [
            ([_('day'), _('days')], 24 * 3600),
            ([_('hour'), _('hours')], 3600),
            ([_('minute'), _('minutes')], 60)
        ]

        for unit_name, limit in unit_limits:
            if seconds >= limit:
                amount = int(float(seconds) / limit)
                if amount > 1:
                    unit_totals.append((unit_name[1], amount))
                else:
                    unit_totals.append((unit_name[0], amount))
                seconds = seconds - (amount * limit)
        return unit_totals

    def get_active_phase(self, instance):
        active_phase = self.active_phases()\
            .filter(module__project=instance)\
            .last()
        time_gone = self.now - active_phase.start_date
        total_time = active_phase.end_date - active_phase.start_date
        progress = (time_gone / total_time * 100)

        time_delta = active_phase.end_date - self.now
        seconds = time_delta.total_seconds()
        time_delta_list = self.seconds_in_units(seconds)
        best_unit = time_delta_list[0]
        time_left = '{} {}'.format(str(best_unit[1]), str(best_unit[0]))
        end_date = str(active_phase.end_date)
        return [progress, time_left, end_date]

    def get_status(self, instance):
        return 0

    def get_future_phase(self, instance):
        return False

    def get_past_phase(self, instance):
        return False

    def get_participation_string(self, instance):
        return _('running')

    def get_participation_active(self, instance):
        return True


class FutureProjectSerializer(ProjectSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._future_phases = Phase.objects\
            .filter(start_date__gt=self.now)\
            .order_by('start_date')

    def get_active_phase(self, instance):
        return False

    def get_status(self, instance):
        return 0

    def get_future_phase(self, instance):
        future_phase = self._future_phases\
            .filter(module__project=instance)\
            .first()
        return str(future_phase.start_date.date())

    def get_past_phase(self, instance):
        return False

    def get_participation_string(self, instance):
        return _('starts in the future')

    def get_participation_active(self, instance):
        return True


class PastProjectSerializer(ProjectSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._past_phases = Phase.objects\
            .filter(end_date__lt=timezone.now())\
            .order_by('start_date')

    def get_active_phase(self, instance):
        return False

    def get_status(self, instance):
        return 1

    def get_future_phase(self, instance):
        return False

    def get_past_phase(self, instance):
        past_phase = self._past_phases.filter(module__project=instance).first()
        return str(past_phase.end_date.date())

    def get_participation_string(self, instance):
        return _('done')

    def get_participation_active(self, instance):
        return False