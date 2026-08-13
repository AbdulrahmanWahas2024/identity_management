from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # for type checkers / linters
    import frappe  # type: ignore
else:
    try:
        import frappe
    except Exception:
        # runtime fallback for environments where frappe is unavailable
        frappe = None  # type: ignore

from identity_management.id_card_system.services.employee_card_service import (
    EmployeeCardService,
)
from identity_management.id_card_system.services.tracking_service import TrackingService


class WorkflowService:

    def __init__(self, doc):

        # مستند Card Request
        self.doc = doc

    # =====================================================
    # معالجة إجراءات Workflow
    # =====================================================

    def process_workflow(self):

        # -------------------------------------------------
        # الحالة الحالية بعد انتقال Workflow
        # -------------------------------------------------

        state = self.doc.workflow_state

        if not state:
            return

        # -------------------------------------------------
        # الحصول على اسم الإجراء الحقيقي
        # من Employee Card Workflow
        # -------------------------------------------------

        action = self.get_action_name(state)

        # -------------------------------------------------
        # تسجيل الإجراء في جدول الإجراءات
        # -------------------------------------------------

        TrackingService(self.doc).add_track(workflow_state=state, action=action)

        # -------------------------------------------------
        # خدمة بطاقة الموظف
        # -------------------------------------------------

        card_service = EmployeeCardService(self.doc)

        # =================================================
        # استلام الطلب من تقنية المعلومات
        #
        # IT Pending
        #      ↓
        # استلام الطلب
        #      ↓
        # Card Preparation
        #
        # عند الوصول إلى Card Preparation
        # يتم إنشاء بطاقة الموظف.
        # =================================================

        if state == "Card Preparation":

            card_service.create_identity_card()

        # =================================================
        # تجهيز البطاقة
        #
        # Card Preparation
        #      ↓
        # تجهيز البطاقة
        #      ↓
        # Ready for Print
        #
        # =================================================

        elif state == "Ready for Print":

            card_service.update_card_status("جاهزة للطباعة")

        # =================================================
        # طباعة البطاقة
        #
        # Ready for Print
        #      ↓
        # طباعة البطاقة
        #      ↓
        # Printed
        #
        # =================================================

        elif state == "Printed":

            card_service.update_card_status("تمت الطباعة")

        # =================================================
        # تسليم البطاقة
        #
        # Printed
        #      ↓
        # تسليم البطاقة
        #      ↓
        # Delivered
        #
        # =================================================

        elif state == "Delivered":

            card_service.update_card_status("تم التسليم")

        # =================================================
        # إكمال الطلب
        #
        # Delivered
        #      ↓
        # اكمال الطلب
        #      ↓
        # Completed
        #
        # =================================================

        elif state == "Completed":

            card_service.update_card_status("نشطة")

    # =====================================================
    # استخراج اسم الإجراء الحقيقي من Workflow
    # =====================================================

    def get_action_name(self, next_state):

        # -------------------------------------------------
        # قراءة Workflow المستخدم فعلياً
        # -------------------------------------------------

        workflow = frappe.get_doc("Workflow", "Employee Card Workflow")

        # -------------------------------------------------
        # البحث عن Transition الذي يصل إلى الحالة الحالية
        # -------------------------------------------------

        for transition in workflow.transitions:

            if transition.next_state == next_state:

                return transition.action

        # -------------------------------------------------
        # إذا لم نجد Transition
        # نستخدم اسم الحالة كإجراء احتياطي
        # -------------------------------------------------

        return next_state
