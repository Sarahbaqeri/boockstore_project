from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from .models import Book
from django.shortcuts import get_object_or_404
from .form import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required


class BookListView(generic.ListView):
    model = Book
    paginate_by = 4
    template_name = 'books/book_list.html'
    context_object_name = 'books'

#
# class BookDetailView(generic.DetailView):
#     model = Book
#     template_name = 'books/book_detail.html'


@login_required
def book_detail_view(request, pk):
    book = get_object_or_404(Book, pk=pk)
    comment = book.comments.all()

    if request.method == 'Post':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            print('hello')
            new_comment = comment_form.save(commit=False)
            new_comment.book = book
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, 'books/book_detail.html', {
        'book': book,
        'comments': comment,
        'comment_form': comment_form,
    })


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    fields = ['title', 'author', 'content', 'price']
    template_name = 'books/book_create.html'


class BookUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Book
    fields = ['title', 'author', 'content']
    template_name = 'books/book_update.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BookDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Book
    template_name = 'books/book_delete.html'
    success_url = reverse_lazy('book_list')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
