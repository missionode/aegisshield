from aegisshield.logic import calculate_health_score

def test_perfect_health_score():
    """Verify that a perfect score (100) is given for a secure domain."""
    ssl_results = {"status": "secure", "issuer": "DigiCert", "version": "TLSv1.3"}
    header_results = {"hsts": True, "csp": True, "x_frame": True, "x_content_type": True}
    port_results = {80: "open", 443: "open"}
    
    score = calculate_health_score(ssl_results, header_results, port_results)
    assert score == 100

def test_poor_health_score_ssl_error():
    """Verify that the score is lower for a domain with an SSL error."""
    ssl_results = {"status": "error", "message": "SSL verification failed"}
    header_results = {"hsts": False, "csp": False, "x_frame": False, "x_content_type": False}
    port_results = {80: "open", 443: "closed"}
    
    score = calculate_health_score(ssl_results, header_results, port_results)
    # 0 + 0 + 10 (for port 80 open)
    assert score == 10

def test_partial_health_score_missing_headers():
    """Verify that the score is partial for a domain with SSL but missing some headers."""
    ssl_results = {"status": "secure"}
    header_results = {"hsts": True, "csp": False, "x_frame": True, "x_content_type": False}
    port_results = {80: "open", 443: "open"}
    
    # SSL: 40
    # Headers: 20 (hsts: 10, x_frame: 10)
    # Ports: 20 (80: 10, 443: 10)
    # Total: 80
    score = calculate_health_score(ssl_results, header_results, port_results)
    assert score == 80
