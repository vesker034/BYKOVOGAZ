"use strict";

document.documentElement.classList.add("js-ready");

const siteI18n = window.siteI18n || {};
const homeFormMessages = siteI18n.homeForm || {};
const careerFormMessages = siteI18n.careerForm || {};
const newsMessages = siteI18n.news || {};

(function () {
    const form = document.querySelector("[data-home-contact-form]");

    if (!form) {
        return;
    }

    const nameField = form.querySelector('[data-field="name"]');
    const emailField = form.querySelector('[data-field="email"]');
    const phoneField = form.querySelector('[data-field="phone"]');
    const subjectField = form.querySelector('[data-field="subject"]');
    const messageField = form.querySelector('[data-field="message"]');

    function shouldShowError(field, force) {
        const isRequiredEmpty = field.hasAttribute("required") && !field.value.trim();

        if (force) {
            return !field.checkValidity();
        }

        if (field.dataset.touched === "true") {
            return !field.checkValidity();
        }

        if (!isRequiredEmpty && field.value.trim() !== "") {
            return !field.checkValidity();
        }

        return false;
    }

    function toggleErrorState(field, force) {
        if (!field) {
            return;
        }

        field.classList.toggle("home-form__control--invalid", shouldShowError(field, force));
    }

    function setNameValidity() {
        const value = nameField.value.trim();

        if (!value) {
            nameField.setCustomValidity(homeFormMessages.nameRequired || "Введите имя.");
        } else if (value.length < 2) {
            nameField.setCustomValidity(homeFormMessages.nameShort || "Имя должно содержать минимум 2 символа.");
        } else if (!/^[A-Za-zА-Яа-яЁё\s-]+$/.test(value)) {
            nameField.setCustomValidity(homeFormMessages.nameInvalid || "Имя может содержать только буквы, пробелы и дефис.");
        } else {
            nameField.setCustomValidity("");
        }
    }

    function setEmailValidity() {
        const value = emailField.value.trim();

        if (!value) {
            emailField.setCustomValidity(homeFormMessages.emailRequired || "Введите email.");
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
            emailField.setCustomValidity(homeFormMessages.emailInvalid || "Укажите корректный email, например your@email.com.");
        } else {
            emailField.setCustomValidity("");
        }
    }

    function setPhoneValidity() {
        const value = phoneField.value.trim();

        if (!value) {
            phoneField.setCustomValidity("");
        } else if (!/^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/.test(value)) {
            phoneField.setCustomValidity(homeFormMessages.phoneInvalid || "Введите телефон в формате +7 (900) 123-45-67.");
        } else {
            phoneField.setCustomValidity("");
        }
    }

    function formatPhoneValue(value) {
        const digitsOnly = value.replace(/\D/g, "");

        if (!digitsOnly) {
            return "";
        }

        let nationalDigits = digitsOnly;

        if (digitsOnly[0] === "7" || digitsOnly[0] === "8") {
            nationalDigits = digitsOnly.slice(1);
        }

        nationalDigits = nationalDigits.slice(0, 10);

        let formatted = "+7";

        if (digitsOnly.length > 0) {
            formatted += " (";
        }

        if (nationalDigits.length > 0) {
            formatted += nationalDigits.slice(0, 3);
        }

        if (nationalDigits.length >= 3) {
            formatted += ") ";
        }

        if (nationalDigits.length > 3) {
            formatted += nationalDigits.slice(3, 6);
        }

        if (nationalDigits.length >= 6) {
            formatted += "-";
        }

        if (nationalDigits.length > 6) {
            formatted += nationalDigits.slice(6, 8);
        }

        if (nationalDigits.length >= 8) {
            formatted += "-";
        }

        if (nationalDigits.length > 8) {
            formatted += nationalDigits.slice(8, 10);
        }

        return formatted;
    }

    function setSubjectValidity() {
        const value = subjectField.value.trim();

        if (!value) {
            subjectField.setCustomValidity(homeFormMessages.subjectRequired || "Укажите тему обращения.");
        } else if (value.length < 3) {
            subjectField.setCustomValidity(homeFormMessages.subjectShort || "Тема должна содержать минимум 3 символа.");
        } else {
            subjectField.setCustomValidity("");
        }
    }

    function setMessageValidity() {
        const value = messageField.value.trim();

        if (!value) {
            messageField.setCustomValidity(homeFormMessages.messageRequired || "Введите сообщение.");
        } else if (value.length < 10) {
            messageField.setCustomValidity(homeFormMessages.messageShort || "Сообщение должно содержать минимум 10 символов.");
        } else {
            messageField.setCustomValidity("");
        }
    }

    function bindValidation(field, validate) {
        field.addEventListener("input", function () {
            validate();
            toggleErrorState(field, false);
        });

        field.addEventListener("blur", function () {
            field.dataset.touched = "true";
            validate();
            toggleErrorState(field, true);
        });
    }

    bindValidation(nameField, setNameValidity);
    bindValidation(emailField, setEmailValidity);
    phoneField.addEventListener("input", function () {
        phoneField.value = formatPhoneValue(phoneField.value);
        setPhoneValidity();
        toggleErrorState(phoneField, false);
    });

    phoneField.addEventListener("blur", function () {
        phoneField.dataset.touched = "true";
        phoneField.value = formatPhoneValue(phoneField.value);
        setPhoneValidity();
        toggleErrorState(phoneField, true);
    });

    bindValidation(subjectField, setSubjectValidity);
    bindValidation(messageField, setMessageValidity);

    form.addEventListener("submit", function (event) {
        setNameValidity();
        setEmailValidity();
        setPhoneValidity();
        setSubjectValidity();
        setMessageValidity();

        [nameField, emailField, phoneField, subjectField, messageField].forEach(function (field) {
            field.dataset.touched = "true";
            toggleErrorState(field, true);
        });

        if (!form.checkValidity()) {
            event.preventDefault();
            form.reportValidity();
            return;
        }

        event.preventDefault();
    });
})();

(function () {
    const form = document.querySelector("[data-career-form]");

    if (!form) {
        return;
    }

    const lastNameField = form.querySelector('[data-field="last-name"]');
    const firstNameField = form.querySelector('[data-field="first-name"]');
    const middleNameField = form.querySelector('[data-field="middle-name"]');
    const birthDateField = form.querySelector('[data-field="birth-date"]');
    const phoneField = form.querySelector('[data-field="phone"]');
    const emailField = form.querySelector('[data-field="email"]');
    const educationField = form.querySelector('[data-field="education"]');
    const positionField = form.querySelector('[data-field="position"]');
    const experienceField = form.querySelector('[data-field="experience"]');
    const aboutField = form.querySelector('[data-field="about"]');
    const allFields = [
        lastNameField,
        firstNameField,
        middleNameField,
        birthDateField,
        phoneField,
        emailField,
        educationField,
        positionField,
        experienceField,
        aboutField,
    ];

    function shouldShowError(field, force) {
        const rawValue = "value" in field ? field.value : "";
        const isRequiredEmpty = field.hasAttribute("required") && !rawValue.trim();

        if (force) {
            return !field.checkValidity();
        }

        if (field.dataset.touched === "true") {
            return !field.checkValidity();
        }

        if (!isRequiredEmpty && rawValue.trim() !== "") {
            return !field.checkValidity();
        }

        return false;
    }

    function toggleErrorState(field, force) {
        if (!field) {
            return;
        }

        field.classList.toggle("form-control-custom--invalid", shouldShowError(field, force));
    }

    function formatPhoneValue(value) {
        const digitsOnly = value.replace(/\D/g, "");

        if (!digitsOnly) {
            return "";
        }

        let nationalDigits = digitsOnly;

        if (digitsOnly[0] === "7" || digitsOnly[0] === "8") {
            nationalDigits = digitsOnly.slice(1);
        }

        nationalDigits = nationalDigits.slice(0, 10);

        let formatted = "+7";

        if (digitsOnly.length > 0) {
            formatted += " (";
        }

        if (nationalDigits.length > 0) {
            formatted += nationalDigits.slice(0, 3);
        }

        if (nationalDigits.length >= 3) {
            formatted += ") ";
        }

        if (nationalDigits.length > 3) {
            formatted += nationalDigits.slice(3, 6);
        }

        if (nationalDigits.length >= 6) {
            formatted += "-";
        }

        if (nationalDigits.length > 6) {
            formatted += nationalDigits.slice(6, 8);
        }

        if (nationalDigits.length >= 8) {
            formatted += "-";
        }

        if (nationalDigits.length > 8) {
            formatted += nationalDigits.slice(8, 10);
        }

        return formatted;
    }

    function isValidDate(value) {
        const match = value.match(/^(\d{2})\.(\d{2})\.(\d{4})$/);

        if (!match) {
            return false;
        }

        const day = Number.parseInt(match[1], 10);
        const month = Number.parseInt(match[2], 10);
        const year = Number.parseInt(match[3], 10);
        const date = new Date(year, month - 1, day);

        return date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day;
    }

    function setPersonNameValidity(field, emptyMessage, shortMessage, invalidMessage, isRequired) {
        const value = field.value.trim();

        if (!value) {
            field.setCustomValidity(isRequired ? emptyMessage : "");
        } else if (value.length < 2) {
            field.setCustomValidity(shortMessage);
        } else if (!/^[A-Za-zА-Яа-яЁё\s-]+$/.test(value)) {
            field.setCustomValidity(invalidMessage);
        } else {
            field.setCustomValidity("");
        }
    }

    function setBirthDateValidity() {
        const value = birthDateField.value.trim();

        if (!value) {
            birthDateField.setCustomValidity(careerFormMessages.birthDateRequired || "Введите дату рождения.");
        } else if (!isValidDate(value)) {
            birthDateField.setCustomValidity(careerFormMessages.birthDateInvalid || "Введите дату в формате ДД.ММ.ГГГГ.");
        } else {
            birthDateField.setCustomValidity("");
        }
    }

    function setPhoneValidity() {
        const value = phoneField.value.trim();

        if (!value) {
            phoneField.setCustomValidity(careerFormMessages.phoneRequired || "Введите телефон.");
        } else if (!/^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/.test(value)) {
            phoneField.setCustomValidity(careerFormMessages.phoneInvalid || "Введите телефон в формате +7 (900) 123-45-67.");
        } else {
            phoneField.setCustomValidity("");
        }
    }

    function setEmailValidity() {
        const value = emailField.value.trim();

        if (!value) {
            emailField.setCustomValidity(careerFormMessages.emailRequired || "Введите email.");
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
            emailField.setCustomValidity(careerFormMessages.emailInvalid || "Укажите корректный email, например your@email.com.");
        } else {
            emailField.setCustomValidity("");
        }
    }

    function setSelectValidity(field, emptyMessage) {
        if (!field.value) {
            field.setCustomValidity(emptyMessage);
        } else {
            field.setCustomValidity("");
        }
    }

    function setPositionValidity() {
        const value = positionField.value.trim();

        if (!value) {
            positionField.setCustomValidity(careerFormMessages.positionRequired || "Укажите желаемую должность.");
        } else if (value.length < 3) {
            positionField.setCustomValidity(careerFormMessages.positionShort || "Должность должна содержать минимум 3 символа.");
        } else {
            positionField.setCustomValidity("");
        }
    }

    function setAboutValidity() {
        const value = aboutField.value.trim();

        if (!value) {
            aboutField.setCustomValidity(careerFormMessages.aboutRequired || "Расскажите немного о себе.");
        } else if (value.length < 10) {
            aboutField.setCustomValidity(careerFormMessages.aboutShort || "Поле О себе должно содержать минимум 10 символов.");
        } else {
            aboutField.setCustomValidity("");
        }
    }

    function bindValidation(field, validate) {
        field.addEventListener("input", function () {
            validate();
            toggleErrorState(field, false);
        });

        field.addEventListener("blur", function () {
            field.dataset.touched = "true";
            validate();
            toggleErrorState(field, true);
        });
    }

    bindValidation(lastNameField, function () {
        setPersonNameValidity(
            lastNameField,
            careerFormMessages.lastNameRequired || "Введите фамилию.",
            careerFormMessages.lastNameShort || "Фамилия должна содержать минимум 2 символа.",
            careerFormMessages.lastNameInvalid || "Фамилия может содержать только буквы, пробелы и дефис.",
            true
        );
    });

    bindValidation(firstNameField, function () {
        setPersonNameValidity(
            firstNameField,
            careerFormMessages.firstNameRequired || "Введите имя.",
            careerFormMessages.firstNameShort || "Имя должно содержать минимум 2 символа.",
            careerFormMessages.firstNameInvalid || "Имя может содержать только буквы, пробелы и дефис.",
            true
        );
    });

    bindValidation(middleNameField, function () {
        setPersonNameValidity(
            middleNameField,
            "",
            careerFormMessages.middleNameShort || "Отчество должно содержать минимум 2 символа.",
            careerFormMessages.middleNameInvalid || "Отчество может содержать только буквы, пробелы и дефис.",
            false
        );
    });

    bindValidation(birthDateField, setBirthDateValidity);
    birthDateField.addEventListener("input", function () {
        birthDateField.value = birthDateField.value
            .replace(/[^\d]/g, "")
            .slice(0, 8)
            .replace(/(\d{2})(\d)/, "$1.$2")
            .replace(/(\d{2}\.\d{2})(\d)/, "$1.$2");
        setBirthDateValidity();
        toggleErrorState(birthDateField, false);
    });

    phoneField.addEventListener("input", function () {
        phoneField.value = formatPhoneValue(phoneField.value);
        setPhoneValidity();
        toggleErrorState(phoneField, false);
    });

    phoneField.addEventListener("blur", function () {
        phoneField.dataset.touched = "true";
        phoneField.value = formatPhoneValue(phoneField.value);
        setPhoneValidity();
        toggleErrorState(phoneField, true);
    });

    bindValidation(emailField, setEmailValidity);
    bindValidation(educationField, function () {
        setSelectValidity(educationField, careerFormMessages.educationRequired || "Выберите образование.");
    });
    bindValidation(positionField, setPositionValidity);
    bindValidation(experienceField, function () {
        setSelectValidity(experienceField, careerFormMessages.experienceRequired || "Выберите опыт работы.");
    });
    bindValidation(aboutField, setAboutValidity);

    form.addEventListener("submit", function (event) {
        setPersonNameValidity(
            lastNameField,
            careerFormMessages.lastNameRequired || "Введите фамилию.",
            careerFormMessages.lastNameShort || "Фамилия должна содержать минимум 2 символа.",
            careerFormMessages.lastNameInvalid || "Фамилия может содержать только буквы, пробелы и дефис.",
            true
        );
        setPersonNameValidity(
            firstNameField,
            careerFormMessages.firstNameRequired || "Введите имя.",
            careerFormMessages.firstNameShort || "Имя должно содержать минимум 2 символа.",
            careerFormMessages.firstNameInvalid || "Имя может содержать только буквы, пробелы и дефис.",
            true
        );
        setPersonNameValidity(
            middleNameField,
            "",
            careerFormMessages.middleNameShort || "Отчество должно содержать минимум 2 символа.",
            careerFormMessages.middleNameInvalid || "Отчество может содержать только буквы, пробелы и дефис.",
            false
        );
        setBirthDateValidity();
        setPhoneValidity();
        setEmailValidity();
        setSelectValidity(educationField, careerFormMessages.educationRequired || "Выберите образование.");
        setPositionValidity();
        setSelectValidity(experienceField, careerFormMessages.experienceRequired || "Выберите опыт работы.");
        setAboutValidity();

        allFields.forEach(function (field) {
            field.dataset.touched = "true";
            toggleErrorState(field, true);
        });

        if (!form.checkValidity()) {
            event.preventDefault();
            form.reportValidity();
            return;
        }

        event.preventDefault();
    });
})();

(function () {
    const galleryRoot = document.querySelector("[data-gallery-root]");

    if (!galleryRoot) {
        return;
    }

    const loadMoreButton = galleryRoot.querySelector("[data-gallery-more]");
    const hiddenItemsSelector = ".news-gallery-grid__cell--hidden";
    const revealStep = Number.parseInt(galleryRoot.dataset.galleryStep || "8", 10);

    if (!loadMoreButton) {
        return;
    }

    function getHiddenItems() {
        return Array.from(galleryRoot.querySelectorAll(hiddenItemsSelector));
    }

    function updateButtonVisibility() {
        loadMoreButton.hidden = getHiddenItems().length === 0;
    }

    loadMoreButton.addEventListener("click", function () {
        const hiddenItems = getHiddenItems();

        hiddenItems.slice(0, revealStep).forEach(function (item) {
            item.classList.remove("news-gallery-grid__cell--hidden");
        });

        updateButtonVisibility();
    });

    updateButtonVisibility();
})();

(function () {
    const storageKey = "site-theme";
    const root = document.documentElement;
    const toggleButton = document.querySelector("[data-theme-toggle]");
    const themeButtons = Array.from(document.querySelectorAll("[data-theme-option]"));

    function getStoredTheme() {
        const storedTheme = window.localStorage.getItem(storageKey);
        return storedTheme === "dark" ? "dark" : "light";
    }

    function updateToggleUi(theme) {
        if (toggleButton) {
            const isDark = theme === "dark";
            const labelNode = toggleButton.querySelector("[data-theme-label]");
            const lightLabel = toggleButton.dataset.labelLight || "Light theme";
            const darkLabel = toggleButton.dataset.labelDark || "Dark theme";

            toggleButton.classList.toggle("is-dark", isDark);
            toggleButton.setAttribute("aria-pressed", String(isDark));
            toggleButton.setAttribute("title", isDark ? darkLabel : lightLabel);

            if (labelNode) {
                labelNode.textContent = isDark ? darkLabel : lightLabel;
            }
        }

        themeButtons.forEach(function (button) {
            const isActive = button.dataset.themeOption === theme;
            button.classList.toggle("is-active", isActive);
            button.setAttribute("aria-pressed", String(isActive));
        });
    }

    function applyTheme(theme) {
        root.dataset.theme = theme;
        updateToggleUi(theme);
    }

    if (!toggleButton && !themeButtons.length) {
        return;
    }

    applyTheme(getStoredTheme());

    if (toggleButton) {
        toggleButton.addEventListener("click", function () {
            const selectedTheme = root.dataset.theme === "dark" ? "light" : "dark";
            applyTheme(selectedTheme);
            window.localStorage.setItem(storageKey, selectedTheme);
        });
    }

    themeButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const selectedTheme = button.dataset.themeOption === "dark" ? "dark" : "light";
            applyTheme(selectedTheme);
            window.localStorage.setItem(storageKey, selectedTheme);
        });
    });
})();

(function () {
    const newsPaginationRoot = document.querySelector("[data-news-pagination-root]");
    let abortController = null;

    if (!newsPaginationRoot) {
        return;
    }

    function setLoadingState(isLoading) {
        newsPaginationRoot.setAttribute("aria-busy", String(isLoading));
    }

    function updateNewsContent(nextRoot) {
        newsPaginationRoot.innerHTML = nextRoot.innerHTML;
    }

    function fetchAndSwapPage(url, shouldPushState) {
        if (abortController) {
            abortController.abort();
        }

        abortController = new window.AbortController();
        setLoadingState(true);

        window.fetch(url, {
            signal: abortController.signal,
            headers: {
                "X-Requested-With": "XMLHttpRequest",
            },
        })
            .then(function (response) {
                if (!response.ok) {
                    throw new Error(newsMessages.loadFailed || "Не удалось загрузить страницу новостей.");
                }

                return response.text();
            })
            .then(function (html) {
                const parser = new window.DOMParser();
                const documentFromResponse = parser.parseFromString(html, "text/html");
                const nextRoot = documentFromResponse.querySelector("[data-news-pagination-root]");

                if (!nextRoot) {
                    throw new Error(newsMessages.blockMissing || "Не найден блок новостей в ответе сервера.");
                }

                updateNewsContent(nextRoot);

                if (shouldPushState) {
                    window.history.pushState({ newsPagination: true }, "", url);
                }
            })
            .catch(function (error) {
                if (error.name === "AbortError") {
                    return;
                }

                window.location.href = url;
            })
            .finally(function () {
                setLoadingState(false);
                abortController = null;
            });
    }

    newsPaginationRoot.addEventListener("click", function (event) {
        const link = event.target.closest(".news-pagination__btn[href]");

        if (!link) {
            return;
        }

        event.preventDefault();
        fetchAndSwapPage(link.href, true);
    });

    window.addEventListener("popstate", function () {
        if (!window.location.search.includes("page=") && !newsPaginationRoot.querySelector(".news-pagination")) {
            return;
        }

        fetchAndSwapPage(window.location.href, false);
    });
})();

(function () {
    const desktopMediaQuery = window.matchMedia("(min-width: 992px)");
    const dropdownItems = Array.from(document.querySelectorAll(".site-header .nav-item.dropdown"));

    if (!dropdownItems.length || !window.bootstrap || !window.bootstrap.Dropdown) {
        return;
    }

    dropdownItems.forEach(function (dropdownItem) {
        const toggle = dropdownItem.querySelector(".dropdown-toggle");

        if (!toggle) {
            return;
        }

        const dropdown = window.bootstrap.Dropdown.getOrCreateInstance(toggle);
        let closeTimeoutId = null;

        function clearCloseTimeout() {
            if (closeTimeoutId !== null) {
                window.clearTimeout(closeTimeoutId);
                closeTimeoutId = null;
            }
        }

        function showDropdown() {
            clearCloseTimeout();

            if (desktopMediaQuery.matches) {
                dropdown.show();
            }
        }

        function hideDropdown() {
            clearCloseTimeout();

            if (!desktopMediaQuery.matches) {
                return;
            }

            closeTimeoutId = window.setTimeout(function () {
                dropdown.hide();
            }, 120);
        }

        dropdownItem.addEventListener("mouseenter", showDropdown);
        dropdownItem.addEventListener("mouseleave", hideDropdown);
        dropdownItem.addEventListener("focusin", showDropdown);
        dropdownItem.addEventListener("focusout", function (event) {
            if (dropdownItem.contains(event.relatedTarget)) {
                return;
            }

            hideDropdown();
        });

        desktopMediaQuery.addEventListener("change", function (event) {
            clearCloseTimeout();

            if (!event.matches) {
                dropdown.hide();
            }
        });
    });
})();
