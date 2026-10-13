(() => {
    const gallery = document.querySelector('.photo-gallery');

    // Jeśli dana strona nie ma galerii, nie uruchamiaj lightboxa.
    if (!gallery) return;

    const items = Array.from(gallery.querySelectorAll('.photo-item'));
    if (!items.length) return;

    let currentIndex = 0;
    let previousFocus = null;
    let touchStartX = 0;
    let touchStartY = 0;

    // Tworzymy podgląd raz, wspólnie dla wszystkich zdjęć galerii.
    const lightbox = document.createElement('div');
    lightbox.className = 'lightbox';
    lightbox.setAttribute('role', 'dialog');
    lightbox.setAttribute('aria-modal', 'true');
    lightbox.setAttribute('aria-label', 'Powiększone zdjęcie');

    lightbox.innerHTML = `
        <button class="lightbox-close" type="button"
            aria-label="Zamknij podgląd">&times;</button>

        <button class="lightbox-arrow lightbox-prev" type="button"
            aria-label="Poprzednie zdjęcie">&#8592;</button>

        <img class="lightbox-image" alt="">

        <button class="lightbox-arrow lightbox-next" type="button"
            aria-label="Następne zdjęcie">&#8594;</button>

        <div class="lightbox-counter" aria-live="polite"></div>
    `;

    document.body.appendChild(lightbox);

    const image = lightbox.querySelector('.lightbox-image');
    const closeButton = lightbox.querySelector('.lightbox-close');
    const prevButton = lightbox.querySelector('.lightbox-prev');
    const nextButton = lightbox.querySelector('.lightbox-next');
    const counter = lightbox.querySelector('.lightbox-counter');

    function getImageSource(item) {
        return item.getAttribute('href')
            || item.querySelector('img')?.getAttribute('src')
            || '';
    }

    function showImage(index) {
        currentIndex = (index + items.length) % items.length;

        const item = items[currentIndex];
        const thumbnail = item.querySelector('img');

        image.src = getImageSource(item);
        image.alt = thumbnail?.alt || 'Zdjęcie z galerii';

        counter.textContent = `${currentIndex + 1} / ${items.length}`;

        // Wczytaj wcześniej sąsiednie zdjęcia, aby ułatwić przewijanie.
        [currentIndex - 1, currentIndex + 1].forEach(neighbor => {
            const source = getImageSource(items[
                (neighbor + items.length) % items.length
            ]);

            if (source) {
                const preload = new Image();
                preload.src = source;
            }
        });
    }

    function openLightbox(index) {
        previousFocus = document.activeElement;

        showImage(index);
        lightbox.classList.add('is-open');
        document.body.classList.add('lightbox-open');

        closeButton.focus();
    }

    function closeLightbox() {
        if (!lightbox.classList.contains('is-open')) return;

        lightbox.classList.remove('is-open');
        document.body.classList.remove('lightbox-open');

        image.removeAttribute('src');
        image.alt = '';

        if (previousFocus && typeof previousFocus.focus === 'function') {
            previousFocus.focus();
        }
    }

    items.forEach((item, index) => {
        item.addEventListener('click', event => {
            // Nie otwieraj pliku zdjęcia w nowej lokalizacji.
            event.preventDefault();
            openLightbox(index);
        });
    });

    prevButton.addEventListener('click', () => {
        showImage(currentIndex - 1);
    });

    nextButton.addEventListener('click', () => {
        showImage(currentIndex + 1);
    });

    closeButton.addEventListener('click', closeLightbox);

    // Kliknięcie ciemnego tła zamyka podgląd.
    lightbox.addEventListener('click', event => {
        if (event.target === lightbox) {
            closeLightbox();
        }
    });

    // Obsługa klawiatury.
    document.addEventListener('keydown', event => {
        if (!lightbox.classList.contains('is-open')) return;

        if (event.key === 'Escape') {
            event.preventDefault();
            closeLightbox();
        } else if (event.key === 'ArrowLeft') {
            event.preventDefault();
            showImage(currentIndex - 1);
        } else if (event.key === 'ArrowRight') {
            event.preventDefault();
            showImage(currentIndex + 1);
        } else if (event.key === 'Tab') {
            // Utrzymaj fokus wewnątrz otwartego podglądu.
            const controls = [
                closeButton,
                prevButton,
                nextButton
            ];

            const first = controls[0];
            const last = controls[controls.length - 1];

            if (event.shiftKey && document.activeElement === first) {
                event.preventDefault();
                last.focus();
            } else if (
                !event.shiftKey &&
                document.activeElement === last
            ) {
                event.preventDefault();
                first.focus();
            }
        }
    });

    // Przewijanie zdjęć gestem przesunięcia palcem.
    lightbox.addEventListener('touchstart', event => {
        if (event.touches.length !== 1) return;

        touchStartX = event.touches[0].clientX;
        touchStartY = event.touches[0].clientY;
    }, { passive: true });

    lightbox.addEventListener('touchend', event => {
        if (!lightbox.classList.contains('is-open')) return;
        if (event.changedTouches.length !== 1) return;

        const deltaX = event.changedTouches[0].clientX - touchStartX;
        const deltaY = event.changedTouches[0].clientY - touchStartY;

        // Reaguj na wyraźny ruch poziomy, nie na zwykłe dotknięcie.
        if (Math.abs(deltaX) < 50 || Math.abs(deltaX) < Math.abs(deltaY)) {
            return;
        }

        showImage(deltaX < 0 ? currentIndex + 1 : currentIndex - 1);
    }, { passive: true });
})();