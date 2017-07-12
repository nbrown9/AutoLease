class Lease(object):

    def __init__(self):
        self.fields = dict.fromkeys(['Owner', 'Date', 't_name', 't_name2', 'Apartment', 'Unit', 'City', 'Zip', 'child_count', 'lease_length', 
        'start_date', 'end_date', 'Rent', 'pet_fee', 'sec_dep', '2monthrent'])
    
    def setLeaseParams(self, leasefield):
        self.fields = leasefield
        
    def getLeaseParams(self):
        return self.fields