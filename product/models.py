from django.db import models
from django.contrib.auth.models import AbstractUser, User
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


ICONS = (
    ('R', 'Run & Drive'),
    ('C', 'Seller Certified'),
    ('E', 'Enhanced Vehicle'),
    ('C', 'CrashedToys'),
    ('S', 'Engine Start Program'),
    ('F', 'Featured Vehicle'),
    ('O', 'Offsite Sales'),
    ('D', 'Donated Vehicle'),
    ('Q', 'Carb Qualification'),
    ('B', 'Sealed Bid Repossession'),
    ('V', 'VIX'),
    ('F', 'FAST'),
    ('H', 'Hybrid Vehicles'),
    # ('A', 'www.driveautoauctions.com'),
)

ICONS_DICT = {
    'Run & Drive': 'R',             # 'lcd'
    'RUNS AND DRIVES': 'R',         # 'lcd'
    'ENHANCED VEHICLES': 'E',       # 'lcd'
    'ENGINE START PROGRAM': 'S',    # 'lcd'
    'FEATURED': 'F',                # 'lic'
    'OFS': 'O',                     # 'lic'
    'DONA': 'D',                    # 'lic'
    'S-RENT': 'B',                  # 'lic'
    # 'SITE-DR': 'A',                 # 'lic' -> https://www.driveautoauctions.com/lot/
}

# Featured Items
# Buy It Now                buy_today_bid != 0
# No License Required
# Pure Sale Items           bid_status = PURE SALE
# Hot Items
# New Items                 items added last week
# Lots with Bids            current_bid != 0
# No Bids Yet               current_bid == 0
# Sealed Bid (7)

# Hybrid Vehicles           'H'
# Repossessions             'B'
# Donations                 'D'
# Featured Vehicles         'F'
# Offsite Sales             'O'
# Run and Drive             'R'

# Clean Title               doc_type_td not contains salvage
# Salvage Title             doc_type_td contains salvage
# Front End                 lot_1st_damage == "Front End" or lot_2nd_damage == "Front End"
# Hail Damage               lot_1st_damage == "Hail" or lot_2nd_damage == "Hail"
# Normal Wear
# Minor Dents/Scratch...
# Water/Flood
# Fleet / Lease             'std' = FLEET SELLER

# Classics
# Exotics
# Impound Vehicles (48)
# Municipal Fleet (67)
# Non-repairable (6,507)
# Recovered Thefts (2,472)
# Rentals (481)


TYPES = (
    ('A', 'ATV'),
    ('V', 'Automobile'),
    ('M', 'Boat'),
    ('D', 'Dirt Bike'),
    ('U', 'Heavy Duty Trucks'),
    ('E', 'Industrial Equipment'),
    ('J', 'Jet Ski'),
    ('K', 'Medium Duty/Box Trucks'),
    ('C', 'Motorcycle'),
    ('R', 'Recreational Vehicle (RV)'),
    ('S', 'Snowmobile'),
    ('L', 'Trailers'),
)
class VehicleMakes(models.Model):
    type = models.CharField(_('Type'), choices=TYPES, max_length=1, default='V')
    code = models.CharField(_('Code'), max_length=4)
    description = models.CharField(_('Description'), max_length=30)

    class Meta:
        verbose_name = _('Make')
        verbose_name_plural = _('Makes')
        ordering = ['type', 'description']

    def __str__(self):
        return dict(TYPES)[self.type] + '-' + self.description

    def scrap_link(self):
        scrap_link = '<a href="/scrap_copart/?id={id}">Scrap {description}</a>'.format
        return mark_safe(scrap_link(id=self.id, description=self.description))


FILTER_TYPES = (
    ('F', 'Featured Items'),
    ('T', 'Vehicle Types'),
    ('M', 'Makes'),
)
class Filter(models.Model):
    name = models.CharField(_('Filter Name'), max_length=50)
    count = models.IntegerField(_('Lots Number'), default=0)
    type = models.CharField(_('Filter Type'), choices=FILTER_TYPES, max_length=1)

    class Meta:
        verbose_name = _('Lots per Filter')
        verbose_name_plural = _('Lots per Filter')
        ordering = ['pk']


SOURCE = (
    ('C', 'Copart'),
    ('I', 'IAAI'),
)
class VehicleBase(models.Model):
    lot = models.IntegerField(_('Lot'))
    vin = models.CharField(_('VIN'), max_length=17, default='')

    # General Information
    name = models.CharField(_('Name'), max_length=255, default='')
    type = models.CharField(_('Type'), choices=TYPES, max_length=1, default='V')
    make = models.CharField(_('Make'), max_length=50, default='')
    model = models.CharField(_('Model'), max_length=50, default='')
    year = models.IntegerField(_('Year'), null=True, blank=True)
    currency = models.CharField(_('Currency'), max_length=3, default='')
    avatar = models.URLField(_('Avatar'), null=True, blank=True)
    source = models.BooleanField(_('Source'), default=True)
    # source = models.CharField(_('Source'), choices=SOURCE, max_length=1, default='C')

    # Lot Information
    doc_type_ts = models.CharField(_('Doc Type TS'), max_length=2, default='')
    doc_type_stt = models.CharField(_('Doc Type STT'), max_length=2, default='')
    doc_type_td = models.CharField(_('Doc Type TD'), max_length=100, default='')
    odometer_orr = models.IntegerField(_('Odometer ORR'), default=0)
    odometer_ord = models.CharField(_('Odometer ORD'), max_length=50, default='')
    lot_highlights = models.CharField(_('Highlights'), max_length=50, null=True, blank=True)
    lot_seller = models.CharField(_('Seller'), max_length=100, null=True, blank=True)
    lot_1st_damage = models.CharField(_('Primary Damage'), max_length=30, null=True, blank=True)
    lot_2nd_damage = models.CharField(_('Secondary Damage'), max_length=30, null=True, blank=True)
    retail_value = models.IntegerField(_('Est. Retail Value'), default=0)

    # Features
    body_style = models.CharField(_('Body Style'), max_length=50, null=True, blank=True)
    color = models.CharField(_('Color'), max_length=50, null=True, blank=True)
    engine_type = models.CharField(_('Engine Type'), max_length=50, null=True, blank=True)
    cylinders = models.CharField(_('Cylinders'), max_length=50, null=True, blank=True)
    transmission = models.CharField(_('Transmission'), max_length=50, null=True, blank=True)
    drive = models.CharField(_('Drive'), max_length=50, null=True, blank=True)
    fuel = models.CharField(_('Fuel'), max_length=50, null=True, blank=True)
    keys = models.CharField(_('Keys'), max_length=20, null=True, blank=True)
    notes = models.TextField(_('Notes'), null=True, blank=True)

    # Bid Information
    bid_status = models.CharField(_('Bid Status'), max_length=30, default='')
    sale_status = models.CharField(_('Sale Status'), max_length=30, default='')
    current_bid = models.IntegerField(_('Current Bid'), default=0)
    buy_today_bid = models.IntegerField(_('Buy Today Bid'), default=0)
    sold_price = models.IntegerField(_('Sold Price'), default=0)

    # Sale Information
    location = models.CharField(_('Location'), max_length=50, default='')
    lane = models.CharField(_('Lane'), max_length=1, default='')
    item = models.CharField(_('Item'), max_length=20, default='')
    grid = models.CharField(_('Grid/Row'), max_length=5, default='')
    sale_date = models.DateTimeField(_('Sale Date'), null=True, blank=True)
    last_updated = models.DateTimeField(_('Last Updated'), null=True, blank=True)

    images = models.TextField(_('Image Urls'), null=True, blank=True)
    thumb_images = models.TextField(_('Thumbnail Image Urls'), null=True, blank=True)

    created_at = models.DateTimeField(verbose_name=_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name=_('Updated at'), auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.vin + ' ' + str(self.lot)

    def lot_(self):
        return mark_safe('<a href="https://www.copart.com/lot/' + str(self.lot) + '" target="_blank">' + str(self.lot) + '</a>')
    lot_.admin_order_field = 'lot'

    def odometer(self):
        return str(self.odometer_orr) + ' ' + (self.odometer_ord[0] if self.odometer_ord else '')
    odometer.admin_order_field = 'odometer_orr'

    def lane_row(self):
        if self.source:
            return self.lane + ' / ' + self.grid
        else:
            return self.lane
    lane_row.short_description = 'Lane / Row'

    def doc_type(self):
        if self.source:
            return self.doc_type_stt + ' - ' + self.doc_type_ts
        else:
            return self.doc_type_td

    def est_retail_value(self):
        return '$' + str(self.retail_value) + ' ' + self.currency
    est_retail_value.short_description = 'Est. Retail Value'
    est_retail_value.admin_order_field = 'retail_value'

    def current_bid_(self):
        return '$' + str(self.current_bid) + ' ' + self.currency
    current_bid_.admin_order_field = 'current_bid'

    def sold_price_(self):
        return '$' + str(self.sold_price) + ' ' + self.currency
    sold_price_.admin_order_field = 'sold_price'

    def avatar_img(self):
        # return mark_safe('<a id="lot-images_{lot}"><img src="{url}" title="{title}" width="96" height="72"></a>'
        #                  .format(lot=self.lot, url=self.avatar, title=self.name))
        return mark_safe('<img src="{url}" title="{title}" width="96" height="72">'
                         .format(lot=self.lot, url=self.avatar, title=self.name))
    avatar_img.short_description = 'Avatar'

    def source_(self):
        return 'copart' if self.source else 'iaai'
    source_.admin_order_field = 'source'

    def images_(self):
        if self.source:
            images = ['https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + a for a in self.images.split('|')]
        else:
            images = ['https://vis.iaai.com:443/resizer?imageKeys=%s&width=640&height=480' % a for a in self.images.split('|')]
        return mark_safe('<br>'.join(['<a href="' + a + '">' + a + '</a>' for a in images]))
    images_.short_description = 'Image Urls'

    def thumb_images_(self):
        if self.source:
            images = ['https://cs.copart.com/v1/AUTH_svc.pdoc00001/' + a for a in self.thumb_images.split('|')]
        else:
            images = ['https://vis.iaai.com:443/resizer?imageKeys=%s&width=128&height=96' % a for a in self.thumb_images.split('|')]
        return mark_safe('<br>'.join(['<a href="' + a + '">' + a + '</a>' for a in images]))
    thumb_images_.short_description = 'Thumbnail Image Urls'


class Vehicle(VehicleBase):
    class Meta:
        verbose_name = _('Vehicle')
        verbose_name_plural = _('Vehicles')


class VehicleSold(VehicleBase):
    class Meta:
        verbose_name = _('Vehicle Sold')
        verbose_name_plural = _('Vehicles Sold')


class Foregoing(models.Model):
    parent_lot_id = models.IntegerField(_('Lot'))
    foregoing_lot = models.ForeignKey(VehicleSold, verbose_name=_('Foregoing'),
                                      related_name='foregoing_vehicle', on_delete=models.CASCADE)
    sold = models.BooleanField(_('Sold'))


class Location(models.Model):
    location = models.CharField(_('Location'), max_length=50, default='')
    count = models.IntegerField(_('Lots Number'), default=0)
    source = models.CharField(_('Source'), choices=SOURCE, max_length=1, default='C')

    class Meta:
        verbose_name = _('Location')
        verbose_name_plural = _('Locations')
        ordering = ['pk']

    def __str__(self):
        return self.source + '-' + self.location
