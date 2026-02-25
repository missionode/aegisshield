"""Home page implementation for AegisShield."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""
    domain: str = ""
    is_scanning: bool = False
    health_score: int = 0
    scan_status: str = "Initializing analysis..."

    def start_diagnosis(self):
        """Trigger the diagnosis process."""
        if not self.domain:
            return
        self.is_scanning = True
        self.health_score = 0
        self.scan_status = "Analyzing SSL/TLS..."
        # Simulation for now
        return rx.call_script("console.log('Diagnosis started')")


def diagnosis_hud() -> rx.Component:
    """The skeleton for the Diagnosis HUD."""
    return rx.vstack(
        rx.heading(
            "Security Posture Diagnosis",
            class_name="text-2xl font-semibold text-accent-cyan tracking-tight mb-4",
        ),
        # Health Score Indicator
        rx.vstack(
            rx.hstack(
                rx.text("Health Score", class_name="text-white/80 text-sm font-medium"),
                rx.spacer(),
                rx.text(f"{State.health_score}%", class_name="text-accent-magenta font-bold"),
                width="100%",
            ),
            # Progress Bar (Linear Indicator)
            rx.box(
                rx.box(
                    class_name="h-full bg-gradient-to-r from-accent-magenta to-accent-cyan rounded-full shadow-[0_0_10px_rgba(53,242,255,0.5)]",
                    width=f"{State.health_score}%",
                ),
                class_name="w-full h-2 bg-white/10 rounded-full overflow-hidden",
            ),
            width="100%",
            spacing="2",
        ),
        # Scan Results Panel (Skeleton)
        rx.box(
            rx.vstack(
                rx.text(State.scan_status, class_name="text-soft-glow-blue/70 text-xs animate-pulse"),
                rx.divider(class_name="border-white/5 my-2"),
                rx.text("• SSL Certificate: Pending...", class_name="text-white/40 text-xs"),
                rx.text("• Security Headers: Pending...", class_name="text-white/40 text-xs"),
                rx.text("• Port Footprint: Pending...", class_name="text-white/40 text-xs"),
                align_items="start",
                width="100%",
            ),
            class_name="mt-6 p-6 w-full rounded-xl bg-midnight-panel/60 border border-white/10 backdrop-blur-glass",
        ),
        align_items="start",
        width="100%",
        max_width="28rem",
        class_name="p-8 rounded-2xl bg-midnight-panel/40 border border-white/5 backdrop-blur-glass shadow-2xl mt-12",
    )


def index() -> rx.Component:
    """The main landing page for AegisShield."""
    return rx.box(
        # Main Background
        rx.container(
            rx.vstack(
                # Header Branding
                rx.heading(
                    "AegisShield",
                    class_name="text-6xl font-bold tracking-widest text-transparent bg-clip-text bg-gradient-to-r from-accent-magenta to-accent-cyan drop-shadow-lg",
                    padding_top="10vh",
                ),
                rx.text(
                    "Predictive Autonomous Security Defender",
                    class_name="text-accent-cyan/80 text-xl tracking-wide",
                    margin_bottom="6vh",
                ),
                
                # Central Input Section
                rx.box(
                    rx.vstack(
                        rx.text(
                            "Enter Domain for Instant Diagnosis",
                            class_name="text-soft-glow-blue text-sm uppercase tracking-tighter mb-2",
                        ),
                        rx.hstack(
                            rx.input(
                                placeholder="example.com",
                                value=State.domain,
                                on_change=State.set_domain,
                                class_name="bg-midnight-panel/70 border border-white/10 text-white px-6 py-4 rounded-lg w-96 focus:outline-none focus:border-accent-cyan/50 backdrop-blur-glass",
                            ),
                            rx.button(
                                "Diagnose",
                                on_click=State.start_diagnosis,
                                loading=State.is_scanning,
                                class_name="bg-gradient-to-r from-accent-magenta to-accent-cyan text-bg-primary font-bold px-8 py-4 rounded-lg hover:scale-105 transition-transform duration-200 shadow-lg shadow-accent-cyan/20",
                            ),
                            spacing="4",
                        ),
                        align_items="center",
                        class_name="p-12 rounded-2xl bg-midnight-panel/40 border border-white/5 backdrop-blur-glass shadow-2xl",
                    ),
                    class_name="relative",
                ),
                
                # Conditional HUD (Skeleton)
                rx.cond(
                    State.is_scanning,
                    diagnosis_hud(),
                ),
                
                # Sub-text
                rx.text(
                    "Analyze SSL, Headers, and Port Footprint instantly.",
                    class_name="text-white/40 text-xs mt-8",
                ),
                
                spacing="4",
                justify="center",
                align_items="center",
                min_height="100vh",
            ),
            size="3",
        ),
        class_name="bg-bg-primary min-h-screen selection:bg-accent-magenta selection:text-white",
    )


app = rx.App(
    stylesheets=[
        "styles.css",
    ],
)
app.add_page(index)
