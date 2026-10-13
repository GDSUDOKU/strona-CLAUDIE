
(() => {
    // Nie uruchamiaj nawigacji drugi raz.
    if (window.__claudieNavigationStarted) return;
    window.__claudieNavigationStarted = true;

    const playerSelector = '.music-player';
    const navigationScriptSelector = 'script[data-site-navigation]';

    function getPersistentElements() {
        return [
            document.querySelector(playerSelector),
            document.querySelector(navigationScriptSelector)
        ].filter(Boolean);
    }

    function isInternalPageLink(link) {
        if (!link || !link.href) return false;
        if (link.target && link.target !== '_self') return false;
        if (link.hasAttribute('download')) return false;

        const url = new URL(link.href, window.location.href);

        if (url.origin !== window.location.origin) return false;

        // Obsługujemy tylko przejścia między plikami HTML
        // oraz kotwice na aktualnej stronie.
        return /\.html?$/i.test(url.pathname)
            || (
                url.pathname === window.location.pathname
                && url.hash
            );
    }

    function closeTransientUI() {
        document.querySelector('.lightbox')?.remove();
        document.body.classList.remove('lightbox-open');

        const menu = document.querySelector('.nav-links');
        const menuButton = document.querySelector('.menu-toggle');

        menu?.classList.remove('menu-open');

        if (menuButton) {
            menuButton.setAttribute('aria-expanded', 'false');
            menuButton.setAttribute('aria-label', 'Otwórz menu');
        }

        document.querySelectorAll('.submenu-open').forEach(element => {
            element.classList.remove('submenu-open');
        });

        document.querySelectorAll('.nav-dropdown-toggle').forEach(button => {
            button.setAttribute('aria-expanded', 'false');
        });
    }

    async function runPageScripts(parsedDocument) {
        const scripts = Array.from(
            parsedDocument.querySelectorAll('script')
        );

        for (const oldScript of scripts) {
            const src = oldScript.getAttribute('src');

            // Muzyka i nawigacja pozostają aktywne z poprzedniego dokumentu.
            if (
                src &&
                (
                    src.includes('music-player.js') ||
                    src.includes('site-navigation.js')
                )
            ) {
                continue;
            }

            try {
                let code = oldScript.textContent;

                if (src) {
                    const scriptURL = new URL(src, parsedDocument.baseURI);
                    const response = await fetch(scriptURL);

                    if (!response.ok) {
                        throw new Error(`Nie udało się pobrać ${src}`);
                    }

                    code = await response.text();
                }

                // Każdy skrypt działa we własnym zakresie,
                // dzięki czemu deklaracje const nie kolidują między stronami.
                if (code.trim()) {
                    new Function(code)();
                }
            } catch (error) {
                console.error('Błąd skryptu podstrony:', error);
            }
        }
    }

    async function navigateTo(url, addHistory = true) {
        const destination = new URL(url, window.location.href);

        if (destination.origin !== window.location.origin) {
            window.location.href = destination.href;
            return;
        }

        // Sama kotwica na tej samej stronie nie wymaga przeładowania.
        if (
            destination.pathname === window.location.pathname &&
            destination.search === window.location.search &&
            destination.hash
        ) {
            history.pushState({}, '', destination.href);

            document.querySelector(
                decodeURIComponent(destination.hash)
            )?.scrollIntoView({ behavior: 'smooth' });

            return;
        }

        try {
            const response = await fetch(destination.href);

            if (!response.ok) {
                throw new Error(`Błąd strony: ${response.status}`);
            }

            const html = await response.text();
            const parsedDocument = new DOMParser().parseFromString(
                html,
                'text/html'
            );

            closeTransientUI();

            const persistentElements = getPersistentElements();

            // Zachowujemy żywy odtwarzacz audio i skrypt nawigacji.
            document.body.replaceChildren(
                ...persistentElements
            );

            const newBodyNodes = Array.from(parsedDocument.body.childNodes)
                .filter(node => {
                    if (node.nodeType !== Node.ELEMENT_NODE) return true;

                    return !node.matches(
                        '.music-player, script[src*="site-navigation.js"]'
                    );
                })
                .map(node => document.importNode(node, true));

            document.body.append(...newBodyNodes);

            document.title = parsedDocument.title || 'CLAUDIE';

            const newDescription = parsedDocument.querySelector(
                'meta[name="description"]'
            );
            let currentDescription = document.querySelector(
                'meta[name="description"]'
            );

            if (newDescription) {
                if (!currentDescription) {
                    currentDescription = document.createElement('meta');
                    currentDescription.name = 'description';
                    document.head.appendChild(currentDescription);
                }

                currentDescription.content = newDescription.content;
            }

            if (addHistory) {
                history.pushState({}, '', destination.href);
            }

            await runPageScripts(parsedDocument);

            if (destination.hash) {
                requestAnimationFrame(() => {
                    document.querySelector(
                        decodeURIComponent(destination.hash)
                    )?.scrollIntoView();
                });
            } else {
                window.scrollTo(0, 0);
            }
        } catch (error) {
            console.error(
                'Nie udało się przejść bez przeładowania strony:',
                error
            );

            // Awaryjnie zwykłe przejście, jeśli pobranie strony nie działa.
            window.location.href = destination.href;
        }
    }

    // Jedna obsługa kliknięć dla linków na wszystkich podstronach.
    document.addEventListener('click', event => {
        const link = event.target.closest('a');

        if (!isInternalPageLink(link)) return;

        if (
            event.defaultPrevented ||
            event.button !== 0 ||
            event.metaKey ||
            event.ctrlKey ||
            event.shiftKey ||
            event.altKey
        ) {
            return;
        }

        event.preventDefault();
        navigateTo(link.href);
    });

    // Obsługa przycisków Wstecz i Dalej w przeglądarce.
    window.addEventListener('popstate', () => {
        navigateTo(window.location.href, false);
    });
})();

