from datetime import date

class CustomerService:
    @staticmethod
    def IsRentAvailable(customerId):
        from persons.models import Customer
        customer = Customer.objects.get(pk=customerId)
        customer = CustomerService.CheckRentAvailability(customer)

        if customer.status.name == 'Active Borrower':
            return True
        else:
            return False

    @staticmethod
    def CheckRentAvailability(customer):
        #import ipdb; ipdb.set_trace()
        rents_due_for_customer = customer.rents_due.exclude(status__name = 'Returned')
        if rents_due_for_customer:
            from persons.models import CustomerStatus
            oldest_rent_date = rents_due_for_customer.earliest('rent_date').rent_date
            
            if (oldest_rent_date - date.today()).days > customer.credit_time:
                customer.status = CustomerStatus.objects.get(pk=5)
            else:
                customer.status = CustomerStatus.objects.get(pk=1)

            customer.save()
            
        return customer
