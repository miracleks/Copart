from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.utils.encoding import smart_text
from django.utils.http import urlencode
from django.utils.translation import ugettext_lazy as _

from product.models import *


class MultipleChangeList(ChangeList):
    def get_query_string(self, new_params=None, remove=None):
        if new_params is None: new_params = {}
        if remove is None: remove = []
        p = self.params.copy()
        for r in remove:
            for k in list(p):
                if k.startswith(r):
                    del p[k]
        for k, v in new_params.items():
            if v is None:
                if k in p:
                    del p[k]
            else:
                if k in p and '__in' in k:
                    in_list = p[k].split(',')
                    if not v in in_list:
                        in_list.append(v)
                    else:
                        in_list.remove(v)
                    p[k] = ','.join(in_list)
                else:
                    p[k] = v
        return '?%s' % urlencode(sorted(p.items()))


class MultipleChoicesFieldListFilter(admin.ChoicesFieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super(MultipleChoicesFieldListFilter, self).__init__(field, request, params, model, model_admin, field_path)
        self.lookup_kwarg = '%s__in' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg)

    def choices(self, cl):
        yield {
            'selected': self.lookup_val is None,
            'query_string': cl.get_query_string({}, [self.lookup_kwarg]),
            'display': _('All')
        }
        for lookup, title in self.field.flatchoices:
            yield {
                'selected': smart_text(lookup) in str(self.lookup_val),
                'query_string': cl.get_query_string({self.lookup_kwarg: lookup}),
                'display': title,
            }


class DescriptionFilter(admin.SimpleListFilter):
    title = 'Description'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'description'

    def lookups(self, request, model_admin):
        descriptions = []
        if 'type__in' in request.GET:
            makes = VehicleMakes.objects.filter(type__in=request.GET['type__in'])
        else:
            makes = VehicleMakes.objects.all()

        for make in makes:
            descriptions.append((make.id, dict(TYPES)[make.type] + '-' + make.description))
        return descriptions

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        return queryset.filter(id=self.value())


class SourceFilter(admin.SimpleListFilter):
    title = _('Source')
    parameter_name = 'source'

    def lookups(self, request, model_admin):
        return (
            ('copart', _('Copart')),
            ('iaai', _('IAAI')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'copart':
            return queryset.filter(source=True)
        elif self.value() == 'iaai':
            return queryset.filter(source=False)
        return queryset


class SoldFilter(admin.SimpleListFilter):
    title = _('Sold Status')
    parameter_name = 'sold'

    def lookups(self, request, model_admin):
        return (
            ('exist', _('Not Sold')),
            ('sold', _('Sold Out')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'exist':
            return queryset.filter(sold_price=0)
        elif self.value() == 'sold':
            return queryset.filter(sold_price__gt=0)
        return queryset
