# import frappe
# from frappe import _


# class ValidationService:


#     def __init__(self, doc):

#         # استلام مستند طلب البطاقة الحالي
#         self.doc = doc


#     # =====================================================
#     # تشغيل جميع عمليات التحقق قبل حفظ الطلب
#     # =====================================================

#     def validate_request(self):

#         # جلب بيانات الموظف من جدول Employee
#         self.load_employee_data()


#         # التأكد أن الموظف تم اختياره
#         self.validate_employee()


#         # التأكد من نوع الموظف
#         self.validate_employment_type()


#         # البحث عن بطاقة سابقة
#         self.validate_existing_card()


#     # =====================================================
#     # جلب بيانات الموظف تلقائياً
#     # المصدر:
#     # Employee Doctype
#     # =====================================================

#     def load_employee_data(self):


#         if not self.doc.employee:

#             return


#         employee = frappe.get_doc(
#             "Employee",
#             self.doc.employee
#         )


#         # تعبئة بيانات الطلب من بيانات الموظف

#         self.doc.employee_name = employee.employee_name

#         self.doc.employee_number = employee.employee_number

#         self.doc.company = employee.company

#         self.doc.designation = employee.designation

#         self.doc.department = employee.department

#         self.doc.branch = employee.branch

#         self.doc.employment_type = employee.employment_type


#     # =====================================================
#     # التأكد من اختيار الموظف
#     # =====================================================

#     def validate_employee(self):


#         if not self.doc.employee:


#             frappe.throw(
#                 _("يجب اختيار الموظف قبل حفظ الطلب.")
#             )


#     # =====================================================
#     # التحقق من نوع الموظف
#     #
#     # المصدر:
#     # Employee -> Employment Type
#     #
#     # يمنع:
#     # متقاعد
#     # =====================================================

#     def validate_employment_type(self):


#         blocked_types = [

#             "متقاعد"

#         ]


#         if self.doc.employment_type in blocked_types:


#             frappe.throw(
#                 f"""
# لا يمكن إصدار بطاقة لهذا الموظف.

# نوع الموظف:
# {self.doc.employment_type}
# """
#             )


#     # =====================================================
#     # التحقق من وجود بطاقة سابقة
#     #
#     # البحث بواسطة الموظف
#     #
#     # يمنع إصدار بطاقة ثانية
#     # =====================================================

#     def validate_existing_card(self):


#         cards = frappe.get_all(

#             "Employee Identity Card",


#             filters={

#                 "employee": self.doc.employee

#             },


#             fields=[

#                 "name",

#                 "card_number",

#                 "card_status",

#                 "expiry_date"

#             ],


#             order_by="creation desc"

#         )


#         # لا توجد بطاقة سابقة

#         if not cards:

#             return


#         # الحالات التي تمنع إصدار بطاقة جديدة

#         active_status = [

#             "جديدة",

#             "بانتظار تقنية المعلومات",

#             "قيد التجهيز",

#             "جاهزة للطباعة",

#             "تمت الطباعة",

#             "تم التسليم",

#             "نشطة",

#             "موقفة"

#         ]


#         for card in cards:


#             if card.card_status in active_status:


# #                 frappe.throw(

# # f"""
# # <b>الموظف:</b> {self.doc.employee_name}

# # <b>الرقم الوظيفي:</b> {self.doc.employee_number}


# # يوجد بطاقة سابقة:

# # <b>رقم البطاقة:</b>
# # {card.card_number}


# # <b>حالة البطاقة:</b>
# # {card.card_status}


# # لا يمكن إصدار بطاقة جديدة.

# # يرجى إلغاء أو إنهاء البطاقة السابقة أولاً.
# # """,

# # title="⚠️ يوجد بطاقة سابقة"

# # )
#                 frappe.throw(
#     f"""
#     <b>للموظف:</b> {self.doc.employee_name} ({self.doc.employee_number})<br>
#     لديه بطاقة حالية برقم: <b>{card.card_number}</b> (الحالة: <b>{card.card_status}</b>).<br><br>
#     <span style="color: #d9534f;">يرجى إلغاء أو إنهاء صلاحية البطاقة السابقة قبل إصدار بطاقة جديدة.</span>
#     """,
#     title="⚠️ لا يمكن إصدار بطاقة جديدة"
# )
import frappe
from frappe import _


class ValidationService:

    def __init__(self, doc):
        self.doc = doc

    # =====================================================
    # تشغيل جميع عمليات التحقق
    # =====================================================

    def validate_request(self):

        # 1. تحميل بيانات الموظف
        self.load_employee_data()

        # 2. التأكد من اختيار الموظف
        self.validate_employee()

        # 3. التحقق من نوع الموظف
        self.validate_employment_type()

        # 4. التحقق من اختيار نوع الطلب
        self.validate_request_type()

        # 5. التحقق من البطاقة الحالية
        # مهم: يجب أن يحدث قبل reason والخطاب
        self.validate_existing_card()

        # 6. التحقق من بيانات الطلب
        self.validate_request_data()

    # =====================================================
    # تحميل بيانات الموظف من Employee
    # =====================================================

    def load_employee_data(self):

        if not self.doc.employee:
            return

        employee = frappe.get_doc("Employee", self.doc.employee)

        self.doc.employee_name = employee.employee_name
        self.doc.employee_number = employee.employee_number
        self.doc.company = employee.company
        self.doc.designation = employee.designation
        self.doc.department = employee.department
        self.doc.branch = employee.branch
        self.doc.employment_type = employee.employment_type

        # صورة الموظف من Employee
        #
        # إذا كان لدى الموظف صورة:
        # يتم استخدامها تلقائياً
        #
        # وإذا لم توجد:
        # يستطيع مختص تقنية المعلومات رفعها لاحقاً

        if employee.image and not self.doc.employee_photo:
            self.doc.employee_photo = employee.image

    # =====================================================
    # التأكد من اختيار الموظف
    # =====================================================

    def validate_employee(self):

        if not self.doc.employee:

            frappe.throw(_("يجب اختيار الموظف قبل حفظ الطلب."), title=_("الموظف مطلوب"))

    # =====================================================
    # التحقق من نوع الموظف
    # =====================================================

    def validate_employment_type(self):

        blocked_types = ["متقاعد"]

        if self.doc.employment_type in blocked_types:

            frappe.throw(
                _(
                    "لا يمكن إصدار بطاقة لهذا الموظف.<br>" "نوع الموظف: <b>{0}</b>"
                ).format(self.doc.employment_type),
                title=_("موظف غير مؤهل"),
            )

    # =====================================================
    # التحقق من نوع الطلب
    # =====================================================

    def validate_request_type(self):

        if not self.doc.request_type:

            frappe.throw(_("يجب اختيار نوع الطلب."), title=_("نوع الطلب مطلوب"))

    # =====================================================
    # الحصول على اسم نوع الطلب
    #
    # Card Request
    #       ↓
    # request_type
    #       ↓
    # Card Request Type
    #       ↓
    # request_type_name
    # =====================================================

    def get_request_type_name(self):

        if not self.doc.request_type:
            return None

        return frappe.db.get_value(
            "Card Request Type", self.doc.request_type, "request_type_name"
        )

    # =====================================================
    # البحث عن البطاقة الحالية للموظف
    # =====================================================

    def get_current_card(self):

        if not self.doc.employee:
            return None

        cards = frappe.get_all(
            "Employee Identity Card",
            filters={"employee": self.doc.employee},
            fields=["name", "card_number", "card_status", "expiry_date"],
            order_by="creation desc",
            limit=20,
        )

        if not cards:
            return None

        # الحالات التي تعتبر بطاقة قائمة/فعالة
        active_statuses = [
            "جديدة",
            "بانتظار تقنية المعلومات",
            "قيد التجهيز",
            "جاهزة للطباعة",
            "تمت الطباعة",
            "تم التسليم",
            "نشطة",
        ]

        for card in cards:

            if card.card_status in active_statuses:

                return card

        return None

    # =====================================================
    # التحقق من البطاقة الحالية
    #
    # هذا التحقق يحدث قبل reason والخطاب
    # =====================================================

    def validate_existing_card(self):

        request_type = self.get_request_type_name()

        current_card = self.get_current_card()

        # =================================================
        # إصدار جديد
        #
        # يجب ألا توجد بطاقة حالية
        # =================================================

        if request_type == "إصدار جديد":

            if current_card:

                frappe.throw(
                    f"""
                    <b>الموظف:</b>
                    {self.doc.employee_name}
                    ({self.doc.employee_number})

                    <br><br>

                    توجد بطاقة حالية للموظف.

                    <br>

                    <b>رقم البطاقة:</b>
                    {current_card.card_number}

                    <br>

                    <b>حالة البطاقة:</b>
                    {current_card.card_status}

                    <br><br>

                    لا يمكن تقديم طلب إصدار جديد
                    قبل إنهاء البطاقة الحالية.
                    """,
                    title=_("⚠️ توجد بطاقة حالية"),
                )

            return

        # =================================================
        # الطلبات التي تحتاج بطاقة حالية
        # =================================================

        requests_require_card = ["بدل فاقد", "تجديد", "تعديل بيانات", "إلغاء"]

        # =================================================
        # إذا كان نوع الطلب يحتاج بطاقة
        # =================================================

        if request_type in requests_require_card:

            # لا توجد بطاقة
            if not current_card:

                frappe.throw(
                    f"""
                    <b>الموظف:</b>
                    {self.doc.employee_name}

                    <br><br>

                    لا توجد بطاقة صادرة وحالية
                    لهذا الموظف.

                    <br><br>

                    لا يمكن تقديم طلب:

                    <b>{request_type}</b>

                    <br><br>

                    يجب أن تكون هناك بطاقة حالية
                    للموظف قبل تنفيذ هذا الإجراء.
                    """,
                    title=_("⚠️ لا توجد بطاقة حالية"),
                )

            # توجد بطاقة
            return

    # =====================================================
    # التحقق من بيانات الطلب
    #
    # يتم استدعاؤها بعد التأكد من البطاقة
    # =====================================================

    def validate_request_data(self):

        request_type = self.get_request_type_name()

        # =================================================
        # الأنواع التي تحتاج سبب
        # =================================================

        request_types_with_reason = ["بدل فاقد", "تجديد", "تعديل بيانات", "إلغاء"]

        # =================================================
        # التحقق من السبب
        # =================================================

        if request_type in request_types_with_reason:

            if not self.doc.reason:

                messages = {
                    "بدل فاقد": "يجب إدخال سبب فقدان البطاقة.",
                    "تجديد": "يجب إدخال سبب التجديد.",
                    "تعديل بيانات": "يجب إدخال سبب تعديل بيانات البطاقة.",
                    "إلغاء": "يجب إدخال سبب إلغاء البطاقة.",
                }
                message = messages.get(request_type, "يجب إدخال سبب الطلب.")

                frappe.throw(
                    _(messages.get(request_type, "يجب إدخال سبب الطلب.")),
                    title=_("سبب الطلب مطلوب"),
                    exc=frappe.MandatoryError,
                )

        # =================================================
        # خطاب التوجيه
        # =================================================

        if not self.doc.directive_attachment:

            frappe.throw(_("يجب إرفاق خطاب التوجيه."), title=_("خطاب التوجيه مطلوب"))

        # =================================================
        # رقم خطاب التوجيه
        # =================================================

        if not self.doc.directive_number:

            frappe.throw(_("يجب إدخال رقم خطاب التوجيه."), title=_("رقم الخطاب مطلوب"))

        # =================================================
        # تاريخ خطاب التوجيه
        # =================================================

        if not self.doc.directive_date:

            frappe.throw(
                _("يجب إدخال تاريخ خطاب التوجيه."), title=_("تاريخ الخطاب مطلوب")
            )
