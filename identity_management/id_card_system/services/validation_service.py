import frappe
from frappe import _


class ValidationService:


    def __init__(self, doc):

        # استلام مستند طلب البطاقة الحالي
        self.doc = doc



    # =====================================================
    # تشغيل جميع عمليات التحقق قبل حفظ الطلب
    # =====================================================

    def validate_request(self):

        # جلب بيانات الموظف من جدول Employee
        self.load_employee_data()


        # التأكد أن الموظف تم اختياره
        self.validate_employee()


        # التأكد من نوع الموظف
        self.validate_employment_type()


        # البحث عن بطاقة سابقة
        self.validate_existing_card()



    # =====================================================
    # جلب بيانات الموظف تلقائياً
    # المصدر:
    # Employee Doctype
    # =====================================================

    def load_employee_data(self):


        if not self.doc.employee:

            return



        employee = frappe.get_doc(
            "Employee",
            self.doc.employee
        )



        # تعبئة بيانات الطلب من بيانات الموظف

        self.doc.employee_name = employee.employee_name

        self.doc.employee_number = employee.employee_number

        self.doc.company = employee.company

        self.doc.designation = employee.designation

        self.doc.department = employee.department

        self.doc.branch = employee.branch

        self.doc.employment_type = employee.employment_type




    # =====================================================
    # التأكد من اختيار الموظف
    # =====================================================

    def validate_employee(self):


        if not self.doc.employee:


            frappe.throw(
                _("يجب اختيار الموظف قبل حفظ الطلب.")
            )




    # =====================================================
    # التحقق من نوع الموظف
    #
    # المصدر:
    # Employee -> Employment Type
    #
    # يمنع:
    # متقاعد
    # =====================================================

    def validate_employment_type(self):


        blocked_types = [

            "متقاعد"

        ]



        if self.doc.employment_type in blocked_types:



            frappe.throw(
                f"""
لا يمكن إصدار بطاقة لهذا الموظف.

نوع الموظف:
{self.doc.employment_type}
"""
            )





    # =====================================================
    # التحقق من وجود بطاقة سابقة
    #
    # البحث بواسطة الموظف
    #
    # يمنع إصدار بطاقة ثانية
    # =====================================================

    def validate_existing_card(self):



        cards = frappe.get_all(

            "Employee Identity Card",


            filters={

                "employee": self.doc.employee

            },


            fields=[

                "name",

                "card_number",

                "card_status",

                "expiry_date"

            ],


            order_by="creation desc"

        )



        # لا توجد بطاقة سابقة

        if not cards:

            return





        # الحالات التي تمنع إصدار بطاقة جديدة

        active_status = [

            "جديدة",

            "بانتظار تقنية المعلومات",

            "قيد التجهيز",

            "جاهزة للطباعة",

            "تمت الطباعة",

            "تم التسليم",

            "نشطة",

            "موقفة"

        ]





        for card in cards:



            if card.card_status in active_status:



#                 frappe.throw(

# f"""
# <b>الموظف:</b> {self.doc.employee_name}

# <b>الرقم الوظيفي:</b> {self.doc.employee_number}


# يوجد بطاقة سابقة:

# <b>رقم البطاقة:</b>
# {card.card_number}


# <b>حالة البطاقة:</b>
# {card.card_status}


# لا يمكن إصدار بطاقة جديدة.

# يرجى إلغاء أو إنهاء البطاقة السابقة أولاً.
# """,

# title="⚠️ يوجد بطاقة سابقة"

# )     
                frappe.throw(
    f"""
    <b>للموظف:</b> {self.doc.employee_name} ({self.doc.employee_number})<br>
    لديه بطاقة حالية برقم: <b>{card.card_number}</b> (الحالة: <b>{card.card_status}</b>).<br><br>
    <span style="color: #d9534f;">يرجى إلغاء أو إنهاء صلاحية البطاقة السابقة قبل إصدار بطاقة جديدة.</span>
    """,
    title="⚠️ لا يمكن إصدار بطاقة جديدة"
)