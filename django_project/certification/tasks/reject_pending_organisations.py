from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from ..models.certifying_organisation import CertifyingOrganisation
from ..models.status import Status
from ..views import send_rejection_email


@shared_task
def reject_pending_organisations(days=365):
    """Celery task to reject pending certifying organisations
    that were created more than one year ago.
    """
    print('Begin process....')
    print(f'Number of days: {days}')
    one_year_ago = timezone.now() - timedelta(days=days)
    old_organisations = CertifyingOrganisation.unapproved_objects.all()

    print('Begin process to reject old certifying organisations.')

    count = 0
    for organisation in old_organisations:
        if organisation.update_date < one_year_ago:
            rejected_status, created = Status.objects.get_or_create(
                name='Rejected',
                project=organisation.project
            )
            organisation.status = rejected_status
            organisation.rejected = True
            organisation.save()

            send_rejection_email(
                organisation,
                'certification.qgis.org',
                'https'
            )
            count += 1
            print(f'{organisation.name} has been set to Rejected')

    result = f'{count} certifying organisations have been set to Rejected'
    print('------------------------------------------------------------')
    print('Process finished.')
    return result