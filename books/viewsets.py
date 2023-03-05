from django.db.models import Count, Avg
from rest_framework.viewsets import ModelViewSet

from books.models import Book, Author, Country, Order
from books.serializers import BookSerializer, AuthorSerializer, CountrySerializer, OrderSerializer
from hillel_django.permissions import IsSellerOrAdminOrReadOnly


class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('country').prefetch_related('authors')

    serializer_class = BookSerializer
    permission_classes = [IsSellerOrAdminOrReadOnly]


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all().annotate(books_count=Count('book'), average_price=Avg('book__price'))
    serializer_class = AuthorSerializer


class CountryViewSet(ModelViewSet):
    queryset = Country.objects.all().annotate(count_selled_books=Count('book__count_selled'))
    serializer_class = CountrySerializer


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
