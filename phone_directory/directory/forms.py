from django import forms

from .models import Employee


class EmployeeForm(forms.ModelForm):
    """Форма для создания и редактирования сотрудников."""

    class Meta:
        model = Employee
        fields = ('name', 'phone', 'position', 'department', 'room', 'email')
        widgets = {
            'department': forms.Select(attrs={'class': 'form-control'}),
        }


class ImportForm(forms.Form):
    """Форма для импорта данных сотрудников из CSV-файла."""

    file = forms.FileField(label='CSV файл')
    update_existing = forms.BooleanField(
        required=False,
        initial=True,
        label='Обновить существующие записи'
    )
