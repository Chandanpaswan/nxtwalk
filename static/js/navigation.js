export function initializeNavigation() {
    const toggle = document.querySelector(".menu-toggle");
    const navigation = document.querySelector(".primary-nav");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    if (toggle && navigation) {
        const closeMenu = (restoreFocus = false) => {
            toggle.setAttribute("aria-expanded", "false");
            toggle.setAttribute("aria-label", "Open navigation");
            navigation.classList.remove("is-open");
            document.body.classList.remove("menu-open");
            if (restoreFocus) toggle.focus();
        };

        toggle.addEventListener("click", () => {
            const willOpen = toggle.getAttribute("aria-expanded") !== "true";
            toggle.setAttribute("aria-expanded", String(willOpen));
            toggle.setAttribute("aria-label", willOpen ? "Close navigation" : "Open navigation");
            navigation.classList.toggle("is-open", willOpen);
            document.body.classList.toggle("menu-open", willOpen);
            if (willOpen) navigation.querySelector("a")?.focus();
        });

        navigation.addEventListener("click", (event) => {
            if (event.target.closest("a")) closeMenu();
        });

        document.addEventListener("keydown", (event) => {
            if (toggle.getAttribute("aria-expanded") !== "true") return;
            if (event.key === "Escape") {
                closeMenu(true);
                return;
            }
            if (event.key === "Tab") {
                const focusable = navigation.querySelectorAll("a[href], button:not([disabled])");
                const first = focusable[0];
                const last = focusable[focusable.length - 1];
                if (event.shiftKey && document.activeElement === first) {
                    event.preventDefault();
                    last?.focus();
                } else if (!event.shiftKey && document.activeElement === last) {
                    event.preventDefault();
                    first?.focus();
                }
            }
        });
    }

    const pageShell = document.querySelector(".page-shell");
    if (!pageShell || reducedMotion) return;

    document.addEventListener("click", (event) => {
        const link = event.target.closest("a[href]");
        if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
        if (link.target || link.hasAttribute("download")) return;

        const destination = new URL(link.href, window.location.href);
        if (destination.origin !== window.location.origin || destination.href === window.location.href) return;
        if (destination.pathname === window.location.pathname && destination.search === window.location.search && destination.hash) return;

        event.preventDefault();
        try {
            sessionStorage.setItem("nxtwalk-page-transition", "true");
        } catch {
            window.location.assign(destination.href);
            return;
        }
        pageShell.classList.add("is-leaving");
        window.setTimeout(() => window.location.assign(destination.href), 170);
    });
}