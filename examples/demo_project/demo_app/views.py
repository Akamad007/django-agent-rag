from django.http import JsonResponse

from django_agent_rag import ask


def ask_view(request):
    query = request.GET.get("q", "What is this project?")
    response = ask(query)
    return JsonResponse({"query": query, "response": response.text, "provider": response.provider})

