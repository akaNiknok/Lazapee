from django.shortcuts import render, redirect, get_object_or_404
from .models import Employee, Payslip

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
            # Optional: Message errors
            return redirect('updaate_employee')
        
        if allowance == "":
            allowance = None
        
        Employee.objects.create(name=name,
                                id_number=id_number,
                                rate=rate,
                                allowance=allowance)
        return redirect('employees')
    else:
        return render(request, 'payroll_app/create_employee.html')

def update_employee(request, pk):
    if request.method == "POST":
        name = request.POST.get('name')
        id_number = request.POST.get('id_number')
        rate = request.POST.get('rate')
        allowance = request.POST.get('allowance')
        
        Employee.objects.filter(pk=pk).update(name=name,
                                id_number=id_number,
                                rate=rate,
                                allowance=allowance,)
        return redirect('employees')

    else:
        employee = get_object_or_404(Employee, pk=pk)
        return render(request, 'payroll_app/update_employee.html',
                      {"e": employee})

def payslips(request):
    employee_objs = Employee.objects.all()
    payslip_objs = Payslip.objects.all()
    
    if request.method == "POST":
        
        payroll = request.POST.get('payroll')
        if payroll == 'allEmployees':
            employee = Employee.objects.all()
            for x in employee:
                month = request.POST.get('month')
                year = request.POST.get('year')
                cycle = request.POST.get('cycle')
                rate = x.getRate()
                overtime = x.getOvertime()
                earnings_allowance =  x.getAllowance()
                deductions_health= x.getRate() * 0.04
                sss=x.getRate() * 0.045
                deductions_tax = 0.2
                total_pay=0
                pag_ibig=100

                if cycle == '1':
                    tax = ((x.getRate() / 2) + x.getAllowance() + x.getOvertime() - pag_ibig) * 0.2
                    total_pay = ((x.getRate() / 2) + x.getAllowance() + x.getOvertime() - pag_ibig) - tax
                    Payslip.objects.create(id_number=x, 
                                        month=month, 
                                        year=year,
                                        pay_cycle=cycle,
                                        rate=rate,
                                        earnings_allowance=earnings_allowance,
                                        overtime=overtime,
                                        total_pay= total_pay,  
                                        deductions_health= deductions_health,
                                        deductions_tax = deductions_health,
                                        pag_ibig=100,
                                        sss=sss,
                                    )
                    x.resetOvertime()
                
            if cycle == '2':
                tax = ((x.getRate() / 2) + x.getAllowance() + x.getOvertime() - deductions_health - sss) * 0.2
                total_pay = ((x.getRate() / 2) + x.getAllowance() + x.getOvertime() - deductions_health - sss) - tax
                

                Payslip.objects.create(id_number=x, 
                                        month=month, 
                                        year=year,
                                        pay_cycle=cycle,
                                        rate=rate,
                                        earnings_allowance=earnings_allowance,
                                        overtime=overtime,
                                        total_pay= total_pay,  
                                        deductions_health=deductions_health,
                                        deductions_tax =  deductions_tax,
                                        pag_ibig=100,
                                        sss=sss,
                                    )
                x.resetOvertime()

        else:
            employee = Employee.objects.get(pk=payroll)

            month = request.POST.get('month')
            year = request.POST.get('year')
            cycle = request.POST.get('cycle')
            rate = employee.getRate()
            overtime = employee.getOvertime()
            earnings_allowance =  employee.getAllowance()
            deductions_tax = 0.2
            deductions_health= employee.getRate() * 0.04
            total_pay=0
            pag_ibig=100
            sss=employee.getRate() * 0.045
           
        
            if cycle == '1':
                tax = ((employee.getRate() / 2) + employee.getAllowance() + employee.getOvertime() - pag_ibig) * 0.2
                total_pay = ((employee.getRate() / 2) + employee.getAllowance() + employee.getOvertime() - pag_ibig) - tax
                Payslip.objects.create(id_number=employee, 
                                    month=month, 
                                    year=year,
                                    pay_cycle=cycle,
                                    rate=rate,
                                    earnings_allowance=earnings_allowance,
                                    overtime=overtime,
                                    total_pay= total_pay,  
                                    deductions_health= deductions_health,
                                    deductions_tax = deductions_health,
                                    pag_ibig=100,
                                    sss=sss,
                                )
                employee.resetOvertime()
                
            if cycle == '2':
                tax = ((employee.getRate() / 2) + employee.getAllowance() + employee.getOvertime() - deductions_health - sss) * 0.2
                total_pay = ((employee.getRate() / 2) + employee.getAllowance() + employee.getOvertime() - deductions_health - sss) - tax
                

                Payslip.objects.create(id_number=employee, 
                                        month=month, 
                                        year=year,
                                        pay_cycle=cycle,
                                        rate=rate,
                                        earnings_allowance=earnings_allowance,
                                        overtime=overtime,
                                        total_pay= total_pay,  
                                        deductions_health=deductions_health,
                                        deductions_tax =  deductions_tax,
                                        pag_ibig=100,
                                        sss=sss,
                                    )
                employee.resetOvertime()
        return redirect('payslips')
    else:
        
        return render(request, 'payroll_app/payslips.html',
                      {'payslips': payslip_objs, "employees": employee_objs})

def view_payslip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    return render(request, 'payroll_app/view_payslip.html',
                  {"p": payslip})

def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    return redirect('employees')
