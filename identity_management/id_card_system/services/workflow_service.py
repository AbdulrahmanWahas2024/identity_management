# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     # for type checkers / linters
#     import frappe  # type: ignore
# else:
#     try:
#         import frappe
#     except Exception:
#         # runtime fallback for environments where frappe is unavailable
#         frappe = None  # type: ignore

# from identity_management.id_card_system.services.employee_card_service import (
#     EmployeeCardService,
# )
# from identity_management.id_card_system.services.tracking_service import TrackingService


# class WorkflowService:

#     def __init__(self, doc):

#         # مستند Card Request
#         self.doc = doc

#     # =====================================================
#     # معالجة إجراءات Workflow
#     # =====================================================

#     def process_workflow(self):

#         # -------------------------------------------------
#         # الحالة الحالية بعد انتقال Workflow
#         # -------------------------------------------------

#         state = self.doc.workflow_state

#         if not state:
#             return

#         # -------------------------------------------------
#         # الحصول على اسم الإجراء الحقيقي
#         # من Employee Card Workflow
#         # -------------------------------------------------

#         action = self.get_action_name(state)

#         # -------------------------------------------------
#         # تسجيل الإجراء في جدول الإجراءات
#         # -------------------------------------------------

#         TrackingService(self.doc).add_track(workflow_state=state, action=action)

#         # -------------------------------------------------
#         # خدمة بطاقة الموظف
#         # -------------------------------------------------

#         card_service = EmployeeCardService(self.doc)

#         # =================================================
#         # استلام الطلب من تقنية المعلومات
#         #
#         # IT Pending
#         #      ↓
#         # استلام الطلب
#         #      ↓
#         # Card Preparation
#         #
#         # عند الوصول إلى Card Preparation
#         # يتم إنشاء بطاقة الموظف.
#         # =================================================

#         if state == "Card Preparation":
#             # إنشاء بطاقة الموظف
#             card_service.create_identity_card()
#             # تسجيل استلام الطلب
#             card_service.receive_card_request()

#         # =================================================
#         # تجهيز البطاقة
#         #
#         # Card Preparation
#         #      ↓
#         # تجهيز البطاقة
#         #      ↓
#         # Ready for Print
#         #
#         # =================================================

#         elif state == "Ready for Print":

#             card_service.update_card_status("جاهزة للطباعة")

#         # =================================================
#         # طباعة البطاقة
#         #
#         # Ready for Print
#         #      ↓
#         # طباعة البطاقة
#         #      ↓
#         # Printed
#         #
#         # =================================================

#         elif state == "Printed":

#             card_service.update_card_status("تمت الطباعة")

#         # =================================================
#         # تسليم البطاقة
#         #
#         # Printed
#         #      ↓
#         # تسليم البطاقة
#         #      ↓
#         # Delivered
#         #
#         # =================================================

#         elif state == "Delivered":

#             card_service.update_card_status("تم التسليم")

#         # =================================================
#         # إكمال الطلب
#         #
#         # Delivered
#         #      ↓
#         # اكمال الطلب
#         #      ↓
#         # Completed
#         #
#         # =================================================

#         elif state == "Completed":

#             card_service.update_card_status("نشطة")

#     # =====================================================
#     # استخراج اسم الإجراء الحقيقي من Workflow
#     # =====================================================

#     def get_action_name(self, next_state):

#         # -------------------------------------------------
#         # قراءة Workflow المستخدم فعلياً
#         # -------------------------------------------------

#         workflow = frappe.get_doc("Workflow", "Employee Card Workflow")

#         # -------------------------------------------------
#         # البحث عن Transition الذي يصل إلى الحالة الحالية
#         # -------------------------------------------------

#         for transition in workflow.transitions:

#             if transition.next_state == next_state:

#                 return transition.action

#         # -------------------------------------------------
#         # إذا لم نجد Transition
#         # نستخدم اسم الحالة كإجراء احتياطي
#         # -------------------------------------------------

#         return next_state
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import frappe  # type: ignore
else:
    try:
        import frappe
    except Exception:
        frappe = None  # type: ignore


from identity_management.id_card_system.services.employee_card_service import (
    EmployeeCardService,
)

from identity_management.id_card_system.services.tracking_service import (
    TrackingService,
)


class WorkflowService:

    def __init__(self, doc):

        # =================================================
        # مستند Card Request
        # =================================================

        self.doc = doc

    # =====================================================
    # معالجة إجراءات Workflow
    # =====================================================

    def process_workflow(self):

        # =================================================
        # الحالة الحالية بعد انتقال Workflow
        # =================================================

        state = self.doc.workflow_state

        if not state:

            return

        # =================================================
        # الحصول على اسم الإجراء
        # =================================================

        action = self.get_action_name(state)

        # =================================================
        # خدمة البطاقة
        # =================================================

        card_service = EmployeeCardService(self.doc)

        # =================================================
        # التحقق من الانتقال إلى الطباعة
        #
        # Ready for Print
        #        ↓
        # طباعة البطاقة
        #        ↓
        # Printed
        #
        # =================================================
        #
        # مهم:
        #
        # عند وصول الحالة إلى Printed
        # لا نعتبر الانتقال صحيحًا إلا بعد
        # نجاح التحقق النهائي.
        #
        # =================================================

        if state == "Printed":

            # -------------------------------------------------
            # التحقق النهائي
            #
            # يعتمد على Card Request:
            #
            # employee_photo
            # photo_status
            #
            # ثم يتحقق من:
            #
            # الموظف
            # الرقم الوظيفي
            # نوع البطاقة
            # الصورة
            # اعتماد الصورة
            # تاريخ الإصدار
            # تاريخ الانتهاء
            #
            # -------------------------------------------------

            card_service.validate_before_print()

            # -------------------------------------------------
            # إذا وصلنا إلى هنا:
            #
            # جميع شروط الطباعة مكتملة
            # -------------------------------------------------

            card_service.update_card_status("تمت الطباعة")

            # -------------------------------------------------
            # تسجيل حركة الطباعة
            # -------------------------------------------------

            return self.finish_workflow_tracking(
                state=state,
                action=action,
            )

        # =====================================================
        # استلام الطلب من تقنية المعلومات
        #
        # IT Pending
        #       ↓
        # استلام الطلب
        #       ↓
        # Card Preparation
        #
        # =====================================================

        if state == "Card Preparation":

            # -------------------------------------------------
            # إنشاء Employee Identity Card
            # إذا لم تكن موجودة
            # -------------------------------------------------

            card_service.create_identity_card()

            # -------------------------------------------------
            # استلام الطلب
            # -------------------------------------------------

            card_service.receive_card_request()

            return self.finish_workflow_tracking(
                state=state,
                action=action,
            )

        # =====================================================
        # تجهيز البطاقة
        #
        # Card Preparation
        #       ↓
        # تجهيز البطاقة
        #       ↓
        # Ready for Print
        #
        # =====================================================

        if state == "Ready for Print":

            # -------------------------------------------------
            # التحقق وتجهيز البطاقة
            #
            # تعتمد الدالة على:
            #
            # Card Request.employee_photo
            # Card Request.photo_status
            #
            # -------------------------------------------------

            card_service.prepare_card()

            return self.finish_workflow_tracking(
                state=state,
                action=action,
            )

        # =====================================================
        # تسليم البطاقة
        #
        # Printed
        #       ↓
        # تسليم البطاقة
        #       ↓
        # Delivered
        #
        # =====================================================

        if state == "Delivered":

            card_service.update_card_status("تم التسليم")

            return self.finish_workflow_tracking(
                state=state,
                action=action,
            )

        # =====================================================
        # إكمال الطلب
        #
        # Delivered
        #       ↓
        # إكمال الطلب
        #       ↓
        # Completed
        #
        # =====================================================

        if state == "Completed":

            card_service.update_card_status("نشطة")

            return self.finish_workflow_tracking(
                state=state,
                action=action,
            )

        # =====================================================
        # أي حالة أخرى
        # =====================================================

        return self.finish_workflow_tracking(
            state=state,
            action=action,
        )

    # =====================================================
    # تسجيل حركة Workflow
    # =====================================================

    def finish_workflow_tracking(
        self,
        state,
        action,
    ):

        # =================================================
        # تسجيل الحركة في Tracking
        # =================================================

        TrackingService(self.doc).add_track(
            workflow_state=state,
            action=action,
        )

        return True

    # =====================================================
    # استخراج اسم الإجراء الحقيقي من Workflow
    # =====================================================

    def get_action_name(self, next_state):

        # =================================================
        # التأكد من وجود frappe
        # =================================================

        if not frappe:

            return next_state

        # =================================================
        # قراءة Workflow
        # =================================================

        workflow = frappe.get_doc("Workflow", "Employee Card Workflow")

        # =================================================
        # البحث عن Transition
        # =================================================

        for transition in workflow.transitions:

            if transition.next_state == next_state:

                return transition.action

        # =================================================
        # في حالة عدم العثور على الإجراء
        # =================================================

        return next_state
