export function initializeDigitalCore() {
    const canvas = document.querySelector("[data-digital-core]");
    const context = canvas?.getContext("2d", { alpha: true });
    if (!canvas || !context) return;

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const count = window.matchMedia("(max-width: 760px)").matches ? 48 : 84;
    const nodes = Array.from({ length: count }, (_, index) => {
        const ratio = (index + 0.5) / count;
        const latitude = Math.acos(1 - 2 * ratio);
        const longitude = Math.PI * (1 + Math.sqrt(5)) * index;
        return {
            x: Math.sin(latitude) * Math.cos(longitude),
            y: Math.cos(latitude),
            z: Math.sin(latitude) * Math.sin(longitude),
        };
    });
    const connections = [];
    nodes.forEach((node, index) => {
        for (let otherIndex = index + 1; otherIndex < nodes.length; otherIndex += 1) {
            const other = nodes[otherIndex];
            const deltaX = node.x - other.x;
            const deltaY = node.y - other.y;
            const deltaZ = node.z - other.z;
            if (deltaX * deltaX + deltaY * deltaY + deltaZ * deltaZ < 0.23) connections.push([index, otherIndex]);
        }
    });

    let width = 0;
    let height = 0;
    let pixelRatio = 1;
    let rotation = 0;
    let frame = 0;
    let lastFrame = 0;
    let inView = true;
    let resizeObserver;
    const projected = new Array(nodes.length);

    const resize = () => {
        const bounds = canvas.getBoundingClientRect();
        if (!bounds.width || !bounds.height) return;
        width = bounds.width;
        height = bounds.height;
        pixelRatio = Math.min(window.devicePixelRatio || 1, 1.5);
        canvas.width = Math.round(width * pixelRatio);
        canvas.height = Math.round(height * pixelRatio);
        context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
        if (reducedMotion) draw();
    };

    const draw = () => {
        if (!width || !height) return;
        context.clearRect(0, 0, width, height);
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) * 0.32;
        const cosine = Math.cos(rotation);
        const sine = Math.sin(rotation);

        const atmosphere = context.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius * 1.25);
        atmosphere.addColorStop(0, "rgba(45, 174, 225, .22)");
        atmosphere.addColorStop(0.52, "rgba(24, 91, 143, .11)");
        atmosphere.addColorStop(1, "rgba(8, 11, 16, 0)");
        context.fillStyle = atmosphere;
        context.fillRect(centerX - radius * 1.25, centerY - radius * 1.25, radius * 2.5, radius * 2.5);

        nodes.forEach((node, index) => {
            const rotatedX = node.x * cosine - node.z * sine;
            const rotatedZ = node.x * sine + node.z * cosine;
            const perspective = 2.8 / (2.8 - rotatedZ * 0.62);
            projected[index] = {
                x: centerX + rotatedX * radius * perspective,
                y: centerY + node.y * radius * perspective,
                depth: rotatedZ,
            };
        });

        context.lineWidth = 0.7;
        connections.forEach(([firstIndex, secondIndex]) => {
            const first = projected[firstIndex];
            const second = projected[secondIndex];
            const depth = (first.depth + second.depth) / 2;
            context.strokeStyle = `rgba(74, 231, 255, ${0.12 + (depth + 1) * 0.18})`;
            context.beginPath();
            context.moveTo(first.x, first.y);
            context.lineTo(second.x, second.y);
            context.stroke();
        });

        projected.forEach((point) => {
            const size = point.depth > 0 ? 2 : 1.2;
            context.fillStyle = point.depth > 0 ? "rgba(155, 249, 255, .98)" : "rgba(112, 164, 255, .58)";
            context.beginPath();
            context.arc(point.x, point.y, size, 0, Math.PI * 2);
            context.fill();
        });

        const nucleus = context.createRadialGradient(centerX, centerY, 0, centerX, centerY, radius * 0.22);
        nucleus.addColorStop(0, "rgba(188, 252, 255, .82)");
        nucleus.addColorStop(0.12, "rgba(74, 231, 255, .3)");
        nucleus.addColorStop(1, "rgba(74, 231, 255, 0)");
        context.fillStyle = nucleus;
        context.beginPath();
        context.arc(centerX, centerY, radius * 0.22, 0, Math.PI * 2);
        context.fill();
    };

    const animate = (timestamp) => {
        frame = 0;
        if (!inView || reducedMotion) return;
        if (timestamp - lastFrame >= 33) {
            rotation += 0.003;
            draw();
            lastFrame = timestamp;
        }
        frame = window.requestAnimationFrame(animate);
    };

    const start = () => {
        if (!reducedMotion && inView && !frame) frame = window.requestAnimationFrame(animate);
    };

    if ("ResizeObserver" in window) {
        resizeObserver = new ResizeObserver(resize);
        resizeObserver.observe(canvas);
    } else {
        window.addEventListener("resize", resize, { passive: true });
    }

    if ("IntersectionObserver" in window) {
        const visibilityObserver = new IntersectionObserver(([entry]) => {
            inView = entry.isIntersecting;
            if (inView) start();
            else if (frame) {
                window.cancelAnimationFrame(frame);
                frame = 0;
            }
        });
        visibilityObserver.observe(canvas);
    }

    resize();
    draw();
    start();
}