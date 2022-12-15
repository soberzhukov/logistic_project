from common.filters import ObjectFilter
from offer.models import Offer


class OfferFilter(ObjectFilter):
    class Meta(ObjectFilter.Meta):
        model = Offer
