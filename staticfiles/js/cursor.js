export function initializeCursor() {
    const cursor = document.querySelector(".custom-cursor");
    const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)").matches;
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (!cursor || !finePointer || reducedMotion) return;

    document.documentElement.classList.add("has-custom-cursor");
    let frame = 0;
    let pointerX = 0;
    let pointerY = 0;

    document.addEventListener("pointermove", (event) => {
        pointerX = event.clientX;
        pointerY = event.clientY;
        if (frame) return;
        frame = window.requestAnimationFrame(() => {
            cursor.style.transform = `translate3d(${pointerX}px, ${pointerY}px, 0) translate(-50%, -50%)`;
            cursor.classList.add("is-visible");
            frame = 0;
        });
    }, { passive: true });

    document.addEventListener("pointerover", (event) => {
        const target = event.target.closest("a, button, [data-magnetic]");
        cursor.classList.toggle("is-hovering", Boolean(target));
        cursor.classList.toggle("is-cta", Boolean(target?.matches("[data-magnetic]")));
    });

    document.addEventListener("pointerleave", () => cursor.classList.remove("is-visible"));

    document.querySelectorAll("[data-magnetic]").forEach((element) => {
        element.addEventListener("pointermove", (event) => {
            const bounds = element.getBoundingClientRect();
            const offsetX = (event.clientX - bounds.left - bounds.width / 2) * 0.08;
            const offsetY = (event.clientY - bounds.top - bounds.height / 2) * 0.12;
            element.style.transform = `translate3d(${offsetX}px, ${offsetY}px, 0)`;
        });
        element.addEventListener("pointerleave", () => { element.style.transform = ""; });
    });
}