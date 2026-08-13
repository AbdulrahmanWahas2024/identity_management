# Copyright (c) 2026, Abdulrahman
from frappe.model.document import Document

from identity_management.id_card_system.services.tracking_service import TrackingService
from identity_management.id_card_system.services.validation_service import (
    ValidationService,
)
from identity_management.id_card_system.services.workflow_service import WorkflowService


class CardRequest(Document):

    # التحقق قبل الحفظ
    def validate(self):
        ValidationService(self).validate_request()

    # أول إنشاء للطلب (Draft)
    def after_insert(self):
        TrackingService(self).add_track(workflow_state="Draft", action="إنشاء الطلب")

    # أي انتقال Workflow بعد الـ Submit
    def on_update_after_submit(self):
        WorkflowService(self).process_workflow()
