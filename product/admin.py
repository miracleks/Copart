from django.contrib import admin
# from django.core.paginator import Paginator
# from django.db import connection

from product.models import *
from product.filters import DescriptionFilter, MultipleChoicesFieldListFilter, MultipleChangeList, SourceFilter, SoldFilter


# class LargeTablePaginator(Paginator):
#     """
#     Warning: Postgresql only hack
#     Overrides the count method of QuerySet objects to get an estimate instead of actual count when not filtered.
#     However, this estimate can be stale and hence not fit for situations where the count of objects actually matter.
#     """
#
#     def _get_count(self):
#         if getattr(self, '_count', None) is not None:
#             return self._count
#
#         query = self.object_list.query
#         if not query.where:
#             try:
#                 cursor = connection.cursor()
#                 cursor.execute("SELECT reltuples FROM pg_class WHERE relname = %s",
#                                [query.model._meta.db_table])
#                 self._count = int(cursor.fetchone()[0])
#             except:
#                 self._count = super(LargeTablePaginator, self)._get_count()
#         else:
#             self._count = super(LargeTablePaginator, self)._get_count()
#
#         return self._count
#
#     count = property(_get_count)


class VehicleMakesAdmin(admin.ModelAdmin):
    list_display = ['type', 'description', 'scrap_link']
    list_filter = (DescriptionFilter, ('type', MultipleChoicesFieldListFilter))
    search_fields = ['description']

    def get_changelist(self, request, **kwargs):
        return MultipleChangeList


class FilterAdmin(admin.ModelAdmin):
    list_display = ['name', 'count', 'type']


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['avatar_img', 'vin', 'lot_', 'year', 'make', 'model', 'est_retail_value',
                    'current_bid_', 'sold_price_', 'sale_date', 'odometer', 'lot_1st_damage', 'source_']

    list_display_links = ['vin']

    list_filter = [SourceFilter, SoldFilter, 'make']

    search_fields = ['name', 'vin', 'lot', 'year', 'make', 'model']

    readonly_fields = ['source_', 'images_', 'thumb_images_', 'created_at', 'updated_at']

    # paginator = LargeTablePaginator

    fieldsets = [
        ('', {'fields': ['vin', 'lot', 'type', 'name', 'make', 'model', 'year', 'location', 'source_']}),
        ('Lot', {'fields': ['doc_type_ts', 'doc_type_stt', 'doc_type_td', 'odometer_orr', 'odometer_ord',
                            'lot_highlights', 'lot_seller', 'lot_1st_damage', 'lot_2nd_damage', 'retail_value']}),
        ('Features', {'fields': ['body_style', 'color', 'engine_type', 'cylinders', 'transmission',
                                 'drive', 'fuel', 'keys', 'notes']}),
        ('Bid Information', {'fields': ['bid_status', 'sale_status', 'current_bid', 'buy_today_bid', 'sold_price', 'currency']}),
        ('Sale Information', {'fields': ['location', 'lane', 'item', 'grid', 'sale_date', 'last_updated']}),
        ('Images', {'fields': ['avatar', 'images_', 'thumb_images_']}),
        ('Dates', {'fields': ['created_at', 'updated_at']}),
    ]


class LocationAdmin(admin.ModelAdmin):
    list_filter = ['source']
    list_display = ['location', 'count', 'source']


class ForegoingAdmin(admin.ModelAdmin):
    list_filter = ['sold']
    search_fields = ['parent_lot_id']
    raw_id_fields = ['foregoing_lot']
    list_display = ['parent_lot_id', 'foregoing_lot', 'sold']


admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(VehicleSold, VehicleAdmin)
admin.site.register(VehicleMakes, VehicleMakesAdmin)
admin.site.register(Filter, FilterAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Foregoing, ForegoingAdmin)
