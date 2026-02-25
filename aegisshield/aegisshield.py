"""Home page implementation for AegisShield."""

import reflex as rx
import asyncio
from typing import Dict, Any

from rxconfig import config
from .scanner import AsyncScanner
from .logic import calculate_health_score


class State(rx.State):
    """The app state."""
    domain: str = ""
    is_scanning: bool = False
    health_score: int = 0
    scan_status: str = "Ready for diagnosis"
    
    # Detailed Results
    ssl_result: Dict[str, Any] = {}
    header_result: Dict[str, Any] = {}
    port_result: Dict[str, Any] = {}

    async def start_diagnosis(self):
        """Trigger the asynchronous diagnosis process."""
        if not self.domain:
            return
            
        # Reset state
        self.is_scanning = True
        self.health_score = 0
        self.ssl_result = {}
        self.header_result = {}
        self.port_result = {}
        
        scanner = AsyncScanner(timeout=5.0)
        
        # 1. SSL Analysis
        self.scan_status = "Verifying SSL/TLS Certificate..."
        yield
        self.ssl_result = await scanner.verify_ssl(self.domain)
        
        # 2. Header Analysis
        self.scan_status = "Analyzing Security Headers..."
        yield
        self.header_result = await scanner.analyze_headers(self.domain)
        
        # 3. Port Scanning
        self.scan_status = "Probing External Footprint..."
        yield
        self.port_result = await scanner.scan_ports(self.domain)
        
        # 4. Final Calculation
        self.scan_status = "Finalizing Expert Assessment..."
        self.health_score = calculate_health_score(
            self.ssl_result, 
            self.header_result, 
            self.port_result
        )
        yield
        
        await asyncio.sleep(0.5)
        self.scan_status = "Diagnosis Complete"
        self.is_scanning = False


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
                    class_name="h-full bg-gradient-to-r from-accent-magenta to-accent-cyan rounded-full shadow-[0_0_10px_rgba(53,242,255,0.5)] transition-all duration-500",
                    width=f"{State.health_score}%",
                ),
                class_name="w-full h-2 bg-white/10 rounded-full overflow-hidden",
            ),
            width="100%",
            spacing="2",
        ),
        # Scan Results Panel
        rx.box(
            rx.vstack(
                rx.text(State.scan_status, class_name="text-soft-glow-blue/70 text-xs font-mono"),
                rx.divider(class_name="border-white/5 my-2"),
                
                # SSL Result
                rx.hstack(
                    rx.text("SSL Certificate:", class_name="text-white/40 text-xs"),
                    rx.cond(
                        State.ssl_result["status"] == "secure",
                        rx.text("SECURE", class_name="text-success-green text-xs font-bold"),
                        rx.text("ERROR/MISSING", class_name="text-warning-pink text-xs font-bold"),
                    ),
                    justify="between", width="100%"
                ),
                
                # Header Result (HSTS)
                rx.hstack(
                    rx.text("HSTS Protection:", class_name="text-white/40 text-xs"),
                    rx.cond(
                        State.header_result["hsts"],
                        rx.text("ENABLED", class_name="text-success-green text-xs font-bold"),
                        rx.text("DISABLED", class_name="text-warning-pink text-xs font-bold"),
                    ),
                    justify="between", width="100%"
                ),
                
                # Port Result (443)
                rx.hstack(
                    rx.text("HTTPS Port (443):", class_name="text-white/40 text-xs"),
                    rx.cond(
                        State.port_result["443"] == "open",
                        rx.text("OPEN", class_name="text-success-green text-xs font-bold"),
                        rx.text("CLOSED", class_name="text-warning-pink text-xs font-bold"),
                    ),
                    justify="between", width="100%"
                ),
                
                align_items="start",
                width="100%",
            ),
            class_name="mt-6 p-6 w-full rounded-xl bg-midnight-panel/60 border border-white/10 backdrop-blur-glass",
        ),
        align_items="start",
        width="100%",
        max_width="28rem",
        class_name="p-8 rounded-2xl bg-midnight-panel/40 border border-white/5 backdrop-blur-glass shadow-2xl mt-12 mb-12",
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
                                type_="text",
                                value=State.domain,
                                on_change=State.set_domain,
                                px="6",
                                py="4",
                                class_name="bg-midnight-panel/80 border border-white/20 text-white placeholder:text-white/30 rounded-lg w-96 focus:outline-none focus:border-accent-cyan/50 backdrop-blur-glass",
                                style={"color": "white"},
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
                    State.is_scanning | (State.scan_status == "Diagnosis Complete"),
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
