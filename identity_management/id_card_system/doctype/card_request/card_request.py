# Copyright (c) 2026, Abdulrahman

import frappe
from frappe.model.document import Document

from identity_management.id_card_system.services.tracking_service import (
    TrackingService,
)
from identity_management.id_card_system.services.validation_service import (
    ValidationService,
)
from identity_management.id_card_system.services.workflow_service import (
    WorkflowService,
)
from identity_management.id_card_system.services.employee_card_service import (
    EmployeeCardService,
)


class CardRequest(Document):

    # =====================================================
    # التحقق قبل الحفظ
    # =====================================================

    def validate(self):

        ValidationService(self).validate_request()

    # =====================================================
    # أول إنشاء للطلب
    # =====================================================

    def after_insert(self):

        TrackingService(self).add_track(
            workflow_state="Draft",
            action="إنشاء الطلب",
        )

    # =====================================================
    # التحقق قبل تنفيذ Workflow
    #
    # هذه أهم دالة في المرحلة الحالية.
    #
    # يتم تنفيذها قبل انتقال الطلب إلى الحالة الجديدة.
    #
    # الهدف:
    #
    # Card Preparation
    #        ↓
    # تجهيز البطاقة
    #        ↓
    # Ready for Print
    #
    # لا يسمح النظام بالانتقال إذا:
    #
    # 1. لا توجد صورة
    # 2. الصورة غير معتمدة
    #
    # =====================================================

    def before_workflow_action(self, workflow_action):

        # -------------------------------------------------
        # معرفة الحالة التي سينتقل إليها الطلب
        # -------------------------------------------------

        next_state = self.get_next_workflow_state(workflow_action)

        if not next_state:
            return

        # -------------------------------------------------
        # التحقق قبل الانتقال إلى Ready for Print
        # -------------------------------------------------

        if next_state == "Ready for Print":

            EmployeeCardService(self).validate_request_before_print()

    # =====================================================
    # استخراج الحالة التالية من Workflow
    # =====================================================

    def get_next_workflow_state(self, workflow_action):

        workflow = frappe.get_doc(
            "Workflow",
            "Employee Card Workflow",
        )

        for transition in workflow.transitions:

            if transition.action == workflow_action:

                return transition.next_state

        return None

    # =====================================================
    # تنفيذ العمليات بعد انتقال Workflow
    # =====================================================

    def on_update_after_submit(self):

        WorkflowService(self).process_workflow()
