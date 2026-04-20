from django.urls import path

from .views import (
    about,
    about_company,
    about_field,
    about_license,
    about_team,
    about_tour,
    career,
    contacts,
    home,
    press,
    press_gallery,
    press_news,
    works,
)


app_name = "main"

urlpatterns = [
    path("", home, name="home"),
    path("about/", about, name="about"),
    path("works/", works, name="works"),
    path("press/", press, name="press"),
    path("career/", career, name="career"),
    path("contacts/", contacts, name="contacts"),
    path("about/company/", about_company, name="about_company"),
    path("about/field/", about_field, name="about_field"),
    path("about/team/", about_team, name="about_team"),
    path("about/license/", about_license, name="about_license"),
    path("about/tour/", about_tour, name="about_tour"),
    path("press/news/", press_news, name="press_news"),
    path("press/gallery/", press_gallery, name="press_gallery"),
    path("press/news-gallery/", press_gallery, name="press_news_gallery"),
]
