export function initializeScroll() {
    const progress = document.querySelector(".scroll-progress span");
    const header = document.querySelector(".site-header");
    const visual = document.querySelector("[data-tilt]");
    const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
    let scrollFrame = 0;

    const updateScroll = () => {
        const available = document.documentElement.scrollHeight - window.innerHeight;
        const ratio = available > 0 ? window.scrollY / available : 0;
        if (progress) progress.style.transform = `scaleX(${Math.min(1, Math.max(0, ratio))})`;
        if (header) header.classList.toggle("is-scrolled", window.scrollY > 24);
        scrollFrame = 0;
    };

    window.addEventListener("scroll", () => {
        if (scrollFrame) return;
        scrollFrame = window.requestAnimationFrame(updateScroll);
    }, { passive: true });
    updateScroll();

    if (!visual || !finePointer || reduceMotion) return;
    visual.addEventListener("pointermove", (event) => {
        const bounds = visual.getBoundingClientRect();
        const offsetX = ((event.clientX - bounds.left) / bounds.width - 0.5) * 12;
        const offsetY = ((event.clientY - bounds.top) / bounds.height - 0.5) * 10;
        visual.style.setProperty("--parallax-x", `${offsetX}px`);
        visual.style.setProperty("--parallax-y", `${offsetY}px`);
    }, { passive: true });
    visual.addEventListener("pointerleave", () => {
        visual.style.setProperty("--parallax-x", "0px");
        visual.style.setProperty("--parallax-y", "0px");
    });
}