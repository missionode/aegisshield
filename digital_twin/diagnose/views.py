from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Scan, Disease
from .utils import analyze_plant_image
from django.http import JsonResponse
import time

class DashboardView(LoginRequiredMixin, ListView):
    model = Scan
    template_name = 'diagnose/dashboard.html'
    context_object_name = 'scans'
    paginate_by = 5

    def get_queryset(self):
        # Prioritize favorites, then by date
        return Scan.objects.filter(user=self.request.user).order_by('-is_favorite', '-date')

class ScannerView(LoginRequiredMixin, TemplateView):
    template_name = 'diagnose/scanner.html'

    def post(self, request, *args, **kwargs):
        image = request.FILES.get('image')
        if image:
            scan = Scan.objects.create(user=request.user, image=image)
            return redirect('diagnose:analysis', scan_id=scan.id)
        return self.get(request)

class AnalysisView(LoginRequiredMixin, DetailView):
    model = Scan
    template_name = 'diagnose/analysis.html'
    pk_url_kwarg = 'scan_id'

def start_analysis(request, scan_id):
    try:
        print(f"Starting analysis for scan {scan_id}")
        scan = get_object_or_404(Scan, id=scan_id, user=request.user)
        
        # Call Gemini
        result = analyze_plant_image(scan.image.path)
        print(f"Gemini result: {result}")

        # Format helper for list/string content
        def format_content(content):
            if isinstance(content, list):
                return "\n".join([f"• {item}" if not item.startswith("•") else item for item in content])
            
            # Handle HTML-like strings returned by AI
            if isinstance(content, str):
                import re
                # Replace <li> with bullets
                content = re.sub(r'<li>', '\n• ', content)
                # Remove all other tags
                content = re.sub(r'<[^>]+>', '', content)
                # Clean up multiple newlines
                content = content.strip()
                
            return content
        
        imm_action = format_content(result.get('immediate_action', ''))
        lt_care = format_content(result.get('long_term_care', ''))
        
        # Save/Update Disease info
        disease, created = Disease.objects.get_or_create(
            name=result['disease_name'],
            defaults={
                'description': result.get('description', ''),
                'immediate_action': imm_action,
                'long_term_care': lt_care,
                'recommended_products': result.get('recommended_products', [])
            }
        )
        
        # If not created, update the fields anyway to ensure they aren't empty
        if not created:
            print(f"Disease {disease.name} already exists, updating fields.")
            disease.description = result.get('description', disease.description)
            disease.immediate_action = imm_action
            disease.long_term_care = lt_care
            disease.recommended_products = result.get('recommended_products', disease.recommended_products)
            disease.save()
        else:
            print(f"Created new disease entry: {disease.name}")
        
        scan.disease = disease
        
        # Normalize confidence to 0-100
        conf = result.get('confidence', 0.0)
        if conf <= 1.0:
            conf *= 100
        scan.confidence = conf
        
        scan.save()
        
        print(f"Scan {scan.id} updated successfully. Redirecting to result page.")
        return JsonResponse({'status': 'success', 'redirect_url': f'/diagnose/result/{scan.id}/'})
    except Exception as e:
        import traceback
        print(f"Analysis Error: {e}")
        traceback.print_exc()
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class ResultView(LoginRequiredMixin, DetailView):
    model = Scan
    template_name = 'diagnose/result.html'
    pk_url_kwarg = 'scan_id'

def toggle_favorite(request, scan_id):
    if request.method == "POST":
        scan = get_object_or_404(Scan, id=scan_id, user=request.user)
        scan.is_favorite = not scan.is_favorite
        scan.save()
        return JsonResponse({'status': 'success', 'is_favorite': scan.is_favorite})
    return JsonResponse({'status': 'error'}, status=400)