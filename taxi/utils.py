"""Get sorted driver instances."""
from django.db.models import Case, When
from mobile.utils import state_dict
from taxi.models import Kierowca


def get_sorted_driver_instances(driver_ids):
    """Get sorted driver instances by status."""
    ordered_ids = []
    for id in driver_ids:
        if id in state_dict.keys():
            ordered_ids.append(id)
    [ordered_ids.append(id) for id in driver_ids if id not in ordered_ids]
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ordered_ids)])
    return Kierowca.objects.filter(idKierowcy__in=ordered_ids).order_by(preserved)


def build_error_dict(form):
    """Build error dict for json response."""
    errors = {}
    if form.non_field_errors():
        errors['other'] = {
            'label': 'Inne błędy',
            'errors': form.non_field_errors(),
        }
    for field in form:
        if field.errors:
            errors[field.name] = {
                'label': field.label,
                'errors': field.errors,
            }
    return errors