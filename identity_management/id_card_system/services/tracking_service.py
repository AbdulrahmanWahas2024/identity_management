# import frappe
# from frappe.utils import now_datetime


# class TrackingService:

#     def __init__(self, doc):
#         self.doc = doc

#     # =====================================================
#     # إضافة سجل جديد لحركة Workflow
#     # =====================================================

#     def add_track(self, workflow_state, action):

#         # -------------------------------------------------
#         # التأكد من وجود الحالة
#         # -------------------------------------------------

#         if not workflow_state:
#             return

#         # -------------------------------------------------
#         # منع تسجيل نفس الانتقال مرتين
#         # -------------------------------------------------

#         existing = frappe.db.exists(
#             "Workflow Track",
#             {
#                 "parent": self.doc.name,
#                 "parenttype": "Card Request",
#                 "parentfield": "workflow_track",
#                 "workflow_state": workflow_state,
#             },
#         )

#         if existing:
#             return

#         # -------------------------------------------------
#         # إنشاء Child Row مباشرة في قاعدة البيانات
#         # -------------------------------------------------

#         row = frappe.get_doc(
#             {
#                 "doctype": "Workflow Track",
#                 "parent": self.doc.name,
#                 "parenttype": "Card Request",
#                 "parentfield": "workflow_track",
#                 "workflow_state": workflow_state,
#                 "action": action,
#                 "action_user": frappe.session.user,
#                 "action_date": now_datetime(),
#                 "remarks": "",
#             }
#         )

#         # -------------------------------------------------
#         # حفظ السجل
#         # -------------------------------------------------

#         row.insert(ignore_permissions=True)

#         return row
import frappe
from frappe.utils import now_datetime


class TrackingService:

    def __init__(self, doc):
        self.doc = doc

    # =====================================================
    # إضافة سجل جديد لحركة Workflow
    # =====================================================

    def add_track(self, workflow_state, action):

        # -------------------------------------------------
        # التأكد من وجود الحالة
        # -------------------------------------------------

        if not workflow_state:
            return

        # -------------------------------------------------
        # منع تسجيل نفس الحالة أكثر من مرة
        # -------------------------------------------------

        existing = frappe.db.exists(
            "Workflow Track",
            {
                "parent": self.doc.name,
                "parenttype": "Card Request",
                "parentfield": "workflow_track",
                "workflow_state": workflow_state,
            },
        )

        if existing:
            return

        # =================================================
        # حساب رقم الصف الجديد
        #
        # مثال:
        #
        # يوجد 3 سجلات
        # السجل الجديد يجب أن يكون:
        #
        # idx = 4
        # =================================================

        jls_extract_var = """
                    SELECT COALESCE(MAX(idx), 0)
                    FROM `tabWorkflow Track`
                    WHERE parent = %s
                        AND parenttype = %s
                        AND parentfield = %s
                    """
        last_idx = frappe.db.sql(
            jls_extract_var,
            (
                self.doc.name,
                "Card Request",
                "workflow_track",
            ),
        )[0][0]

        new_idx = int(last_idx or 0) + 1

        # =================================================
        # إنشاء Child Document
        # =================================================

        row = frappe.get_doc(
            {
                "doctype": "Workflow Track",
                "parent": self.doc.name,
                "parenttype": "Card Request",
                "parentfield": "workflow_track",
                # -------------------------------------------------
                # رقم ترتيب الصف
                # -------------------------------------------------
                "idx": new_idx,
                # -------------------------------------------------
                # بيانات الإجراء
                # -------------------------------------------------
                "workflow_state": workflow_state,
                "action": action,
                "action_user": frappe.session.user,
                "action_date": now_datetime(),
                "remarks": "",
            }
        )

        # =================================================
        # حفظ السجل
        # =================================================

        row.insert(ignore_permissions=True)

        return row
