class Test:
    def __init__(self, companies=None, start_date=None, end_date=None):
        if companies is None:
            self.companies = []
        else:
            self.companies = companies

        self.start_date = start_date
        self.end_date = end_date

    def get_comp_list(self):
        comp_input = input("Enter the companies to test separated by spaces: ")
        # split into list
        self.companies = comp_input.split()

    def get_start_date(self):
        self.start_date = input("Enter start date YYYY-MM-DD: ")

    def get_end_date(self):
        self.end_date = input("Enter end date YYYY-MM-DD: ")

    def print_comp(self):
        print("Companies: ", self.companies)

    def print_all(self):
        print("Companies: ", self.companies)
        print("Start date: ", self.start_date)
        print("End date: ", self.end_date)


# testing
test1 = Test()
test1.get_comp_list()
test1.get_start_date()
test1.get_end_date()
test1.print_all()


