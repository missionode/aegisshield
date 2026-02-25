from typing import Dict, Any

def calculate_health_score(ssl_results: Dict[str, Any], header_results: Dict[str, Any], port_results: Dict[str, Any]) -> int:
    """
    Calculate a weighted security health score (0-100).
    
    Weights:
    - SSL Status: 40%
    - Security Headers: 40% (10% each for HSTS, CSP, X-Frame, X-Content-Type)
    - Port Footprint: 20% (10% each for 80, 443; -5% for unexpected open ports like 8080)
    """
    score = 0
    
    # 1. SSL Status (40 points)
    if ssl_results.get("status") == "secure":
        score += 40
        
    # 2. Security Headers (40 points)
    header_weights = {
        "hsts": 10,
        "csp": 10,
        "x_frame": 10,
        "x_content_type": 10
    }
    for header, weight in header_weights.items():
        if header_results.get(header):
            score += weight
            
    # 3. Port Footprint (20 points)
    # Ideally 80 and 443 are open, others are closed for a simple web domain
    if port_results.get(443) == "open":
        score += 10
    if port_results.get(80) == "open":
        score += 10
    
    # Penalties for other ports (simplified)
    for port, status in port_results.items():
        if port not in [80, 443] and status == "open":
            score -= 5
            
    return max(0, min(100, score))
