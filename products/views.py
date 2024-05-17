from django.contrib import messages
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from .forms import AddReviewForm, ReviewUpdateForm
from .models import Books, Review, CategoryBooks
from django.urls import reverse_lazy
# Create your views here.


class BookListView(View):
    def get(self, request):
        book = Books.objects.all().order_by('-id')
        return render(request, 'book/book_list.html', {'book': book})

# class BookListView(ListView):
#     model = Books
#     template_name = 'book/book_list.html'
#     context_object_name = 'book'

class BookDetailView(View):
    def get(self, request, pk):
        book = Books.objects.get(pk=pk)
        reviews = Review.objects.filter(book=pk)
        category_books = Books.objects.filter(category=book.category.pk)
        context = {
            'book': book,
            'reviews': reviews,
            'category_books': category_books
        }
        return render(request, 'book/book_detail.html', context=context)



class BookCreateView(CreateView):
    model = Books
    template_name = 'book/book_create.html'
    fields = '__all__'
    success_url = reverse_lazy('products:book-list')


class BookDeleteView(DeleteView):
    model = Books
    template_name = 'book/book_delete.html'
    success_url = reverse_lazy('products:book-list')


class AddReviewView(LoginRequiredMixin, View):
    def get(self, request, pk):
        books = Books.objects.get(pk=pk)
        add_review_form = AddReviewForm()
        context = {
            'books': books,
            'add_review_form': add_review_form
        }
        return render(request, 'book/add_review.html', context=context)

    def post(self, request, pk):
        books = Books.objects.get(pk=pk)
        add_review_form = AddReviewForm(request.POST)
        if add_review_form.is_valid():
            review = Review.objects.create(
                comment=add_review_form.cleaned_data['comment'],
                book=books,
                user=request.user,
                star_given=add_review_form.cleaned_data['star_given']
            )

            review.save()
            messages.success(request, "Review added successfully.")
            return redirect('products:book-detail', pk=pk)
        else:
            messages.error(request, "Failed to add review. Please check the form.")
            return render(request, 'book/add_review.html', {'books': books, 'add_review_form': add_review_form})


class ReviewUpdateView(View):
    def get(self, request, pk):
        review = Review.objects.get(pk=pk)
        update_review_form = ReviewUpdateForm(instance=review)
        context = {
            'update_review_form': update_review_form
        }
        return render(request, 'book/review_update.html', context=context)

    def post(self, request, pk):
        review = Review.objects.get(pk=pk)
        update_review_form = ReviewUpdateForm(request.POST, instance=review)
        if update_review_form.is_valid():
            # Set the book_id before saving
            update_review = update_review_form.save(commit=False)
            update_review.book_id = review.book_id
            update_review.save()
            return redirect('products:book-detail', pk=review.book_id)
        else:
            return render(request, 'book/review_update.html', {'update_review_form': update_review_form})



class CategoriesListView(View):
    def get(self, request):
        category = CategoryBooks.objects.all()

        return render(request, 'book/products.html', {'categorys': category})










