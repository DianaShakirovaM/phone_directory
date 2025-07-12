import csv
from io import TextIOWrapper

from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView

from .forms import EmployeeForm, ImportForm
from .models import Employee


class PhoneDirectoryView(TemplateView):
    template_name = 'directory.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('search', '')
        department_filter = self.request.GET.get('department', '')

        employees = Employee.objects.all().order_by('department', 'name')

        if search_query:
            employees = employees.filter(
                Q(name__icontains=search_query) |
                Q(position__icontains=search_query) |
                Q(phone__icontains=search_query) |
                Q(room__icontains=search_query)
            )

        if department_filter:
            employees = employees.filter(department=department_filter)

        departments = Employee.objects.exclude(department__isnull=True) \
            .exclude(department__exact='').order_by('department') \
            .values_list('department', flat=True) \
            .distinct()

        context.update({
            'employees': employees,
            'departments': departments,
            'search_query': search_query,
            'selected_department': department_filter,
            'employee_form': EmployeeForm(),
            'import_form': ImportForm(),
        })

        return context


class EmployeeCreateUpdateView(View):
    def post(self, request):
        employee_id = request.POST.get('id')
        instance = get_object_or_404(
            Employee, pk=employee_id
        ) if employee_id else None
        form = EmployeeForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            messages.success(request, 'Сотрудник успешно сохранен')
        else:
            messages.error(request, 'Ошибка при сохранении сотрудника')
        return redirect('directory:phone_directory')


class EmployeeDeleteView(View):
    def post(self, request, employee_id):
        employee = get_object_or_404(Employee, id=employee_id)
        employee.delete()
        messages.success(request, 'Сотрудник успешно удален')
        return redirect('directory:phone_directory')


class DataExportView(View):
    def get(self, request):
        fields = request.GET.getlist('fields', [
            'name', 'position', 'department', 'phone', 'room', 'email'
        ])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="directory.csv"'

        writer = csv.writer(response, delimiter=';')
        writer.writerow(fields)

        employees = Employee.objects.all()
        for employee in employees:
            row = [getattr(employee, field) for field in fields]
            writer.writerow(row)

        return response


def import_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        csv_file = request.FILES['file']
        update_existing = request.POST.get('update_existing', False)

        try:
            decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
            sample = decoded_file.read(1024)
            decoded_file.seek(0)

            for delimiter in [';', ',', '\t']:
                if delimiter in sample:
                    break
            else:
                delimiter = ';'

            reader = csv.DictReader(
                decoded_file, delimiter=delimiter, skipinitialspace=True
            )

            imported_count = 0
            updated_count = 0
            skipped_count = 0

            for row_num, row in enumerate(reader, start=1):
                if not row.get('name', '').strip():
                    messages.error(
                        request,
                        "Отсутствует обязательное поле 'ФИО/Организация'"
                    )
                    skipped_count += 1
                    continue

                employee_data = {
                    'name': row['name'].strip(),
                    'position': row.get('position', '').strip() or None,
                    'department': row.get('department', '').strip() or None,
                    'phone': row.get('phone', '').strip() or None,
                    'room': row.get('room', '').strip() or None,
                    'email': row.get('email', '').strip() or None,
                }

                existing = Employee.objects.filter(
                    name__iexact=employee_data['name'],
                    department=employee_data['department']
                ).first()

                if existing and update_existing:
                    for field, value in employee_data.items():
                        setattr(existing, field, value)
                    existing.save()
                    updated_count += 1
                elif not existing:
                    Employee.objects.create(**employee_data)
                    imported_count += 1
                else:
                    messages.warning(
                        request,
                        f"Сотрудник {employee_data['name']} уже существует"
                    )
                    skipped_count += 1

            if imported_count or updated_count:
                result_msg = f'Успешно: добавлено {imported_count}, обновлено {updated_count}'
                if skipped_count:
                    result_msg += f', пропущено {skipped_count}'
                messages.success(request, result_msg)
            else:
                messages.warning(request, 'Импорт не выполнен: нет новых данных для добавления')

        except csv.Error as e:
            messages.error(request, f'Ошибка CSV: {str(e)}')
        except Exception as e:
            messages.error(request, f'Ошибка импорта: {str(e)}')

        return redirect('directory:phone_directory')

    return redirect('directory:phone_directory')
