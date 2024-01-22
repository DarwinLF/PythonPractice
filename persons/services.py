from datetime import date

class CustomerService:
    @staticmethod
    def IsRentAvailable(customerId):
        from persons.models import Customer
        customer = Customer.objects.get(pk=customerId)
        customer = customer.CheckRentAvailability()

        if customer.status.name == 'Active Borrower':
            return True
        else:
            return False

    @staticmethod
    def CheckRentAvailability(customer):
        #import ipdb; ipdb.set_trace()
        from persons.models import CustomerStatus
        rents_due_for_customer = customer.rents_due.exclude(
            status__name = 'Returned')
        if rents_due_for_customer:
            oldest_rent_date = rents_due_for_customer.earliest(
                'rent_date').rent_date
            
            if (date.today() - oldest_rent_date).days > customer.credit_time:
                customer.status = CustomerStatus.objects.get(pk=5)
            elif customer.status.name == 'Suspended Borrowing Privileges':
                customer.status = CustomerStatus.objects.get(pk=1)
        elif customer.status.name == 'Suspended Borrowing Privileges':
            customer.status = CustomerStatus.objects.get(pk=1)

        customer.save()
            
        return customer
