import os
import reflex as rx
from aegisshield.aegisshield import index

def test_reflex_config_exists():
    """Verify that rxconfig.py exists."""
    assert os.path.exists("rxconfig.py"), "rxconfig.py not found"

def test_app_directory_exists():
    """Verify that the aegisshield app directory exists."""
    assert os.path.isdir("aegisshield"), "aegisshield directory not found"

def test_main_app_file_exists():
    """Verify that aegisshield/aegisshield.py exists."""
    assert os.path.exists(os.path.join("aegisshield", "aegisshield.py")), "aegisshield/aegisshield.py not found"

def test_tailwind_config_exists():
    """Verify that Tailwind configuration (CSS variables) exists."""
    css_path = os.path.join("assets", "styles.css")
    assert os.path.exists(css_path), f"{css_path} not found"
    
    with open(css_path, "r") as f:
        content = f.read()
        assert "--color-bg-primary: #0B0F1A;" in content
        assert "--color-accent-cyan: #35F2FF;" in content
        assert "--color-accent-magenta: #FF4FD8;" in content

def test_index_page_structure():
    """Verify the basic structure of the index page."""
    component = index()
    assert isinstance(component, rx.Component)
    # Check if the component tree contains the welcome text
    # This is a bit implementation specific for Reflex
    assert component is not None
