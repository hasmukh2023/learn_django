from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from .models import Book

# Create your views here.

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        total_books = Book.objects.filter(user=user).count()
        books_read = Book.objects.filter(user=user, reading_status='completed').count()
        currently_reading = Book.objects.filter(user=user, reading_status='reading').count()

        stats = {
            'totalBooks': total_books,
            'booksRead': books_read,
            'currentlyReading': currently_reading
        }
        
        return Response(stats)
