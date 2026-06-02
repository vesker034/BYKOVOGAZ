from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import get_language, gettext as _

from .forms import CandidateApplicationForm
from .models import (
    AboutExploreCard,
    CareerPageSettings,
    CandidateStatus,
    ContactsPageExtras,
    FieldSiteBullet,
    GalleryCategory,
    GalleryItem,
    GalleryPageSettings,
    HomeServiceCard,
    HomeStatTile,
    HubPageStub,
    NewsListSettings,
    PressNewsArticle,
    TeamMember,
    TeamValue,
    Vacancy,
    VirtualTourOfficeZone,
    WorkPageKpi,
    WorksPageSettings,
    WorkTimelineProject,
)


def _language_code():
    language = (get_language() or "ru").lower()
    return "en" if language.startswith("en") else "ru"


def _pick(instance, stem: str) -> str:
    if instance is None:
        return ""
    lc = _language_code()
    ru = getattr(instance, f"{stem}_ru", None)
    en = getattr(instance, f"{stem}_en", None)
    ru_s = "" if ru is None else str(ru)
    en_s = "" if en is None else str(en)
    if lc == "en":
        return (en_s.strip() or ru_s.strip())
    return ru_s.strip()


def _display_date(a: PressNewsArticle) -> str:
    lc = _language_code()
    ru = (a.display_date_ru or "").strip()
    en = (a.display_date_en or "").strip()
    if lc == "en":
        return en or ru or a.published_at.isoformat()
    return ru or a.published_at.strftime("%d.%m.%Y")


def _serialize_timeline(p: WorkTimelineProject) -> dict:
    return {
        "blue_left": p.blue_left,
        "blue_height_px": float(p.blue_height_px),
        "period": p.period,
        "project_title": _pick(p, "title"),
        "status": _pick(p, "status"),
        "description": _pick(p, "description"),
        "achievements": [_pick(a, "text") for a in p.achievements.all()],
    }


def _serialize_home_project(p: WorkTimelineProject) -> dict:
    return {
        "period": p.period,
        "title": _pick(p, "title"),
        "status": _pick(p, "status"),
        "summary": _pick(p, "description"),
        "achievements": [_pick(a, "text") for a in p.achievements.all()],
    }


def _serialize_kpi(k: WorkPageKpi) -> dict:
    lc = _language_code()
    if lc == "en":
        if (k.label_html_en or "").strip():
            return {"value": k.value, "label_html": k.label_html_en, "label": None}
        return {"value": k.value, "label_html": None, "label": (k.label_en or k.label_ru)}
    if (k.label_html_ru or "").strip():
        return {"value": k.value, "label_html": k.label_html_ru, "label": None}
    return {"value": k.value, "label_html": None, "label": k.label_ru}


def _serialize_home_stat(t: HomeStatTile) -> dict:
    label = _pick(t, "label")
    is_html = bool(t.use_html_labels) or ("<" in label)
    return {"value": t.value_text, "label": label, "label_is_html": is_html}


def _serialize_home_service(c: HomeServiceCard) -> dict:
    body = _pick(c, "body")
    return {
        "icon": c.icon,
        "title": _pick(c, "title"),
        "body": body,
        "body_is_html": "<" in body,
    }


def _serialize_featured_news(a: PressNewsArticle) -> dict:
    excerpt = _pick(a, "excerpt")
    mod = (a.gallery_style or "").strip() or "production"
    return {
        "media_modifier": mod,
        "tag": _pick(a, "category"),
        "date_display": _display_date(a),
        "title": _pick(a, "title"),
        "excerpt": excerpt,
        "excerpt_is_html": "<" in excerpt,
    }


def _news_row_for_list(a: PressNewsArticle, index: int) -> dict:
    excerpt = _pick(a, "excerpt")
    row = {
        "iso_date": a.published_at.isoformat(),
        "date_display": _display_date(a),
        "category": _pick(a, "category"),
        "title": _pick(a, "title"),
        "excerpt": excerpt,
        "excerpt_is_html": "<" in excerpt,
    }
    if a.hero_image:
        row["image_is_media"] = True
        row["image_url"] = a.hero_image.url
    else:
        row["image_is_media"] = False
        row["image_static"] = f"img/news/news-{(index % 6) + 1:02d}.png"
    return row


def _gallery_row(it: GalleryItem) -> dict:
    src = it.resolved_src()
    is_media = bool(it.image)
    return {
        "src": src,
        "is_media": is_media,
        "alt": _pick(it, "caption"),
        "category": it.category.slug,
    }


def home(request):
    stats = [_serialize_home_stat(t) for t in HomeStatTile.objects.order_by("sort_order", "pk")]
    services = [_serialize_home_service(c) for c in HomeServiceCard.objects.order_by("sort_order", "pk")]
    featured_news = [
        _serialize_featured_news(a)
        for a in PressNewsArticle.objects.filter(is_published=True, show_on_homepage=True).order_by(
            "home_sort_order",
            "-published_at",
            "pk",
        )
    ]
    home_projects_qs = (
        WorkTimelineProject.objects.filter(show_on_homepage=True)
        .prefetch_related("achievements")
        .order_by("home_sort_order", "pk")
    )
    home_projects = [_serialize_home_project(p) for p in home_projects_qs]
    return render(
        request,
        "pages/home.html",
        {
            "home_stats": stats,
            "home_services": services,
            "featured_news": featured_news,
            "home_projects": home_projects,
        },
    )


def about(request):
    hub = HubPageStub.objects.filter(code="about").first()
    return render(request, "pages/empty.html", {"page_title": _pick(hub, "heading")})


def works(request):
    lbl = WorksPageSettings.objects.filter(pk=1).first()
    tl_qs = WorkTimelineProject.objects.prefetch_related("achievements").order_by("sort_order", "pk")
    timeline = [_serialize_timeline(p) for p in tl_qs]
    kpis = [_serialize_kpi(k) for k in WorkPageKpi.objects.order_by("sort_order", "pk")]
    context = {
        "page_title": _pick(lbl, "page_title"),
        "hero_title": _pick(lbl, "hero_title"),
        "hero_subtitle": _pick(lbl, "hero_subtitle"),
        "realized_title": _pick(lbl, "realized_heading"),
        "realized_lead": _pick(lbl, "realized_lead"),
        "timeline": timeline,
        "kpi_section_title": _pick(lbl, "kpi_heading"),
        "kpis": kpis,
        "cta_title": _pick(lbl, "cta_title"),
        "cta_subtitle": _pick(lbl, "cta_subtitle"),
    }
    return render(request, "pages/works.html", context)


def press(request):
    hub = HubPageStub.objects.filter(code="press").first()
    return render(request, "pages/empty.html", {"page_title": _pick(hub, "heading")})


def career(request):
    vacancies = Vacancy.objects.filter(is_active=True)
    accept = request.headers.get("Accept", "")
    wants_json = request.headers.get("X-Requested-With") == "XMLHttpRequest" or (
        accept and "application/json" in accept
    )

    if request.method == "POST":
        form = CandidateApplicationForm(request.POST)
        if form.is_valid():
            status = CandidateStatus.objects.filter(name="Новая").first() or CandidateStatus.objects.order_by(
                "pk",
            ).first()
            if not status:
                err = _("Справочник статусов не настроен. Обратитесь к администратору сайта.")
                if wants_json:
                    return JsonResponse({"ok": False, "message": str(err)}, status=503)
                messages.error(request, err)
            else:
                form.save_profile(status=status)
                if wants_json:
                    return JsonResponse({"ok": True})
                return redirect(f"{request.path}?application_sent=1")
        else:
            err = _("Не удалось отправить анкету. Проверьте поля и попробуйте снова.")
            if wants_json:
                return JsonResponse({"ok": False, "message": str(err)}, status=400)
            messages.error(request, err)

    cfg = CareerPageSettings.objects.filter(pk=1).first()
    hero_title = _pick(cfg, "hero_title") or _("Карьера")
    hero_lead = _pick(cfg, "hero_lead") or _("Присоединяйтесь к нашей команде")

    return render(
        request,
        "pages/career.html",
        {"vacancies": vacancies, "career_hero_title": hero_title, "career_hero_lead": hero_lead},
    )


def contacts(request):
    ce = ContactsPageExtras.objects.filter(pk=1).first()
    hero_title = _pick(ce, "hero_title") or _("Контакты")
    hero_lead = _pick(ce, "hero_lead") or _("Свяжитесь с нами удобным способом")
    ctx = {
        "contacts_hero_title": hero_title,
        "contacts_hero_lead": hero_lead,
        "contacts_panel_eyebrow": _pick(ce, "panel_eyebrow"),
        "contacts_panel_heading": _pick(ce, "panel_heading"),
        "contacts_panel_lead": _pick(ce, "panel_lead"),
    }
    return render(request, "pages/contacts.html", ctx)


def about_company(request):
    cards_qs = AboutExploreCard.objects.order_by("sort_order", "pk")
    explore_cards = [
        {"href": c.build_url(), "title": _pick(c, "title"), "text": _pick(c, "text")} for c in cards_qs
    ]
    return render(request, "pages/about_company.html", {"explore_cards": explore_cards})


def about_field(request):
    geo_bullets = FieldSiteBullet.objects.filter(group_slug="geo").order_by("sort_order", "pk")
    geology_bullets = FieldSiteBullet.objects.filter(group_slug="geology").order_by("sort_order", "pk")
    field_geo = [{"text": _pick(b, "body"), "is_html": b.supports_html} for b in geo_bullets]
    field_geology = [{"text": _pick(b, "body"), "is_html": b.supports_html} for b in geology_bullets]
    return render(request, "pages/about_field.html", {"field_geo": field_geo, "field_geology": field_geology})


def about_team(request):
    team_members = (
        TeamMember.objects.select_related("department")
        .prefetch_related("socials__social")
        .order_by("last_name", "first_name")
    )
    values = [{"title": _pick(v, "title"), "body": _pick(v, "body")} for v in TeamValue.objects.order_by("sort_order")]
    return render(
        request,
        "pages/about_team.html",
        {"team_members": team_members, "team_values": values},
    )


def about_license(request):
    return render(request, "pages/about_license.html")


def about_tour(request):
    zones_qs = VirtualTourOfficeZone.objects.prefetch_related("bullets").order_by("sort_order", "pk")
    tour_zones = []
    for z in zones_qs:
        bul = [_pick(b, "text") for b in z.bullets.all()]
        tour_zones.append(
            {
                "slug": z.slug,
                "css_modifier": z.css_modifier,
                "title": _pick(z, "title"),
                "intro": _pick(z, "intro"),
                "bullets": bul,
            },
        )
    return render(request, "pages/about_tour.html", {"tour_zones": tour_zones})


def press_news(request):
    nls = NewsListSettings.objects.filter(pk=1).first()
    qs = PressNewsArticle.objects.filter(is_published=True).order_by("-published_at", "pk")
    page_size = nls.list_page_size if nls else 6
    article_rows = [_news_row_for_list(a, ix) for ix, a in enumerate(qs)]
    paginator = Paginator(article_rows, page_size)
    news_page = paginator.get_page(request.GET.get("page") or 1)
    context = {
        "page_title": _pick(nls, "page_title"),
        "hero_title": _pick(nls, "hero_title"),
        "hero_subtitle": _pick(nls, "hero_subtitle"),
        "news_page": news_page,
        "news_cta_title": _pick(nls, "cta_title"),
        "news_cta_subtitle": _pick(nls, "cta_subtitle"),
        "news_cta_button": _pick(nls, "cta_button"),
    }
    return render(request, "pages/news.html", context)


def press_gallery(request):
    cfg = GalleryPageSettings.objects.filter(pk=1).first()
    cats_qs = GalleryCategory.objects.order_by("sort_order", "slug")
    gallery_categories = [{"id": c.slug, "label": _pick(c, "label")} for c in cats_qs]
    items_qs = GalleryItem.objects.select_related("category").filter(is_active=True).order_by("sort_order", "pk")
    gallery_items = [_gallery_row(it) for it in items_qs]
    category = (request.GET.get("category") or "all").strip()
    valid_ids = {c["id"] for c in gallery_categories}
    if category not in valid_ids:
        category = "all"
    filtered = gallery_items if category == "all" else [row for row in gallery_items if row["category"] == category]
    initial = cfg.initial_visible_count if cfg else 8
    context = {
        "page_title": _pick(cfg, "page_title"),
        "hero_title": _pick(cfg, "hero_title"),
        "hero_subtitle": _pick(cfg, "hero_subtitle"),
        "gallery_items": filtered,
        "gallery_categories": gallery_categories,
        "gallery_category_active": category,
        "gallery_initial_visible": initial,
    }
    return render(request, "pages/gallery.html", context)
