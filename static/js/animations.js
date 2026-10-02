export function initializeAnimations() {
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const revealElements = document.querySelectorAll(".reveal");

    if (reducedMotion || !("IntersectionObserver" in window)) {
        revealElements.forEach((element) => element.classList.add("is-visible"));
    } else {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        revealElements.forEach((element) => revealObserver.observe(element));

        const timelineObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    document.querySelectorAll("[data-scroll-step]").forEach((step) => step.classList.remove("is-active"));
                    entry.target.classList.add("is-active");
                }
            });
        }, { rootMargin: "-42% 0px -42% 0px" });

        document.querySelectorAll("[data-scroll-step]").forEach((step) => timelineObserver.observe(step));
    }

    const loader = document.querySelector(".site-loader");
    if (loader) {
        let hasVisited = false;
        try {
            hasVisited = sessionStorage.getItem("nxtwalk-intro-seen") === "true";
            sessionStorage.setItem("nxtwalk-intro-seen", "true");
        } catch {
            hasVisited = true;
        }

        const dismissLoader = () => loader.classList.add("is-done");
        if (hasVisited || reducedMotion) {
            dismissLoader();
        } else {
            window.setTimeout(dismissLoader, 520);
        }
    }

    const pageShell = document.querySelector(".page-shell");
    let hasTransition = false;
    try {
        hasTransition = sessionStorage.getItem("nxtwalk-page-transition") === "true";
        sessionStorage.removeItem("nxtwalk-page-transition");
    } catch {
        hasTransition = false;
    }
    if (pageShell && hasTransition && !reducedMotion) pageShell.classList.add("is-entering");
}