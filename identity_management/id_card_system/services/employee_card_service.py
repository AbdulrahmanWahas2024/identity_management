import frappe
from frappe import _


class EmployeeCardService:

    def __init__(self, doc):

        # مستند طلب البطاقة Card Request
        self.doc = doc

    # =====================================================
    # إنشاء بطاقة الموظف
    #
    # يتم استدعاؤها عند وصول الطلب إلى:
    # Card Preparation
    #
    # مسؤول تقنية المعلومات
    # =====================================================

    def create_identity_card(self):

        # منع إنشاء بطاقة مكررة لنفس الطلب

        if self.doc.employee_identity_card:

            return

        # إنشاء مستند بطاقة جديد

        card = frappe.new_doc("Employee Identity Card")

        # =====================================================
        # ربط البطاقة بطلب الإصدار
        # =====================================================

        card.card_request = self.doc.name

        # الموظف

        card.employee = self.doc.employee

        # الرقم الوظيفي الذي سيطبع على البطاقة

        card.employee_number = self.doc.employee_number

        # =====================================================
        # تحديد نوع البطاقة الافتراضي
        # =====================================================

        card.card_type = frappe.db.get_value("Card Type", {"is_default": 1}, "name")

        if not card.card_type:

            frappe.throw(_("لم يتم تعريف نوع بطاقة افتراضي."))

        # =====================================================
        # الحالة الابتدائية للبطاقة
        #
        # عند إنشاء البطاقة تكون:
        # بانتظار تقنية المعلومات
        # =====================================================

        card.card_status = "بانتظار تقنية المعلومات"

        # =====================================================
        # إنشاء رقم البطاقة
        #
        # مثال:
        # EMP-ID-26-00001
        #
        # هذا رقم البطاقة الصادرة
        # وليس رقم الطلب
        # =====================================================

        card.card_number = frappe.model.naming.make_autoname("EMP-ID-.YY.-.#####")

        # جهة الإصدار

        card.issuing_office = self.doc.branch

        # حفظ البطاقة

        card.insert(ignore_permissions=True)

        # =====================================================
        # ربط البطاقة مع طلب الإصدار
        # =====================================================

        self.doc.db_set("employee_identity_card", card.name)

        frappe.msgprint(f"""
تم إنشاء بطاقة الموظف بنجاح.


رقم البطاقة:

{card.card_number}

""")

    # =====================================================
    # تحديث حالة البطاقة
    #
    # يتم استدعاؤها مع تغير Workflow
    #
    # مثال:
    #
    # Ready for Print
    # Printed
    # Delivered
    # Completed
    #
    # =====================================================

    def update_card_status(self, status):

        # لا يوجد بطاقة مرتبطة

        if not self.doc.employee_identity_card:

            return

        frappe.db.set_value(
            "Employee Identity Card",
            self.doc.employee_identity_card,
            "card_status",
            status,
        )
