import frappe

from identity_management.id_card_system.services.tracking_service import TrackingService


def handle_workflow(doc, method=None):

    # =====================================================
    # التأكد أن المستند هو Card Request
    # =====================================================

    if doc.doctype != "Card Request":
        return

    # =====================================================
    # الحصول على حالة Workflow الحالية
    # =====================================================

    current_state = doc.workflow_state

    if not current_state:
        return

    # =====================================================
    # معرفة الحالة السابقة
    # =====================================================

    old_doc = doc.get_doc_before_save()

    if not old_doc:
        return

    old_state = old_doc.workflow_state

    # =====================================================
    # إذا لم تتغير الحالة فلا يوجد انتقال
    # =====================================================

    if old_state == current_state:
        return

    # =====================================================
    # الحصول على الإجراء الذي ضغط عليه المستخدم
    #
    # مثال:
    #
    # ارسال
    # اعتماد
    # استلام الطلب
    # تجهيز البطاقة
    # طباعة البطاقة
    # تسليم البطاقة
    # اكمال الطلب
    # =====================================================

    action = frappe.form_dict.get("workflow_action")

    # =====================================================
    # إذا لم يرسل Frappe اسم الإجراء
    # نحاول الحصول عليه من Workflow
    # =====================================================

    if not action:

        workflow = frappe.get_doc("Workflow", "Employee Card Workflow")

        for transition in workflow.transitions:

            if transition.state == old_state and transition.next_state == current_state:
                action = transition.action
                break

    # =====================================================
    # احتياطي أخير
    # =====================================================

    if not action:
        action = current_state

    # =====================================================
    # تسجيل الانتقال
    # =====================================================

    TrackingService(doc).add_track(workflow_state=current_state, action=action)
