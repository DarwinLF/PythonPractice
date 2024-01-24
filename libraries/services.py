from datetime import date

class BookService:
    @staticmethod
    def adjust_status(bookId):
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
    
class RentService:
    @staticmethod
    def update_status(rent):
        from libraries.models import RentStatus

        if rent.due_date < date.today() and rent.status.name == 'Checked Out':
            rent.status = RentStatus.objects.get(name='Overdue')

        rent.save()
        rent.customer = rent.customer.update_status()

        return rent
