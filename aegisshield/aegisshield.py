"""Home page implementation for AegisShield."""

import reflex as rx

from rxconfig import config


class State(rx.State):
    """The app state."""
    domain: str = ""
    is_scanning: bool = False

    def start_diagnosis(self):
        """Trigger the diagnosis process."""
        if not self.domain:
            return
        self.is_scanning = True
        # Future: Trigger background scan


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
