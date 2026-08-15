from django.http import JsonResponse
from django.shortcuts import render


def _is_api_request(request):
    return request.path.startswith("/api/")


def error_400(request, exception=None):
    if _is_api_request(request):
        return JsonResponse({"error": {"code": "bad_request", "message": "The request could not be processed."}}, status=400)
    return render(request, "400.html", status=400)


def error_403(request, exception=None):
    if _is_api_request(request):
        return JsonResponse({"error": {"code": "permission_denied", "message": "You do not have permission to access this resource."}}, status=403)
    return render(request, "403.html", status=403)


def error_404(request, exception=None):
    if _is_api_request(request):
        return JsonResponse({"error": {"code": "not_found", "message": "The requested resource was not found."}}, status=404)
    return render(request, "404.html", status=404)


def error_500(request):
    if _is_api_request(request):
        return JsonResponse({"error": {"code": "internal_error", "message": "An internal error occurred."}}, status=500)
    return render(request, "500.html", status=500)
