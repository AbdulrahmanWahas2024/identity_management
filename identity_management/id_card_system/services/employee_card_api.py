# import frappe
# from frappe import _

# from identity_management.id_card_system.services.employee_card_service import (
#     EmployeeCardService,
# )


# @frappe.whitelist()
# def approve_employee_photo(card_request):

#     # =====================================================
#     # التأكد من وجود الطلب
#     # =====================================================

#     if not card_request:

#         frappe.throw(_("لم يتم تحديد طلب البطاقة."))

#     # =====================================================
#     # جلب Card Request
#     # =====================================================

#     doc = frappe.get_doc("Card Request", card_request)

#     # =====================================================
#     # التأكد من صلاحية مختص تقنية المعلومات
#     # =====================================================

#     if not frappe.has_role("IT Card Officer"):

#         frappe.throw(_("ليس لديك صلاحية اعتماد صورة الموظف."))

#     # =====================================================
#     # التأكد من مرحلة Workflow
#     # =====================================================

#     if doc.workflow_state != "Card Preparation":

#         frappe.throw(_("لا يمكن اعتماد الصورة في هذه المرحلة."))

#     # =====================================================
#     # إنشاء Service
#     # =====================================================

#     service = EmployeeCardService(doc)

#     # =====================================================
#     # اعتماد الصورة
#     # =====================================================

#     card = service.approve_photo()

#     # =====================================================
#     # إرجاع النتيجة إلى Client Script
#     # =====================================================

#     return {
#         "success": True,
#         "card": card.name,
#         "photo_status": card.photo_status,
#         "employee_photo": card.employee_photo,
#     }
