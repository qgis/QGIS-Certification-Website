# coding=utf-8
"""Urls for certification apps."""

from django.urls import re_path as url

from .api_views.certifying_organisations import CertifyingOrganisationApiListView
from .api_views.checklist import UpdateChecklistReviewer
from .api_views.course import (
    GetPastCourseOrganisation,
    GetPastCourseProject,
    GetUpcomingCourseOrganisation,
    GetUpcomingCourseProject,
)
from .api_views.external_reviewer import UpdateExternalReviewerText
from .api_views.get_status import GetStatus
from .api_views.invite_reviewer import InviteReviewerApiView
from .api_views.training_center import (
    GetTrainingCenterOrganisationLocation,
    GetTrainingCenterProjectLocation,
)
from .api_views.update_status import UpdateStatusOrganisation
from .views import (  # Certifying Organisation.; Course Type.; Course Convener.; Course.; Certificate type and checklist; Training Center.; Attendee.; Course Attendee.; Certificate.; Certificate for certifying organisation.; Validate Certificate.; TopUpView,; Documentation
    ActivateChecklist,
    ApproveCertifyingOrganisationView,
    ArchiveChecklist,
    ArchivedCertifyingOrganisationListView,
    AttendeeCreateView,
    AttendeeUpdateView,
    CertificateChecklistCreateView,
    CertificateCreateView,
    CertificateDetailView,
    CertificateRevokeView,
    CertificationManagementView,
    CertifyingOrganisationArchivingView,
    CertifyingOrganisationCreateView,
    CertifyingOrganisationDeleteView,
    CertifyingOrganisationDetailView,
    CertifyingOrganisationJson,
    CertifyingOrganisationListView,
    CertifyingOrganisationUpdateView,
    CheckoutSessionSuccessView,
    CourseAttendeeCreateView,
    CourseAttendeeDeleteView,
    CourseConvenerCreateView,
    CourseConvenerDeleteView,
    CourseConvenerUpdateView,
    CourseCreateView,
    CourseDeleteView,
    CourseDetailView,
    CourseTypeCreateView,
    CourseTypeDeleteView,
    CourseTypeDetailView,
    CourseTypeUpdateView,
    CourseUpdateView,
    CreateCheckoutSessionView,
    CsvUploadView,
    GetCertificateTypeList,
    HomepageView,
    OrganisationCertificateCreateView,
    OrganisationCertificateDetailView,
    PayrexxTopUpView,
    PayrexxWebhookView,
    PendingCertifyingOrganisationListView,
    TrainingCenterCreateView,
    TrainingCenterDeleteView,
    TrainingCenterDetailView,
    TrainingCenterUpdateView,
    UpdateChecklistOrder,
    ValidateCertificate,
    ValidateCertificateOrganisation,
    certificate_pdf_view,
    docs_approval_cert_org,
    docs_cert_manager,
    docs_course_conveners,
    docs_course_types,
    docs_courses,
    docs_create_certificate_template,
    docs_getting_help,
    docs_issuing_certificates,
    docs_manage_cert_org,
    docs_overview,
    docs_payments,
    docs_register_cert_org,
    docs_training_centers,
    download_certificates_zip,
    email_all_attendees,
    generate_all_certificate,
    organisation_certificate_pdf_view,
    preview_certificate,
    regenerate_all_certificate,
    regenerate_certificate,
    reject_certifying_organisation,
    update_paid_status,
    update_project_certificate_view,
)

urlpatterns = [
    # Home page
    url(r"^$", view=HomepageView.as_view(), name="home"),
    # Certifying Organisation management
    url(
        r"^archived-certifyingorganisation/list/$",
        view=ArchivedCertifyingOrganisationListView.as_view(),
        name="archived-certifyingorganisation-list",
    ),
    url(
        r"^pending-certifyingorganisation/list/$",
        view=PendingCertifyingOrganisationListView.as_view(),
        name="pending-certifyingorganisation-list",
    ),
    url(
        r"^certifyingorganisation-json/$",
        view=CertifyingOrganisationJson.as_view(),
        name="certifyingorganisation-list-json",
    ),
    url(
        r"^approve-certifyingorganisation/(?P<slug>[\w-]+)/$",
        view=ApproveCertifyingOrganisationView.as_view(),
        name="certifyingorganisation-approve",
    ),
    url(
        r"^reject-certifyingorganisation/(?P<slug>[\w-]+)/$",
        view=reject_certifying_organisation,
        name="certifyingorganisation-reject",
    ),
    url(
        r"^update-status-certifyingorganisation/(?P<slug>[\w-]+)/$",
        view=UpdateStatusOrganisation.as_view(),
        name="certifyingorganisation-update-status",
    ),
    url(
        r"^certifyingorganisation/list/$",
        view=CertifyingOrganisationListView.as_view(),
        name="certifyingorganisation-list",
    ),
    url(
        r"^certifyingorganisation/(?P<slug>[\w-]+)/$",
        view=CertifyingOrganisationDetailView.as_view(),
        name="certifyingorganisation-detail",
    ),
    url(
        r"^certifyingorganisation/(?P<slug>[\w-]+)/archiving/(?P<toogle_archive>[\w-]+)/$",
        view=CertifyingOrganisationArchivingView.as_view(),
        name="certifyingorganisation-toogle-archive",
    ),
    url(
        r"^certifyingorganisation/(?P<slug>[\w-]+)/delete/$",
        view=CertifyingOrganisationDeleteView.as_view(),
        name="certifyingorganisation-delete",
    ),
    url(
        r"^create-certifyingorganisation/$",
        view=CertifyingOrganisationCreateView.as_view(),
        name="certifyingorganisation-create",
    ),
    url(
        r"^certifyingorganisation/(?P<slug>[\w-]+)/update/$",
        view=CertifyingOrganisationUpdateView.as_view(),
        name="certifyingorganisation-update",
    ),
    # Course Type.
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/create-coursetype/$",
        view=CourseTypeCreateView.as_view(),
        name="coursetype-create",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/coursetype/(?P<pk>[0-9]+)/update/$",
        view=CourseTypeUpdateView.as_view(),
        name="coursetype-update",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/coursetype/(?P<pk>[0-9]+)/delete/$",
        view=CourseTypeDeleteView.as_view(),
        name="coursetype-delete",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/coursetype/(?P<pk>[0-9]+)/$",
        view=CourseTypeDetailView.as_view(),
        name="coursetype-detail",
    ),
    # Course convener.
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/create-courseconvener/",
        view=CourseConvenerCreateView.as_view(),
        name="courseconvener-create",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/convener/(?P<slug>[\w-]+)/delete/$",
        view=CourseConvenerDeleteView.as_view(),
        name="courseconvener-delete",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/convener/(?P<slug>[\w-]+)/update/$",
        view=CourseConvenerUpdateView.as_view(),
        name="courseconvener-update",
    ),
    # Training Center management
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/create-trainingcenter/$",
        view=TrainingCenterCreateView.as_view(),
        name="trainingcenter-create",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/trainingcenter/(?P<slug>[\w-]+)/$",
        view=TrainingCenterDetailView.as_view(),
        name="trainingcenter-detail",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/trainingcenter/(?P<slug>[\w-]+)/delete/$",
        view=TrainingCenterDeleteView.as_view(),
        name="trainingcenter-delete",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/trainingcenter/(?P<slug>[\w-]+)/update/$",
        view=TrainingCenterUpdateView.as_view(),
        name="trainingcenter-update",
    ),
    # Attendee.
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<slug>[\w-]+)/create-attendee/$",
        view=AttendeeCreateView.as_view(),
        name="attendee-create",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/attendee/(?P<pk>[\w-]+)/update/$",
        view=AttendeeUpdateView.as_view(),
        name="attendee-update",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<slug>[\w-]+)/upload/$",
        view=CsvUploadView.as_view(),
        name="upload-attendee",
    ),
    # Course Attendee.
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<slug>[\w-]+)/create-courseattendee/$",
        view=CourseAttendeeCreateView.as_view(),
        name="courseattendee-create",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/courseattendee/(?P<pk>[\w-]+)/delete/$",
        view=CourseAttendeeDeleteView.as_view(),
        name="courseattendee-delete",
    ),
    # Certificate for certifying organisation
    url(
        r"^organisationcertificate/(?P<organisation_slug>[\w-]+)/issue/$",
        view=OrganisationCertificateCreateView.as_view(),
        name="issue-certificate-organisation",
    ),
    url(
        r"^organisationcertificate/(?P<organisation_slug>[\w-]+)/print/$",
        view=organisation_certificate_pdf_view,
        name="print-certificate-organisation",
    ),
    url(
        r"^organisationcertificate/(?P<id>[\w-]+)/$",
        view=OrganisationCertificateDetailView.as_view(),
        name="detail-certificate-organisation",
    ),
    # Certificate Type and Checklist.
    url(
        r"^certification-management/$",
        view=CertificationManagementView.as_view(),
        name="certification-management-view",
    ),
    url(
        r"^activate-checklist/$",
        view=ActivateChecklist.as_view(),
        name="activate-checklist",
    ),
    url(
        r"^archive-checklist/$",
        view=ArchiveChecklist.as_view(),
        name="archive-checklist",
    ),
    url(
        r"^update-checklist-order/$",
        view=UpdateChecklistOrder.as_view(),
        name="update-checklist-order",
    ),
    url(
        r"^certificate-types/update/$",
        view=update_project_certificate_view,
        name="certificate-type-update",
    ),
    url(
        r"^certificate-checklist/create/",
        view=CertificateChecklistCreateView.as_view(),
        name="certificate-checklist-create",
    ),
    url(
        r"^update-checklist-reviewer/(?P<slug>[\w-]+)/",
        view=UpdateChecklistReviewer.as_view(),
        name="update-checklist-reviewer",
    ),
    url(
        r"^invite-external-reviewer/(?P<slug>[\w-]+)/",
        view=InviteReviewerApiView.as_view(),
        name="invite-external-reviewer",
    ),
    url(
        r"^update-external-reviewer-text/",
        view=UpdateExternalReviewerText.as_view(),
        name="update-external-reviewer-text",
    ),
    # Certificate.
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/courseattendee/(?P<pk>[\w-]+)/create-certificate/(?P<certificate_type_pk>[\w-]+)/$",
        view=CertificateCreateView.as_view(),
        name="certificate-create",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/courseattendee/(?P<pk>[\w-]+)/update-certificate-status/$",
        view=update_paid_status,
        name="paid-certificate",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/top-up/$",
        view=PayrexxTopUpView.as_view(),
        name="top-up",
    ),
    url(
        r"^certificate/(?P<id>[\w-]+)/$",
        view=CertificateDetailView.as_view(),
        name="certificate-details",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/print/(?P<pk>[\w-]+)/$",
        certificate_pdf_view,
        name="print-certificate",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/revoke/(?P<pk>[\w-]+)/$",
        CertificateRevokeView.as_view(),
        name="revoke-certificate",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/download_zip/$",
        download_certificates_zip,
        name="download_zip_all",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/send_email/$",
        email_all_attendees,
        name="send_email",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/regenerate-certificate/(?P<pk>[\w-]+)/$",
        regenerate_certificate,
        name="regenerate-certificate",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/regenerate-all-certificate/$",
        regenerate_all_certificate,
        name="regenerate-all-certificate",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<course_slug>[\w-]+)/generate-all-certificate/$",
        generate_all_certificate,
        name="generate-all-certificate",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/preview-certificate/$",
        preview_certificate,
        name="preview-certificate",
    ),
    url(
        r"^certificate-types-list/$",
        view=GetCertificateTypeList.as_view(),
        name="certificate-types-list",
    ),
    # Course.
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/create-course/",
        view=CourseCreateView.as_view(),
        name="course-create",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<slug>[\w-]+)/update/$",
        view=CourseUpdateView.as_view(),
        name="course-update",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<slug>[\w-]+)/delete/$",
        view=CourseDeleteView.as_view(),
        name="course-delete",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/course/(?P<slug>[\w-]+)/$",
        view=CourseDetailView.as_view(),
        name="course-detail",
    ),
    # Search.
    url(
        r"^organisationcertificate/$",
        view=ValidateCertificateOrganisation.as_view(),
        name="validate-certificate-organisation",
    ),
    url(
        r"^certificate/$",
        view=ValidateCertificate.as_view(),
        name="validate-certificate",
    ),
    # API Views
    url(r"^get-status-list/$", view=GetStatus.as_view(), name="get-status-list"),
    # Feeds
    url(
        r"^feed/certifyingorganisations/$",
        view=CertifyingOrganisationApiListView.as_view(),
        name="feed-certifyingorganisations",
    ),
    url(
        r"^feed/upcoming-course/$",
        view=GetUpcomingCourseProject.as_view(),
        name="feed-upcoming-project-course",
    ),
    url(
        r"^feed/past-course/$",
        view=GetPastCourseProject.as_view(),
        name="feed-past-project-course",
    ),
    url(
        r"^feed/training-center/$",
        view=GetTrainingCenterProjectLocation.as_view(),
        name="feed-training-center-project",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/feed/training-center/$",
        view=GetTrainingCenterOrganisationLocation.as_view(),
        name="feed-training-center",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/feed/upcoming-course/$",
        view=GetUpcomingCourseOrganisation.as_view(),
        name="feed-upcoming-course",
    ),
    url(
        r"^certifyingorganisation/(?P<organisation_slug>[\w-]+)/feed/past-course/$",
        view=GetPastCourseOrganisation.as_view(),
        name="feed-past-course",
    ),
    # Checkout
    url(
        "^checkout/$",
        CreateCheckoutSessionView.as_view(),
        name="checkout",
    ),
    url(
        "^checkout-success/$",
        CheckoutSessionSuccessView.as_view(),
        name="checkout-success",
    ),
    # Payrexx webhook
    url(r"^payrexx-hook/$", view=PayrexxWebhookView.as_view(), name="payrexx-webhook"),
    # Documentation
    url(r"^docs/$", view=docs_overview, name="docs-overview"),
    url(r"^docs/cert-manager/$", view=docs_cert_manager, name="docs-cert-manager"),
    url(
        r"^docs/register-cert-org/$",
        view=docs_register_cert_org,
        name="docs-register-cert-org",
    ),
    url(
        r"^docs/approval-cert-org/$",
        view=docs_approval_cert_org,
        name="docs-approval-cert-org",
    ),
    url(
        r"^docs/manage-cert-org/$",
        view=docs_manage_cert_org,
        name="docs-manage-cert-org",
    ),
    url(
        r"^docs/training-centers/$",
        view=docs_training_centers,
        name="docs-training-centers",
    ),
    url(
        r"^docs/course-conveners/$",
        view=docs_course_conveners,
        name="docs-course-conveners",
    ),
    url(r"^docs/course-types/$", view=docs_course_types, name="docs-course-types"),
    url(r"^docs/courses/$", view=docs_courses, name="docs-courses"),
    url(
        r"^docs/create-certificate-template/$",
        view=docs_create_certificate_template,
        name="docs-create-certificate-template",
    ),
    url(r"^docs/payments/$", view=docs_payments, name="docs-payments"),
    url(
        r"^docs/issuing-certificates/$",
        view=docs_issuing_certificates,
        name="docs-issuing-certificates",
    ),
    url(r"^docs/getting-help/$", view=docs_getting_help, name="docs-getting-help"),
]
