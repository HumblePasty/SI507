### Lets Refactor this Big Ugly Code
class Lec:
    def __init__(self, df_row):
        self.name = df_row['Employee First Name'] + " " + df_row['Employee Last Name']
        self.id = df_row['UM ID']
        if df_row['Appointment Period'] == "7":  # 12 month
            self.Rate = df_row['Comp Rate'] * (1 / df_row['FTE'])
            self.cost = df_row['Comp Rate']
            self.salary = df_row['Comp Rate']
        elif df_row['Appointment Period'] == "9":  # 8 month paid over 8
            self.Rate = df_row['Comp Rate'] * 8 * (1 / df_row['FTE'])
            self.cost = df_row['Comp Rate'] * 8
            self.salary = df_row['Comp Rate'] * 8
        elif df_row['Appointment Period'] == "6":  # worked a 7 week course paid twice
            self.Rate = df_row['Comp Rate'] * 8 * (1 / df_row['FTE'])  #### not sure about this
            self.cost = df_row['Comp Rate'] * 2
            self.salary = df_row['Comp Rate'] * 2
        elif df_row['Appointment Period'] == "5":  # 8 month Dbn paid over 12
            if df_row['Comp Frequency'] == "Annual":
                self.Rate = df_row['Comp Rate'] * (1 / df_row['FTE'])
                self.cost = df_row['Comp Rate']
                self.salary = df_row['Comp Rate']
            elif df_row['Comp Frequency'] == "Monthly":
                self.Rate = df_row['Comp Rate'] * 12 * (1 / df_row['FTE'])
                self.cost = df_row['Comp Rate'] * 12
                self.salary = df_row['Comp Rate'] * 12
        elif df_row['Appointment Period'] == "4":  # 9 month AA paid over 12
            if df_row['Comp Frequency'] == "Annual":
                self.Rate = df_row['Comp Rate'] * (1 / df_row['FTE'])
                self.cost = df_row['Comp Rate']
                self.salary = df_row['Comp Rate']
            elif df_row['Comp Frequency'] == "Monthly":
                self.Rate = df_row['Comp Rate'] * 12 * (1 / df_row['FTE'])
                self.cost = df_row['Comp Rate'] * 12
                self.salary = df_row['Comp Rate'] * 12
        elif df_row['Appointment Period'] == "3":  # Term worker paid monthly. Costed out as both terms
            self.Rate = df_row['Comp Rate'] * 8 * (1 / df_row['FTE'])
            self.cost = df_row['Comp Rate'] * 8  ## assuming they get hired both terms
            self.salary = df_row['Comp Rate'] * 4  ## doesn't assume they get hired both terms.

        self.appointment = df_row['Appointment Period']
        self.start_date = df_row['Appointment Start Date']
        ContractStart = datetime(2024, 9, 21)
        self.ReviewClock = (ContractStart - datetime.strptime(df_row["Appointment Start Date"],
                                                              date_format)).days // 365
        if df_row['School/College/Division'].startswith('FLINT'):
            self.campus = "Flint"
        elif df_row['School/College/Division'].startswith('DBN'):
            self.campus = "Dearborn"
        else:
            self.campus = "Ann Arbor"

        self.title = df_row['Job Title']
        self.effort = df_row['FTE']
        self.MRcount24 = 0
        self.MRcount25 = 0
        self.MRcount26 = 0
        self.MRraiseIn24 = None
        self.MRraiseIn25 = None
        self.MRraiseIn26 = None
        self.salary24 = None
        self.salary25 = None
        self.salary26 = None
        self.cost24 = None
        self.cost25 = None
        self.cost26 = None
        self.Rate24 = None
        self.Rate25 = None
        self.Rate26 = None

    def info(self):
        return f"Employee Information:\nName: {self.name}\nID: {self.id}\nAppointment: {self.appointment}\nStart Date: {self.start_date}\nTitle: {self.title}\nEffort: {self.effort}\nFull Time Rate: {self.Rate}\nCosted in Budget as: {self.cost}\nSalary: {self.salary}\nCampus: {self.campus}"

    def countMRs(self):
        # print("just to confirm no L1/3s have MRs and ignore starting at L2/4 & jump between tracks")
        print("+++")
        # print("  ")
        # print("I'm anticipating MR for all Lec 1s/3s starting with 3 years of service. Do i need to calculate  promotion of intermittent to L1?")
        if self.title in ["LEO Lecturer I", "LEO Lecturer II", "LEO Lecturer III" "LEO Lecturer IV"]:
            if self.ReviewClock == 2:  ### start at 2 because this counts complete years.
                self.MRcount24 = 0
                self.MRcount25 = 0
                self.MRcount26 = 1
                self.MRraiseIn26 = "YES"
            if self.ReviewClock == 3:
                self.MRcount24 = 0
                self.MRcount25 = 1
                self.MRcount26 = 1
                self.MRraiseIn25 = "YES"
            if self.ReviewClock == 4:
                self.MRcount24 = 1
                self.MRcount25 = 1
                self.MRcount26 = 1
                self.MRraisein24 = "YES"
            if self.ReviewClock == 5:
                self.MRcount24 = 1
                self.MRcount25 = 1
                self.MRcount26 = 1
            if self.ReviewClock == 6:
                self.MRcount24 = 1
                self.MRcount25 = 1
                self.MRcount26 = 2
                self.MRraiseIn26 = "YES"
            if self.ReviewClock == 7:
                self.MRcount24 = 1
                self.MRcount25 = 2
                self.MRcount26 = 2
                self.MRraiseIn25 = "YES"
            if self.ReviewClock == 8:
                self.MRcount24 = 2
                self.MRcount25 = 2
                self.MRcount26 = 2
                self.MRraiseIn24 = "YES"
            if self.ReviewClock > 8:
                self.MRcount24 = 2
                self.MRcount25 = 2
                self.MRcount26 = 2
        return self
