from django.shortcuts import render


def home(request):
    return render(request, "pages/home.html")


def about(request):
    return render(request, "pages/empty.html", {"page_title": "О нас"})


def works(request):
    return render(request, "pages/empty.html", {"page_title": "Наши работы"})


def press(request):
    return render(request, "pages/empty.html", {"page_title": "Пресс-центр"})


def career(request):
    return render(request, "pages/empty.html", {"page_title": "Карьера"})


def contacts(request):
    return render(request, "pages/empty.html", {"page_title": "Контакты"})


def about_company(request):
    return render(request, "pages/about_company.html")


def about_field(request):
    return render(request, "pages/about_field.html")


def about_team(request):
    return render(request, "pages/about_team.html")


def about_license(request):
    return render(request, "pages/empty.html", {"page_title": "Лицензия"})


def about_tour(request):
    return render(request, "pages/empty.html", {"page_title": "Виртуальный тур"})


def press_news(request):
    return render(request, "pages/empty.html", {"page_title": "Новости"})


def press_gallery(request):
    return render(request, "pages/empty.html", {"page_title": "Галерея"})
