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
        pass
    else:
        return render(request, 'payroll_app/create_employee.html')

def update_employee(request, pk):
    if request.method == "POST":
        pass
    else:
        employee = get_object_or_404(Employee, pk=pk)
        return render(request, 'payroll_app/update_employee.html',
                      {"e": employee})

def payslips(request):
    if request.method == "POST":
        pass
    else:
        payslip_objs = Payslip.objects.all()
        return render(request, 'payroll_app/payslips.html',
                      {'payslips': payslip_objs})

def view_payslip(request, pk):
    payslip = get_object_or_404(Payslip, pk=pk)
    return render(request, 'payroll_app/view_payslip.html',
                  {"p": payslip})

def delete_employee(request, pk):
    Employee.objects.filter(pk=pk).delete()
    return redirect('employees')
