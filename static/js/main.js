"use strict";

document.documentElement.classList.add("js-ready");

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
            nameField.setCustomValidity("Введите имя.");
        } else if (value.length < 2) {
            nameField.setCustomValidity("Имя должно содержать минимум 2 символа.");
        } else if (!/^[A-Za-zА-Яа-яЁё\s-]+$/.test(value)) {
            nameField.setCustomValidity("Имя может содержать только буквы, пробелы и дефис.");
        } else {
            nameField.setCustomValidity("");
        }
    }

    function setEmailValidity() {
        const value = emailField.value.trim();

        if (!value) {
            emailField.setCustomValidity("Введите email.");
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(value)) {
            emailField.setCustomValidity("Укажите корректный email, например your@email.com.");
        } else {
            emailField.setCustomValidity("");
        }
    }

    function setPhoneValidity() {
        const value = phoneField.value.trim();

        if (!value) {
            phoneField.setCustomValidity("");
        } else if (!/^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$/.test(value)) {
            phoneField.setCustomValidity("Введите телефон в формате +7 (900) 123-45-67.");
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
            subjectField.setCustomValidity("Укажите тему обращения.");
        } else if (value.length < 3) {
            subjectField.setCustomValidity("Тема должна содержать минимум 3 символа.");
        } else {
            subjectField.setCustomValidity("");
        }
    }

    function setMessageValidity() {
        const value = messageField.value.trim();

        if (!value) {
            messageField.setCustomValidity("Введите сообщение.");
        } else if (value.length < 10) {
            messageField.setCustomValidity("Сообщение должно содержать минимум 10 символов.");
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
    const themeButtons = Array.from(document.querySelectorAll("[data-theme-option]"));

    function getStoredTheme() {
        const storedTheme = window.localStorage.getItem(storageKey);
        return storedTheme === "dark" ? "dark" : "light";
    }

    function updateToggleUi(theme) {
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

    if (!themeButtons.length) {
        return;
    }

    applyTheme(getStoredTheme());

    themeButtons.forEach(function (button) {
        button.addEventListener("click", function () {
            const selectedTheme = button.dataset.themeOption === "dark" ? "dark" : "light";
            applyTheme(selectedTheme);
            window.localStorage.setItem(storageKey, selectedTheme);
        });
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
