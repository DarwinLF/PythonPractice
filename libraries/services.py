class BookService:
    @staticmethod
    def AdjustStatusOfBook(bookId):
        from libraries.models import Book, BookStatus
        book = Book.objects.get(pk=bookId)
        status = BookStatus.objects.all()

        #import ipdb; ipdb.set_trace()

        #if the book is not available and the status is available
        if book.available() == 0 and book.status.name == 'Available':
            book.status = status[1]
        #if the book is available and the status is spent
        elif book.available() > 0 and book.status.name == 'Spent':
            #print(status[0])
            book.status = status[0]

        book.save()