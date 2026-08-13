import frappe

from identity_management.id_card_system.services.validation_service import (
    ValidationService,
)
from identity_management.id_card_system.services.workflow_service import WorkflowService


class CardRequestService:

    def __init__(self, doc):

        # مستند طلب البطاقة
        self.doc = doc

    # =====================================================
    # التحقق قبل حفظ الطلب
    #
    # CardRequest.validate()
    #
    # =====================================================

    def validate_request(self):

        ValidationService(self.doc).validate_request()

    # =====================================================
    # تشغيل  Workflow
    #
    # يتم  بعد انتقال الحالة
    #
    # =====================================================

    def process_workflow(self):

        WorkflowService(self.doc).process_workflow()
