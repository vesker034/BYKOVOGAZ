from django.contrib import admin

from .models import (
    AboutExploreCard,
    BrandSettings,
    CareerPageSettings,
    CandidateAttachment,
    CandidateProfile,
    CandidateStatus,
    ContactMessage,
    ContactMessageAttachment,
    ContactsPageExtras,
    Department,
    FieldSiteBullet,
    GalleryCategory,
    GalleryItem,
    GalleryPageSettings,
    HomeServiceCard,
    HomeStatTile,
    HubPageStub,
    LocalizedMessage,
    MarketingAsset,
    MemberSocialLink,
    NewsListSettings,
    OrganizationContacts,
    PressNewsArticle,
    Role,
    SocialLink,
    TeamMember,
    TeamValue,
    UserRole,
    Vacancy,
    VirtualTourBullet,
    VirtualTourOfficeZone,
    WorkPageKpi,
    WorksPageSettings,
    WorkTimelineAchievement,
    WorkTimelineProject,
)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ("title", "title_en", "employment_type", "is_active", "display_order")
    list_display_links = ("title",)
    list_filter = ("is_active", "employment_type")
    search_fields = (
        "title",
        "title_en",
        "department",
        "department_en",
        "location",
        "location_en",
        "summary",
        "summary_en",
        "requirements",
        "requirements_en",
    )
    list_editable = ("is_active", "display_order")
    ordering = ("display_order", "-created_at")
    fieldsets = (
        ("Русский", {
            "fields": ("title", "department", "location", "summary", "requirements"),
        }),
        ("English", {
            "fields": ("title_en", "department_en", "location_en", "summary_en", "requirements_en"),
        }),
        ("Параметры публикации", {
            "fields": ("employment_type", "is_active", "display_order"),
        }),
    )


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    list_filter = ("role",)
    autocomplete_fields = ("user", "role")


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ("name",)


class MemberSocialLinkInline(admin.TabularInline):
    model = MemberSocialLink
    extra = 0
    autocomplete_fields = ("social",)


@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    search_fields = ("name", "base_url")


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "position", "department", "created_at")
    list_filter = ("department",)
    search_fields = ("first_name", "last_name", "position", "bio")
    autocomplete_fields = ("department",)
    inlines = [MemberSocialLinkInline]


class CandidateAttachmentInline(admin.TabularInline):
    model = CandidateAttachment
    extra = 1


@admin.register(CandidateStatus)
class CandidateStatusAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "desired_position", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("full_name", "email", "phone", "desired_position", "message")
    autocomplete_fields = ("status",)
    date_hierarchy = "created_at"
    inlines = [CandidateAttachmentInline]


class ContactMessageAttachmentInline(admin.TabularInline):
    model = ContactMessageAttachment
    extra = 1


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_email", "subject", "created_at", "processed_by")
    search_fields = ("name", "phone_email", "subject", "message")
    autocomplete_fields = ("processed_by",)
    date_hierarchy = "created_at"
    inlines = [ContactMessageAttachmentInline]


@admin.register(LocalizedMessage)
class LocalizedMessageAdmin(admin.ModelAdmin):
    search_fields = ("key", "ru", "en")
    list_display = ("key", "ru_preview", "en_preview")

    @staticmethod
    def ru_preview(obj):
        text = (obj.ru or "").replace("\n", " ")
        return text[:72] + ("…" if len(text) > 72 else "")

    @staticmethod
    def en_preview(obj):
        text = (obj.en or "").replace("\n", " ")
        return text[:72] + ("…" if len(text) > 72 else "")


@admin.register(BrandSettings)
class BrandSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(OrganizationContacts)
class OrganizationContactsAdmin(admin.ModelAdmin):
    pass


@admin.register(MarketingAsset)
class MarketingAssetAdmin(admin.ModelAdmin):
    pass


@admin.register(WorksPageSettings)
class WorksPageSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(NewsListSettings)
class NewsListSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(GalleryPageSettings)
class GalleryPageSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactsPageExtras)
class ContactsPageExtrasAdmin(admin.ModelAdmin):
    pass


@admin.register(CareerPageSettings)
class CareerPageSettingsAdmin(admin.ModelAdmin):
    pass


@admin.register(HubPageStub)
class HubPageStubAdmin(admin.ModelAdmin):
    list_display = ("code", "heading_ru")


class WorkTimelineAchievementInline(admin.TabularInline):
    model = WorkTimelineAchievement
    extra = 0
    ordering = ("sort_order", "pk")


@admin.register(WorkTimelineProject)
class WorkTimelineProjectAdmin(admin.ModelAdmin):
    list_display = ("period", "title_ru", "sort_order", "show_on_homepage", "home_sort_order")
    list_editable = ("sort_order", "show_on_homepage", "home_sort_order")
    inlines = (WorkTimelineAchievementInline,)
    search_fields = ("title_ru", "title_en", "period")


@admin.register(WorkPageKpi)
class WorkPageKpiAdmin(admin.ModelAdmin):
    list_display = ("value", "label_ru", "sort_order")
    list_editable = ("sort_order",)
    ordering = ("sort_order", "pk")


@admin.register(PressNewsArticle)
class PressNewsArticleAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "published_at", "show_on_homepage", "home_sort_order", "is_published")
    list_filter = ("is_published", "show_on_homepage")
    list_editable = ("show_on_homepage", "home_sort_order", "is_published")
    search_fields = ("title_ru", "title_en", "category_ru")
    date_hierarchy = "published_at"
    ordering = ("-published_at", "pk")


@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ("slug", "label_ru", "sort_order", "is_all_option")
    list_editable = ("sort_order", "is_all_option")


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("caption_ru", "category", "sort_order", "is_active")
    list_filter = ("category", "is_active")
    list_editable = ("sort_order", "is_active")


@admin.register(HomeStatTile)
class HomeStatTileAdmin(admin.ModelAdmin):
    list_display = ("value_text", "label_ru", "sort_order", "use_html_labels")
    list_editable = ("sort_order", "use_html_labels")


@admin.register(HomeServiceCard)
class HomeServiceCardAdmin(admin.ModelAdmin):
    list_display = ("icon", "title_ru", "sort_order")
    list_editable = ("sort_order",)


@admin.register(TeamValue)
class TeamValueAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "sort_order")
    list_editable = ("sort_order",)


@admin.register(AboutExploreCard)
class AboutExploreCardAdmin(admin.ModelAdmin):
    list_display = ("title_ru", "url_name", "sort_order")
    list_editable = ("sort_order",)


class VirtualTourBulletInline(admin.TabularInline):
    model = VirtualTourBullet
    extra = 0
    ordering = ("sort_order", "pk")


@admin.register(VirtualTourOfficeZone)
class VirtualTourOfficeZoneAdmin(admin.ModelAdmin):
    list_display = ("slug", "title_ru", "sort_order")
    list_editable = ("sort_order",)
    inlines = (VirtualTourBulletInline,)
    ordering = ("sort_order", "pk")


@admin.register(FieldSiteBullet)
class FieldSiteBulletAdmin(admin.ModelAdmin):
    list_display = ("group_slug", "body_ru", "sort_order", "supports_html")
    list_filter = ("group_slug",)
    list_editable = ("sort_order", "supports_html")
    ordering = ("group_slug", "sort_order", "pk")
