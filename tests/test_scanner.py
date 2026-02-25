import pytest
import asyncio
from aegisshield.scanner import AsyncScanner

@pytest.mark.asyncio
async def test_ssl_verification_real_domain():
    """Verify SSL for a real secure domain."""
    scanner = AsyncScanner(timeout=5.0)
    result = await scanner.verify_ssl("google.com")
    assert result["status"] == "secure"
    assert "Google" in result["issuer"] or "GTS" in result["issuer"]

@pytest.mark.asyncio
async def test_header_analysis_real_domain():
    """Verify security headers for a real domain."""
    scanner = AsyncScanner()
    result = await scanner.analyze_headers("google.com")
    # Google usually has some of these
    assert isinstance(result, dict)
    assert "hsts" in result

@pytest.mark.asyncio
async def test_port_scan_real_domain():
    """Verify port scanning for common ports."""
    scanner = AsyncScanner()
    result = await scanner.scan_ports("google.com", ports=[80, 443])
    assert result[80] == "open"
    assert result[443] == "open"

@pytest.mark.asyncio
async def test_ssl_verification_invalid_domain():
    """Verify SSL for an invalid domain handles error gracefully."""
    scanner = AsyncScanner(timeout=2.0)
    result = await scanner.verify_ssl("invalid-domain-12345.com")
    assert result["status"] == "error"
