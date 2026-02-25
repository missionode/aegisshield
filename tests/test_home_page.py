import reflex as rx
import pytest
from aegisshield.aegisshield import index, State

def test_home_page_branding():
    """Verify that the home page contains AegisShield branding."""
    component = index()
    assert "AegisShield" in str(component)

def test_home_page_input_field():
    """Verify that the home page has a domain input field."""
    component = index()
    assert "Input" in str(component)

def test_home_page_diagnose_button():
    """Verify that the home page has a Diagnose button."""
    component = index()
    assert "Button" in str(component)
    assert "Diagnose" in str(component)

@pytest.mark.asyncio
async def test_state_start_diagnosis():
    """Verify the state transition for starting a diagnosis."""
    # Reflex state testing involves creating an instance
    state = State()
    assert state.is_scanning is False
    assert state.domain == ""
    
    # Try with empty domain
    state.start_diagnosis()
    assert state.is_scanning is False
    
    # Try with domain
    state.domain = "google.com"
    state.start_diagnosis()
    assert state.is_scanning is True
