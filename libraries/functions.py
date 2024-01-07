from libraries.models import Book, BookStatus

def AdjustStatusOfBook(bookId):
    book = Book.objects.get(pk=bookId)
    status = BookStatus.objects.all()
    if book.available == 0 and book.status == 'Available':
        book.status = status[1]
    elif book.available > 0 and book.status == 'Spent':
        book.status = status[0]

    book.save()