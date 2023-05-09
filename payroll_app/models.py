from django.db import models

# Create your models here.

class Employee(models.Model):
    name = models.CharField(max_length=300)
    id_number = models.CharField(max_length=300, primary_key=True)
    rate = models.FloatField()
    overtime_pay = models.FloatField(null=True, blank=True)
    allowance = models.FloatField(null=True, blank=True)
    objects = models.Manager()

    def getName(self):
        return self.name
    
    def getID(self):
        return self.id_number
    
    def getRate(self):
        return self.rate
    
    def getOvertime(self):
        if self.overtime_pay:
            return self.overtime_pay
        else:
            return 0
    
    def resetOvertime(self):
        self.overtime_pay = None
    
    def getAllowance(self):
        if self.allowance:
            return self.allowance
        else:
            return 0
    
    def __str__(self):
        return f"pk: {self.id_number}, rate: {self.rate}"


class Payslip(models.Model):
    id_number = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=300)
    date_range = models.CharField(max_length=300)
    year = models.CharField(max_length=300)
    pay_cycle = models.IntegerField()
    rate = models.FloatField()
    earnings_allowance = models.FloatField()
    deductions_tax = models.FloatField()
    deductions_health = models.FloatField()
    pag_ibig = models.FloatField()
    sss = models.FloatField()
    overtime = models.FloatField()
    total_pay = models.FloatField()
    objects = models.Manager()

    def getIDNumber(self):
        return self.id_number.getID()
    
    def getMonth(self):
        return self.month
    
    def getDate_range(self):
        return self.date_range

    def getYear(self):
        return self.year

    def getPay_cycle(self):
        return self.pay_cycle

    def getRate(self):
        return self.rate

    def getCycleRate(self):
        return self.rate / 2
    
    def getEarnings_allowance(self):
        return self.earnings_allowance

    def getDeductions_tax(self):
        return self.deductions_tax

    def getDeductions_health(self):
        return self.deductions_health
    
    def getPag_ibig(self):
        return self.pag_ibig

    def getSSS(self):
        return self.sss
    
    def getOvertime(self):
        return self.overtime

    def getTotal_pay(self):
        return self.total_pay
    
    def __str__(self):
        return f"pk: {self.pk}, Employee: {self.id_number.getID()}, " \
             + f"Period: {self.month} {self.date_range}, {self.year}, " \
             + f"Cycle: {self.pay_cycle}, Total Pay: {self.total_pay}"