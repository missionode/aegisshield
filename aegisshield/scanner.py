import asyncio
import ssl
import socket
import httpx
from typing import Dict, Any, List

class AsyncScanner:
    """Asynchronous engine for domain security diagnosis."""

    def __init__(self, timeout: float = 5.0):
        self.timeout = timeout

    async def verify_ssl(self, domain: str) -> Dict[str, Any]:
        """Verify SSL/TLS certificate for a domain."""
        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        "status": "secure",
                        "issuer": dict(x[0] for x in cert['issuer'])['organizationName'],
                        "version": ssock.version(),
                    }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def analyze_headers(self, domain: str) -> Dict[str, Any]:
        """Analyze security headers of a domain."""
        url = f"https://{domain}"
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                headers = response.headers
                return {
                    "hsts": "Strict-Transport-Security" in headers,
                    "csp": "Content-Security-Policy" in headers,
                    "x_frame": "X-Frame-Options" in headers,
                    "x_content_type": "X-Content-Type-Options" in headers,
                }
        except Exception as e:
            return {"status": "error", "message": str(e)}

    async def scan_ports(self, domain: str, ports: List[int] = [80, 443, 8080]) -> Dict[str, Any]:
        """Scan common ports for a domain."""
        results = {}
        for port in ports:
            try:
                # Basic non-intrusive connection check
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(domain, port),
                    timeout=2.0
                )
                results[port] = "open"
                writer.close()
                await writer.wait_closed()
            except:
                results[port] = "closed"
        return results
