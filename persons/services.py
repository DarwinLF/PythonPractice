from datetime import date

class CustomerService:
    @staticmethod
    def is_rent_available(customerId):
        from persons.models import Customer
        customer = Customer.objects.get(pk=customerId)
        customer = customer.update_status()

        if customer.status.name == 'Active Borrower':
            return True
        else:
            return False

    @staticmethod
    def update_status(customer):
        #import ipdb; ipdb.set_trace()
        from persons.models import CustomerStatus
        rents_due_for_customer = customer.rents_due.exclude(
            status__name = 'Returned')
        if rents_due_for_customer:
            oldest_rent_date = rents_due_for_customer.earliest(
                'rent_date').rent_date
            
            if (date.today() - oldest_rent_date).days > customer.credit_time:
                customer.status = CustomerStatus.objects.get(
                    name='Suspended Borrowing Privileges')
            elif customer.status.name == 'Suspended Borrowing Privileges':
                customer.status = CustomerStatus.objects.get(
                    name='Active Borrower')
        elif customer.status.name == 'Suspended Borrowing Privileges':
            customer.status = CustomerStatus.objects.get(
                name='Active Borrower')

        rents_overdue = rents_due_for_customer.filter(status__name='Overdue')
        if rents_overdue:
            customer.status = CustomerStatus.objects.get(
                name='Overdue Materials')
        elif customer.status.name == 'Overdue Materials':
            customer.status = CustomerStatus.objects.get(
                name='Active Borrower')


        customer.save()
            
        return customer
