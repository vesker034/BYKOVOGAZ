# -*- coding: utf-8 -*-
import re

from django import forms
from django.core.exceptions import ValidationError
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _

_name_re = re.compile(r"^[A-Za-zА-Яа-яЁё\s\-]+$")
_phone_re = re.compile(r"^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$")
_birth_date_re = re.compile(r"^\d{2}\.\d{2}\.\d{4}$")


def validate_person_name_part(value: str, *, optional: bool) -> str:
    v = value.strip()
    if not v:
        if optional:
            return ""
        raise ValidationError(_("Обязательное поле."), code="required")
    if len(v) < 2:
        raise ValidationError(_("Не менее 2 символов."), code="min_length")
    if not _name_re.match(v):
        raise ValidationError(_("Допускаются только буквы, пробелы и дефис."), code="invalid_chars")
    return v


class CandidateApplicationForm(forms.Form):
    last_name = forms.CharField(label=_("Фамилия"), max_length=80)
    first_name = forms.CharField(label=_("Имя"), max_length=80)
    middle_name = forms.CharField(label=_("Отчество"), max_length=80, required=False)
    birth_date = forms.CharField(label=_("Дата рождения"), max_length=10)
    phone = forms.CharField(label=_("Телефон"), max_length=18)
    email = forms.EmailField(label=_("Email"), max_length=120)
    education = forms.ChoiceField(
        label=_("Образование"),
        choices=[
            ("school", _("Среднее")),
            ("vocational", _("Среднее специальное")),
            ("incomplete_higher", _("Неполное высшее")),
            ("higher", _("Высшее")),
            ("multiple_higher", _("Несколько высших")),
            ("postgraduate", _("Аспирантура, кандидат наук")),
        ],
    )
    position = forms.CharField(label=_("Желаемая должность"), max_length=120, min_length=3)
    experience = forms.ChoiceField(
        label=_("Опыт работы"),
        choices=[
            ("none", _("Без опыта")),
            ("lt1", _("До 1 года")),
            ("y1_3", _("1-3 года")),
            ("y3_5", _("3-5 лет")),
            ("gt5", _("Более 5 лет")),
        ],
    )
    about = forms.CharField(label=_("О себе"), min_length=10, max_length=2000, widget=forms.Textarea)

    def clean_last_name(self) -> str:
        return validate_person_name_part(self.cleaned_data.get("last_name", ""), optional=False)

    def clean_first_name(self) -> str:
        return validate_person_name_part(self.cleaned_data.get("first_name", ""), optional=False)

    def clean_middle_name(self) -> str:
        raw = self.cleaned_data.get("middle_name") or ""
        v = raw.strip()
        if not v:
            return ""
        return validate_person_name_part(v, optional=False)

    def clean_phone(self) -> str:
        v = (self.cleaned_data.get("phone") or "").strip()
        if not v:
            raise ValidationError(_("Введите телефон."), code="required")
        if not _phone_re.match(v):
            raise ValidationError(_("Введите телефон в формате +7 (900) 123-45-67."), code="invalid_phone")
        return v

    def clean_birth_date(self) -> str:
        v = (self.cleaned_data.get("birth_date") or "").strip()
        if not v:
            raise ValidationError(_("Введите дату рождения."), code="required")
        if not _birth_date_re.match(v):
            raise ValidationError(_("Введите дату в формате ДД.ММ.ГГГГ."), code="invalid_format")
        day_s, month_s, year_s = v.split(".")
        try:
            from datetime import date as date_cls

            date_cls(int(year_s), int(month_s), int(day_s))
        except ValueError as exc:
            raise ValidationError(_("Укажите корректную дату."), code="invalid_date") from exc
        return v

    def save_profile(self, *, status):
        from django.utils.translation import gettext as _

        data = self.cleaned_data
        parts = [
            _("Дата рождения: %(d)s") % {"d": data["birth_date"]},
            _("Образование: %(e)s") % {
                "e": force_str(dict(self.fields["education"].choices).get(data["education"], data["education"]))
            },
            _("Опыт работы: %(e)s") % {
                "e": force_str(dict(self.fields["experience"].choices).get(data["experience"], data["experience"]))
            },
            "",
            _("О себе:"),
            data["about"].strip(),
        ]
        body = "\n".join(force_str(part) for part in parts)

        fn_parts = [data["last_name"], data["first_name"]]
        if data.get("middle_name"):
            fn_parts.append(data["middle_name"])
        full_name = " ".join(fn_parts)

        from .models import CandidateProfile

        return CandidateProfile.objects.create(
            status=status,
            full_name=full_name,
            phone=data["phone"],
            email=data["email"],
            desired_position=data["position"],
            message=body,
        )
