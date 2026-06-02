from django.utils.translation import get_language


def cms_globals(request):
    from .content_models import (
        BrandSettings,
        LocalizedMessage,
        MarketingAsset,
        OrganizationContacts,
    )

    lang_is_en = (get_language() or "ru").lower().startswith("en")
    msgs = LocalizedMessage.objects.all().values("key", "ru", "en")
    l10: dict[str, str] = {}
    for row in msgs:
        l10[row["key"]] = (row["en"] if lang_is_en and (row["en"] or "").strip() else row["ru"]) or ""

    ctx = {"L10": l10}

    org = OrganizationContacts.objects.filter(pk=1).first()
    if org:

        class _LocalizedOrg:
            def __init__(self, row):
                self._row = row
                self._en = lang_is_en

            @property
            def address_line(self):
                r = self._row
                return r.address_en if self._en and r.address_en else r.address_ru

            @property
            def weekday_hours(self):
                r = self._row
                return r.weekday_hours_en if self._en and r.weekday_hours_en else r.weekday_hours_ru

            @property
            def weekend_hours(self):
                r = self._row
                return r.weekend_hours_en if self._en and r.weekend_hours_en else r.weekend_hours_ru

            @property
            def chamber_line(self):
                r = self._row
                return r.chamber_line_en if self._en and r.chamber_line_en else r.chamber_line_ru

            @property
            def copyright_entity(self):
                r = self._row
                return r.company_short_title_en if self._en and r.company_short_title_en else r.company_short_title_ru

            @property
            def legal_name_line(self):
                r = self._row
                return r.legal_name_en if self._en and r.legal_name_en else r.legal_name_ru

            @property
            def phone_display(self):
                return self._row.phone_display

            @property
            def phone_href(self):
                return self._row.phone_href

            @property
            def email_display(self):
                return self._row.email_display

            @property
            def email_href(self):
                return self._row.email_href

            @property
            def inn(self):
                return self._row.inn

            @property
            def kpp(self):
                return self._row.kpp

            @property
            def ogrn(self):
                return self._row.ogrn

        ctx["org"] = _LocalizedOrg(org)

    brand_row = BrandSettings.objects.filter(pk=1).first()
    if brand_row:

        class _Brand:
            def __init__(self, row):
                self._row = row
                self._en = lang_is_en

            @property
            def brand_name(self):
                r = self._row
                return r.site_name_en if self._en and r.site_name_en else r.site_name_ru

            @property
            def header_tagline(self):
                r = self._row
                return r.header_tagline_en if self._en and r.header_tagline_en else r.header_tagline_ru

        ctx["brand"] = _Brand(brand_row)

    ctx["marketing_asset"] = MarketingAsset.objects.filter(pk=1).first()

    return ctx
