import { initializeTheme } from "./theme.js";
import { initializeAnimations } from "./animations.js";
import { initializeCursor } from "./cursor.js";
import { initializeDigitalCore } from "./digital-core.js";
import { initializeNavigation } from "./navigation.js";
import { initializeScroll } from "./scroll.js";
import { initializeDashboard } from "./dashboard.js";

// Initialize Theme first to prevent any visual delay
initializeTheme();
initializeAnimations();
initializeCursor();
initializeDigitalCore();
initializeNavigation();
initializeScroll();
initializeDashboard();
