from mezzanine.conf import register_setting
from django.conf import settings

register_setting(
    name="WHOLESALE_MINIMUM_SPEND",
    label='Minimum wholesale spend',
    description="(&pound; Sterling)",
    editable=True,
    default="120.00",
)

register_setting(
    name="WHOLESALE_DELIVERY_COST",
    label='Wholesale delivery cost',
    description="(&pound; Sterling)",
    editable=True,
    default="00.00",
)

register_setting(
    name="UK_RETAIL_FREE_DELIVERY_MINIMUM",
    label='UK free delivery minimum spend',
    description="The amount a customer has to spend to get free delivery",
    editable=True,
    default=55.00,
)

register_setting(
    name="UK_DELIVERY_SLOW_RATE",
    label='UK First Class Delivery 3-5 days',
    description="",
    editable=True,
    default=3.95,
)

register_setting(
    name="UK_DELIVERY_FAST_RATE",
    label='UK Special Delivery 1-2 days',
    description="",
    editable=True,
    default=7.95,
)

register_setting(
    name="EUROPE_DELIVERY_SLOW_RATE",
    label='Europe Airmail Standard 4-6 Days',
    description="",
    editable=True,
    default=8.00,
)

register_setting(
    name="EUROPE_DELIVERY_FAST_RATE",
    label='Europe Airsure Recorded Delivery 3-5 Days',
    description="",
    editable=True,
    default=15.00,
)

register_setting(
    name="WORLD_DELIVERY_SLOW_RATE",
    label='World Airmail Standard 6-8 Days',
    description="",
    editable=True,
    default=9.00,
)

register_setting(
    name="WORLD_DELIVERY_FAST_RATE",
    label='World Airsure Recorded Delivery 5-7 Days',
    description="",
    editable=True,
    default=20.00,
)