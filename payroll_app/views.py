from django.shortcuts import render

# Create your views here.

def employees(request):
    return render(request, 'payroll_app/employees.html')

def create_employee(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'payroll_app/create_employee.html')

def update_employee(request, pk):
    if request.method == "POST":
        pass
    else:
        return render(request, 'payroll_app/update_employee.html')

def payslips(request):
    if request.method == "POST":
        pass
    else:
        return render(request, 'payroll_app/payslips.html')

def view_payslip(request, pk):
    return render(request, 'payroll_app/view_payslip.html')
