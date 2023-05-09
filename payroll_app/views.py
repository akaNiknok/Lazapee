from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip
from django.contrib import messages

# Create your views here.

def employees(request):
    if request.method == "POST":
        id_number = request.POST.get('id_number')
        overtime_hours = float(request.POST.get('addOvertime'))
        employee = Employee.objects.get(pk=id_number)

        overtime = (employee.getRate() / 160) * 1.5 * overtime_hours
        if employee.overtime_pay:
            employee.overtime_pay += employee.overtime_pay + overtime
        else:
            employee.overtime_pay = overtime

        employee.save()
        return redirect("employees")
    else:
        employee_objs = Employee.objects.all()
        return render(request, 'payroll_app/employees.html',
                    {'employees': employee_objs})

def create_employee(request):
    if request.method == "POST":
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')

        if Employee.objects.filter(id_number=id_number).exists():
            messages.error(request, "Employee ID already exists")
            return render(request, 'payroll_app/create_employee.html')
        
        if allowance == "":
            allowance = None
        
        Employee.objects.create(name=name,
                                id_number=id_number,
                                rate=rate,
                                allowance=allowance)

        messages.success(request, "Employee successfully created")
        return redirect('employees')
    else:
        return render(request, 'payroll_app/create_employee.html')

def update_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)

    if request.method == "POST":
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')

        if id_number != employee.getID() and Employee.objects.filter(id_number=id_number).exists():
            messages.error(request, "Employee ID already exists")
            return render(request, 'payroll_app/update_employee.html',
                      {"e": employee})

        if allowance == "":
            allowance = None
        
        Employee.objects.filter(pk=pk).update(name=name,
                                id_number=id_number,
                                rate=rate,
                                allowance=allowance,)
        messages.success(request, "Employee updated successfully")
        return redirect('employees')

    else:
        return render(request, 'payroll_app/update_employee.html',
                      {"e": employee})

def payslips(request):
    employee_objs = Employee.objects.all()
    payslip_objs = Payslip.objects.all()
    
    if request.method == "POST":
        payroll = request.POST.get('payroll')
        month = request.POST.get('month')
        year = request.POST.get('year')
        cycle = request.POST.get('cycle')
        pag_ibig = 100

        if payroll == "allEmployees":
            employees = Employee.objects.all()
        else:
            employees = Employee.objects.filter(pk=payroll)

        for employee in employees:
            if Payslip.objects.filter(id_number=employee, month=month, pay_cycle=cycle, year=year).exists():
                messages.error(request, "Payslip already exists")
                return render(request, 'payroll_app/payslips.html',
                      {'payslips': payslip_objs, "employees": employee_objs})

        for employee in employees:
            rate = employee.getRate()
            overtime = employee.getOvertime()
            earnings_allowance =  employee.getAllowance()
            deductions_health= employee.getRate() * 0.04
            sss=employee.getRate() * 0.045

            if cycle == "1":
                deductions_tax = ((employee.getRate() / 2) + employee.getAllowance() + employee.getOvertime() - pag_ibig) * 0.2
                total_pay = ((employee.getRate() / 2) + employee.getAllowance() + employee.getOvertime() - pag_ibig) - deductions_tax
            else:
                deductions_tax = ((employee.getRate() / 2) + employee.getAllowance() + employee.getOvertime() - deductions_health - sss) * 0.2
                total_pay = ((employee.getRate() / 2) + employee.getAllowance() + employee.getOvertime() - deductions_health - sss) - deductions_tax

            newPayslip = Payslip.objects.create(id_number=employee, 
                                month=month, 
                                year=year,
                                pay_cycle=cycle,
                                rate=rate,
                                earnings_allowance=earnings_allowance,
                                overtime=overtime,
                                total_pay= total_pay,  
                                deductions_health= deductions_health,
                                deductions_tax = deductions_tax,
                                pag_ibig=100,
                                sss=sss,
                            )
            employee.resetOvertime()
            newPayslip.setDate_range()

        messages.success(request, "Payslip successfully created.")
        return redirect('payslips')
    else:
        
        return render(request, 'payroll_app/payslips.html',
                      {'payslips': payslip_objs, "employees": employee_objs})

def view_payslip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    base_pay = payslip.getCycleRate()
    gross = base_pay + payslip.getEarnings_allowance() + payslip.getOvertime()
    if payslip.getPay_cycle() == 1:
        deductions = payslip.getDeductions_tax() + payslip.getPag_ibig()
    else:
        deductions = payslip.getDeductions_tax() + payslip.getDeductions_health() + payslip.getSSS()

    return render(request, 'payroll_app/view_payslip.html',
                  {"p": payslip, "base_pay": base_pay, "gross_pay": gross, 'deductions': deductions})

def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    return redirect('employees')
