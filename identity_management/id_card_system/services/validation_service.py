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
# import frappe
# from frappe import _


# class ValidationService:

#     def __init__(self, doc):
#         self.doc = doc

#     # =====================================================
#     # تشغيل جميع عمليات التحقق
#     # =====================================================

#     def validate_request(self):

#         # 1. تحميل بيانات الموظف
#         self.load_employee_data()

#         # 2. التأكد من اختيار الموظف
#         self.validate_employee()

#         # 3. التحقق من نوع الموظف
#         self.validate_employment_type()

#         # 4. التحقق من اختيار نوع الطلب
#         self.validate_request_type()

#         # 5. التحقق من البطاقة الحالية
#         # مهم: يجب أن يحدث قبل reason والخطاب
#         self.validate_existing_card()

#         # 6. التحقق من بيانات الطلب
#         self.validate_request_data()

#     # =====================================================
#     # تحميل بيانات الموظف من Employee
#     # =====================================================

#     def load_employee_data(self):

#         if not self.doc.employee:
#             return

#         employee = frappe.get_doc("Employee", self.doc.employee)

#         self.doc.employee_name = employee.employee_name
#         self.doc.employee_number = employee.employee_number
#         self.doc.company = employee.company
#         self.doc.designation = employee.designation
#         self.doc.department = employee.department
#         self.doc.branch = employee.branch
#         self.doc.employment_type = employee.employment_type

#         # صورة الموظف من Employee
#         #
#         # إذا كان لدى الموظف صورة:
#         # يتم استخدامها تلقائياً
#         #
#         # وإذا لم توجد:
#         # يستطيع مختص تقنية المعلومات رفعها لاحقاً

#         if employee.image and not self.doc.employee_photo:
#             self.doc.employee_photo = employee.image

#     # =====================================================
#     # التأكد من اختيار الموظف
#     # =====================================================

#     def validate_employee(self):

#         if not self.doc.employee:

#             frappe.throw(_("يجب اختيار الموظف قبل حفظ الطلب."), title=_("الموظف مطلوب"))

#     # =====================================================
#     # التحقق من نوع الموظف
#     # =====================================================

#     def validate_employment_type(self):

#         blocked_types = ["متقاعد"]

#         if self.doc.employment_type in blocked_types:

#             frappe.throw(
#                 _(
#                     "لا يمكن إصدار بطاقة لهذا الموظف.<br>" "نوع الموظف: <b>{0}</b>"
#                 ).format(self.doc.employment_type),
#                 title=_("موظف غير مؤهل"),
#             )

#     # =====================================================
#     # التحقق من نوع الطلب
#     # =====================================================

#     def validate_request_type(self):

#         if not self.doc.request_type:

#             frappe.throw(_("يجب اختيار نوع الطلب."), title=_("نوع الطلب مطلوب"))

#     # =====================================================
#     # الحصول على اسم نوع الطلب
#     #
#     # Card Request
#     #       ↓
#     # request_type
#     #       ↓
#     # Card Request Type
#     #       ↓
#     # request_type_name
#     # =====================================================

#     def get_request_type_name(self):

#         if not self.doc.request_type:
#             return None

#         return frappe.db.get_value(
#             "Card Request Type", self.doc.request_type, "request_type_name"
#         )

#     # =====================================================
#     # البحث عن البطاقة الحالية للموظف
#     # =====================================================

#     def get_current_card(self):

#         if not self.doc.employee:
#             return None

#         cards = frappe.get_all(
#             "Employee Identity Card",
#             filters={"employee": self.doc.employee},
#             fields=["name", "card_number", "card_status", "expiry_date"],
#             order_by="creation desc",
#             limit=20,
#         )

#         if not cards:
#             return None

#         # الحالات التي تعتبر بطاقة قائمة/فعالة
#         active_statuses = [
#             "جديدة",
#             "بانتظار تقنية المعلومات",
#             "قيد التجهيز",
#             "جاهزة للطباعة",
#             "تمت الطباعة",
#             "تم التسليم",
#             "نشطة",
#         ]

#         for card in cards:

#             if card.card_status in active_statuses:

#                 return card

#         return None

#     # =====================================================
#     # التحقق من البطاقة الحالية
#     #
#     # هذا التحقق يحدث قبل reason والخطاب
#     # =====================================================

#     def validate_existing_card(self):

#         request_type = self.get_request_type_name()

#         current_card = self.get_current_card()

#         # =================================================
#         # إصدار جديد
#         #
#         # يجب ألا توجد بطاقة حالية
#         # =================================================

#         if request_type == "إصدار جديد":

#             if current_card:

#                 frappe.throw(
#                     f"""
#                     <b>الموظف:</b>
#                     {self.doc.employee_name}
#                     ({self.doc.employee_number})

#                     <br><br>

#                     توجد بطاقة حالية للموظف.

#                     <br>

#                     <b>رقم البطاقة:</b>
#                     {current_card.card_number}

#                     <br>

#                     <b>حالة البطاقة:</b>
#                     {current_card.card_status}

#                     <br><br>

#                     لا يمكن تقديم طلب إصدار جديد
#                     قبل إنهاء البطاقة الحالية.
#                     """,
#                     title=_("⚠️ توجد بطاقة حالية"),
#                 )

#             return

#         # =================================================
#         # الطلبات التي تحتاج بطاقة حالية
#         # =================================================

#         requests_require_card = ["بدل فاقد", "تجديد", "تعديل بيانات", "إلغاء"]

#         # =================================================
#         # إذا كان نوع الطلب يحتاج بطاقة
#         # =================================================

#         if request_type in requests_require_card:

#             # لا توجد بطاقة
#             if not current_card:

#                 frappe.throw(
#                     f"""
#                     <b>الموظف:</b>
#                     {self.doc.employee_name}

#                     <br><br>

#                     لا توجد بطاقة صادرة وحالية
#                     لهذا الموظف.

#                     <br><br>

#                     لا يمكن تقديم طلب:

#                     <b>{request_type}</b>

#                     <br><br>

#                     يجب أن تكون هناك بطاقة حالية
#                     للموظف قبل تنفيذ هذا الإجراء.
#                     """,
#                     title=_("⚠️ لا توجد بطاقة حالية"),
#                 )

#             # توجد بطاقة
#             return

#     # =====================================================
#     # التحقق من بيانات الطلب
#     #
#     # يتم استدعاؤها بعد التأكد من البطاقة
#     # =====================================================

#     def validate_request_data(self):

#         request_type = self.get_request_type_name()

#         # =================================================
#         # الأنواع التي تحتاج سبب
#         # =================================================

#         request_types_with_reason = ["بدل فاقد", "تجديد", "تعديل بيانات", "إلغاء"]

#         # =================================================
#         # التحقق من السبب
#         # =================================================

#         if request_type in request_types_with_reason:

#             if not self.doc.reason:

#                 messages = {
#                     "بدل فاقد": "يجب إدخال سبب فقدان البطاقة.",
#                     "تجديد": "يجب إدخال سبب التجديد.",
#                     "تعديل بيانات": "يجب إدخال سبب تعديل بيانات البطاقة.",
#                     "إلغاء": "يجب إدخال سبب إلغاء البطاقة.",
#                 }
#                 message = messages.get(request_type, "يجب إدخال سبب الطلب.")

#                 frappe.throw(
#                     _(messages.get(request_type, "يجب إدخال سبب الطلب.")),
#                     title=_("سبب الطلب مطلوب"),
#                     exc=frappe.MandatoryError,
#                 )

#         # =================================================
#         # خطاب التوجيه
#         # =================================================

#         if not self.doc.directive_attachment:

#             frappe.throw(_("يجب إرفاق خطاب التوجيه."), title=_("خطاب التوجيه مطلوب"))

#         # =================================================
#         # رقم خطاب التوجيه
#         # =================================================

#         if not self.doc.directive_number:

#             frappe.throw(_("يجب إدخال رقم خطاب التوجيه."), title=_("رقم الخطاب مطلوب"))

#         # =================================================
#         # تاريخ خطاب التوجيه
#         # =================================================

#         if not self.doc.directive_date:

#             frappe.throw(
#                 _("يجب إدخال تاريخ خطاب التوجيه."), title=_("تاريخ الخطاب مطلوب")
#             )
# import frappe
# from frappe import _


# class ValidationService:

#     def __init__(self, doc):
#         self.doc = doc

#     # =====================================================
#     # تشغيل جميع عمليات التحقق
#     # =====================================================

#     def validate_request(self):

#         # 1. تحميل بيانات الموظف
#         self.load_employee_data()

#         # 2. التأكد من اختيار الموظف
#         self.validate_employee()

#         # 3. التحقق من نوع الموظف
#         self.validate_employment_type()

#         # 4. التحقق من اختيار نوع الطلب
#         self.validate_request_type()

#         # 5. التحقق من وجود طلب سابق قيد المعالجة
#         self.validate_existing_request()

#         # 6. التحقق من البطاقة الحالية
#         self.validate_existing_card()

#         # 7. التحقق من بيانات الطلب
#         self.validate_request_data()

#     # =====================================================
#     # تحميل بيانات الموظف من Employee
#     # =====================================================

#     def load_employee_data(self):

#         if not self.doc.employee:
#             return

#         employee = frappe.get_doc("Employee", self.doc.employee)

#         self.doc.employee_name = employee.employee_name
#         self.doc.employee_number = employee.employee_number
#         self.doc.company = employee.company
#         self.doc.designation = employee.designation
#         self.doc.department = employee.department
#         self.doc.branch = employee.branch
#         self.doc.employment_type = employee.employment_type

#         # =================================================
#         # صورة الموظف من Employee
#         #
#         # إذا كان لدى الموظف صورة:
#         # يتم استخدامها تلقائياً
#         #
#         # وإذا لم توجد:
#         # يستطيع مختص تقنية المعلومات رفعها لاحقاً
#         # =================================================

#         if employee.image and not self.doc.employee_photo:

#             self.doc.employee_photo = employee.image

#     # =====================================================
#     # التأكد من اختيار الموظف
#     # =====================================================

#     def validate_employee(self):

#         if not self.doc.employee:

#             frappe.throw(_("يجب اختيار الموظف قبل حفظ الطلب."), title=_("الموظف مطلوب"))

#     # =====================================================
#     # التحقق من نوع الموظف
#     # =====================================================

#     def validate_employment_type(self):

#         blocked_types = ["متقاعد"]

#         if self.doc.employment_type in blocked_types:

#             frappe.throw(
#                 _(
#                     "لا يمكن إصدار بطاقة لهذا الموظف.<br>" "نوع الموظف: <b>{0}</b>"
#                 ).format(self.doc.employment_type),
#                 title=_("موظف غير مؤهل"),
#             )

#     # =====================================================
#     # التحقق من نوع الطلب
#     # =====================================================

#     def validate_request_type(self):

#         if not self.doc.request_type:

#             frappe.throw(_("يجب اختيار نوع الطلب."), title=_("نوع الطلب مطلوب"))

#     # =====================================================
#     # الحصول على اسم نوع الطلب
#     #
#     # Card Request
#     #       ↓
#     # request_type
#     #       ↓
#     # Card Request Type
#     #       ↓
#     # request_type_name
#     # =====================================================

#     def get_request_type_name(self):

#         if not self.doc.request_type:
#             return None

#         return frappe.db.get_value(
#             "Card Request Type", self.doc.request_type, "request_type_name"
#         )

#     # =====================================================
#     # التحقق من وجود طلب سابق قيد المعالجة
#     #
#     # يتم البحث مباشرة في قاعدة البيانات
#     # داخل Card Request
#     # =====================================================

#     def validate_existing_request(self):

#         # =================================================
#         # لا يوجد موظف
#         # =================================================

#         if not self.doc.employee:
#             return

#         # =================================================
#         # الحالات التي يعتبر فيها الطلب السابق
#         # ما زال قيد المعالجة
#         #
#         # هذه هي الحالات الفعلية في Workflow لديك
#         # =================================================

#         active_request_states = [
#             "Submitted",
#             "HR Review",
#             "HR Approved",
#             "IT Pending",
#             "Card Preparation",
#             "Ready for Print",
#             "Printed",
#             "Delivered",
#         ]

#         # =================================================
#         # البحث عن طلب سابق لنفس الموظف
#         # =================================================

#         filters = {
#             "employee": self.doc.employee,
#             "workflow_state": ["in", active_request_states],
#         }

#         # =================================================
#         # استبعاد الطلب الحالي
#         #
#         # حتى لا يعتبر النظام نفس الطلب
#         # طلباً سابقاً عند التعديل والحفظ
#         # =================================================

#         if self.doc.name and self.doc.name != "new-card-request":

#             filters["name"] = ["!=", self.doc.name]

#         # =================================================
#         # البحث المباشر في قاعدة البيانات
#         # =================================================

#         existing_request = frappe.db.get_value(
#             "Card Request",
#             filters,
#             ["name", "workflow_state", "request_type", "request_date"],
#             as_dict=True,
#         )

#         # =================================================
#         # لم يوجد طلب سابق
#         # =================================================

#         if not existing_request:
#             return

#         # =================================================
#         # الحصول على اسم نوع الطلب
#         # =================================================

#         request_type_name = None

#         if existing_request.request_type:

#             request_type_name = frappe.db.get_value(
#                 "Card Request Type", existing_request.request_type, "request_type_name"
#             )

#         # =================================================
#         # منع إنشاء الطلب
#         # =================================================

#         frappe.throw(
#             _("""
#                 <div style="
#                     direction:rtl;
#                     text-align:right;
#                     line-height:2;
#                     font-size:14px;
#                 ">

#                     <div style="
#                         text-align:center;
#                         font-size:18px;
#                         font-weight:700;
#                         color:#dc3545;
#                         margin-bottom:15px;
#                     ">
#                         ⚠ يوجد طلب بطاقة قيد المعالجة
#                     </div>

#                     <div>
#                         <b>الموظف:</b>
#                         {0}
#                     </div>

#                     <div>
#                         <b>الرقم الوظيفي:</b>
#                         {1}
#                     </div>

#                     <div>
#                         <b>رقم الطلب السابق:</b>
#                         {2}
#                     </div>

#                     <div>
#                         <b>نوع الطلب:</b>
#                         {3}
#                     </div>

#                     <div>
#                         <b>حالة الطلب:</b>
#                         {4}
#                     </div>

#                     <br>

#                     <div style="
#                         background:#fff3cd;
#                         padding:10px;
#                         border-radius:6px;
#                         border:1px solid #ffe69c;
#                     ">
#                         لا يمكن إنشاء طلب بطاقة جديد لهذا الموظف
#                         لأن لديه طلباً سابقاً ما زال قيد المعالجة.
#                     </div>

#                     <br>

#                     <div>
#                         يجب إكمال الطلب السابق أو إلغاؤه
#                         قبل تقديم طلب جديد.
#                     </div>

#                 </div>
#                 """).format(
#                 self.doc.employee_name or self.doc.employee or "-",
#                 self.doc.employee_number or "-",
#                 existing_request.name or "-",
#                 request_type_name or existing_request.request_type or "-",
#                 existing_request.workflow_state or "-",
#             ),
#             title=_("يوجد طلب سابق"),
#         )

#     # =====================================================
#     # البحث عن البطاقة الحالية للموظف
#     #
#     # يتم البحث مباشرة في:
#     # Employee Identity Card
#     # =====================================================

#     def get_current_card(self):

#         if not self.doc.employee:
#             return None

#         # =================================================
#         # الحالات التي تعتبر البطاقة فيها قائمة
#         # =================================================

#         active_card_statuses = [
#             "جديدة",
#             "بانتظار تقنية المعلومات",
#             "قيد التجهيز",
#             "جاهزة للطباعة",
#             "تمت الطباعة",
#             "تم التسليم",
#             "نشطة",
#         ]

#         # =================================================
#         # البحث المباشر في قاعدة البيانات
#         # =================================================

#         current_card = frappe.db.get_value(
#             "Employee Identity Card",
#             {
#                 "employee": self.doc.employee,
#                 "card_status": ["in", active_card_statuses],
#             },
#             ["name", "card_number", "card_status", "expiry_date"],
#             as_dict=True,
#         )

#         return current_card

#     # =====================================================
#     # التحقق من البطاقة الحالية
#     #
#     # هذا التحقق يحدث بعد التحقق من الطلب السابق
#     # =====================================================

#     def validate_existing_card(self):

#         request_type = self.get_request_type_name()

#         current_card = self.get_current_card()

#         # =================================================
#         # إصدار جديد
#         #
#         # يجب ألا توجد بطاقة حالية
#         # =================================================

#         if request_type == "إصدار جديد":

#             if current_card:

#                 frappe.throw(
#                     _("""
#                         <div style="
#                             direction:rtl;
#                             text-align:right;
#                             line-height:2;
#                             font-size:14px;
#                         ">

#                             <div style="
#                                 text-align:center;
#                                 font-size:18px;
#                                 font-weight:700;
#                                 color:#dc3545;
#                                 margin-bottom:15px;
#                             ">
#                                 ⚠️ توجد بطاقة حالية للموظف
#                             </div>

#                             <div>
#                                 <b>الموظف:</b>
#                                 {0}
#                             </div>

#                             <div>
#                                 <b>الرقم الوظيفي:</b>
#                                 {1}
#                             </div>

#                             <div>
#                                 <b>رقم البطاقة:</b>
#                                 {2}
#                             </div>

#                             <div>
#                                 <b>حالة البطاقة:</b>
#                                 {3}
#                             </div>

#                             <br>

#                             <div style="
#                                 background:#fff3cd;
#                                 padding:10px;
#                                 border-radius:6px;
#                                 border:1px solid #ffe69c;
#                             ">
#                                 لا يمكن تقديم طلب إصدار جديد
#                                 قبل إنهاء البطاقة الحالية.
#                             </div>

#                         </div>
#                         """).format(
#                         self.doc.employee_name or self.doc.employee or "-",
#                         self.doc.employee_number or "-",
#                         current_card.card_number or "-",
#                         current_card.card_status or "-",
#                     ),
#                     title=_("توجد بطاقة حالية"),
#                 )

#             return

#         # =================================================
#         # الطلبات التي تحتاج بطاقة حالية
#         # =================================================

#         requests_require_card = ["بدل فاقد", "تجديد", "تعديل بيانات", "إلغاء"]

#         # =================================================
#         # إذا كان نوع الطلب يحتاج بطاقة
#         # =================================================

#         if request_type in requests_require_card:

#             # =================================================
#             # لا توجد بطاقة
#             # =================================================

#             if not current_card:

#                 frappe.throw(
#                     _("""
#                         <div style="
#                             direction:rtl;
#                             text-align:right;
#                             line-height:2;
#                             font-size:14px;
#                         ">

#                             <div style="
#                                 text-align:center;
#                                 font-size:18px;
#                                 font-weight:700;
#                                 color:#dc3545;
#                                 margin-bottom:15px;
#                             ">
#                                 ⚠️ لا توجد بطاقة حالية
#                             </div>

#                             <div>
#                                 <b>الموظف:</b>
#                                 {0}
#                             </div>

#                             <br>

#                             <div>
#                                 لا توجد بطاقة صادرة وحالية
#                                 لهذا الموظف.
#                             </div>

#                             <br>

#                             <div>
#                                 لا يمكن تقديم طلب:
#                                 <b>{1}</b>
#                             </div>

#                             <br>

#                             <div style="
#                                 background:#fff3cd;
#                                 padding:10px;
#                                 border-radius:6px;
#                                 border:1px solid #ffe69c;
#                             ">
#                                 يجب أن تكون هناك بطاقة حالية
#                                 للموظف قبل تنفيذ هذا الإجراء.
#                             </div>

#                         </div>
#                         """).format(
#                         self.doc.employee_name or self.doc.employee or "-",
#                         request_type or "-",
#                     ),
#                     title=_("لا توجد بطاقة حالية"),
#                 )

#             # =================================================
#             # توجد بطاقة حالية
#             # =================================================

#             return

#     # =====================================================
#     # التحقق من بيانات الطلب
#     #
#     # يتم استدعاؤها بعد:
#     #
#     # 1. الموظف
#     # 2. نوع الموظف
#     # 3. نوع الطلب
#     # 4. الطلب السابق
#     # 5. البطاقة الحالية
#     # =====================================================

#     def validate_request_data(self):

#         request_type = self.get_request_type_name()

#         # =================================================
#         # الأنواع التي تحتاج سبب
#         # =================================================

#         request_types_with_reason = ["بدل فاقد", "تجديد", "تعديل بيانات", "إلغاء"]

#         # =================================================
#         # التحقق من السبب
#         # =================================================

#         if request_type in request_types_with_reason:

#             if not self.doc.reason:

#                 messages = {
#                     "بدل فاقد": "يجب إدخال سبب فقدان البطاقة.",
#                     "تجديد": "يجب إدخال سبب التجديد.",
#                     "تعديل بيانات": "يجب إدخال سبب تعديل بيانات البطاقة.",
#                     "إلغاء": "يجب إدخال سبب إلغاء البطاقة.",
#                 }

#                 message = messages.get(request_type, "يجب إدخال سبب الطلب.")

#                 frappe.throw(
#                     _(message), title=_("سبب الطلب مطلوب"), exc=frappe.MandatoryError
#                 )

#         # =================================================
#         # خطاب التوجيه
#         # =================================================

#         if not self.doc.directive_attachment:

#             frappe.throw(_("يجب إرفاق خطاب التوجيه."), title=_("خطاب التوجيه مطلوب"))

#         # =================================================
#         # رقم خطاب التوجيه
#         # =================================================

#         if not self.doc.directive_number:

#             frappe.throw(_("يجب إدخال رقم خطاب التوجيه."), title=_("رقم الخطاب مطلوب"))

#         # =================================================
#         # تاريخ خطاب التوجيه
#         # =================================================

#         if not self.doc.directive_date:

#             frappe.throw(
#                 _("يجب إدخال تاريخ خطاب التوجيه."), title=_("تاريخ الخطاب مطلوب")
#             )
# import frappe
# from frappe import _


# class ValidationService:

#     def __init__(self, doc):
#         self.doc = doc

#     # =====================================================
#     # تشغيل جميع عمليات التحقق
#     # =====================================================

#     def validate_request(self):

#         # 1. تحميل بيانات الموظف
#         self.load_employee_data()

#         # 2. التأكد من اختيار الموظف
#         self.validate_employee()

#         # 3. التحقق من نوع الموظف
#         self.validate_employment_type()

#         # 4. التحقق من اختيار نوع الطلب
#         self.validate_request_type()

#         # 5. التحقق من وجود طلب سابق قيد المعالجة
#         self.validate_existing_request()

#         # 6. التحقق من البطاقة الحالية
#         self.validate_existing_card()

#         # 7. التحقق من بيانات الطلب
#         self.validate_request_data()

#     # =====================================================
#     # تحميل بيانات الموظف من Employee
#     # =====================================================

#     def load_employee_data(self):

#         if not self.doc.employee:
#             return

#         employee = frappe.get_doc("Employee", self.doc.employee)

#         self.doc.employee_name = employee.employee_name
#         self.doc.employee_number = employee.employee_number
#         self.doc.company = employee.company
#         self.doc.designation = employee.designation
#         self.doc.department = employee.department
#         self.doc.branch = employee.branch
#         self.doc.employment_type = employee.employment_type

#         # =================================================
#         # صورة الموظف من Employee
#         # =================================================

#         if employee.image and not self.doc.employee_photo:
#             self.doc.employee_photo = employee.image

#     # =====================================================
#     # التأكد من اختيار الموظف
#     # =====================================================

#     def validate_employee(self):

#         if not self.doc.employee:

#             frappe.throw(_("يجب اختيار الموظف قبل حفظ الطلب."), title=_("الموظف مطلوب"))

#     # =====================================================
#     # التحقق من نوع الموظف
#     # =====================================================

#     def validate_employment_type(self):

#         blocked_types = ["متقاعد"]

#         if self.doc.employment_type in blocked_types:

#             frappe.throw(
#                 _(
#                     "لا يمكن إصدار بطاقة لهذا الموظف.<br>" "نوع الموظف: <b>{0}</b>"
#                 ).format(self.doc.employment_type),
#                 title=_("موظف غير مؤهل"),
#             )

#     # =====================================================
#     # التحقق من نوع الطلب
#     # =====================================================

#     def validate_request_type(self):

#         if not self.doc.request_type:

#             frappe.throw(_("يجب اختيار نوع الطلب."), title=_("نوع الطلب مطلوب"))

#     # =====================================================
#     # الحصول على اسم نوع الطلب
#     # =====================================================

#     def get_request_type_name(self):

#         if not self.doc.request_type:
#             return None

#         return frappe.db.get_value(
#             "Card Request Type", self.doc.request_type, "request_type_name"
#         )

#     # =====================================================
#     # التحقق من وجود طلب سابق قيد المعالجة
#     #
#     # ملاحظة مهمة:
#     #
#     # الطلبات التي وصلت إلى:
#     #
#     # Printed
#     # Delivered
#     #
#     # تعتبر مكتملة ولا تمنع الطلب الجديد.
#     #
#     # أما الطلبات التي ما زالت في مراحل المعالجة
#     # فتمنع إنشاء طلب جديد.
#     # =====================================================

#     def validate_existing_request(self):

#         if not self.doc.employee:
#             return

#         request_type = self.get_request_type_name()

#         # =================================================
#         # الحالات التي تعتبر الطلب فيها ما زال مفتوحًا
#         # =================================================

#         active_request_states = [
#             "Submitted",
#             "HR Review",
#             "HR Approved",
#             "IT Pending",
#             "Card Preparation",
#             "Ready for Print",
#         ]

#         # =================================================
#         # البحث المباشر في قاعدة البيانات
#         #
#         # لا يوجد limit
#         #
#         # قاعدة البيانات نفسها تبحث عن سجل مطابق.
#         # =================================================

#         filters = {
#             "employee": self.doc.employee,
#             "workflow_state": ["in", active_request_states],
#         }

#         # =================================================
#         # استبعاد الطلب الحالي
#         # =================================================

#         if self.doc.name and self.doc.name != "new-card-request":

#             filters["name"] = ["!=", self.doc.name]

#         # =================================================
#         # البحث المباشر
#         #
#         # نحتاج فقط إلى وجود سجل واحد.
#         # لا نحتاج تحميل جميع الطلبات.
#         # =================================================

#         existing_request = frappe.db.get_value(
#             "Card Request",
#             filters,
#             ["name", "workflow_state", "request_type", "request_date"],
#             as_dict=True,
#         )

#         # =================================================
#         # لا يوجد طلب سابق قيد المعالجة
#         # =================================================

#         if not existing_request:
#             return

#         # =================================================
#         # الحصول على اسم نوع الطلب السابق
#         # =================================================

#         previous_request_type_name = None

#         if existing_request.request_type:

#             previous_request_type_name = frappe.db.get_value(
#                 "Card Request Type", existing_request.request_type, "request_type_name"
#             )

#         # =================================================
#         # رسالة المنع
#         # =================================================

#         frappe.throw(
#             _("""
#                 <div style="
#                     direction:rtl;
#                     text-align:right;
#                     line-height:2;
#                     font-size:14px;
#                 ">

#                     <div style="
#                         text-align:center;
#                         font-size:18px;
#                         font-weight:700;
#                         color:#dc3545;
#                         margin-bottom:15px;
#                     ">
#                         ⚠ يوجد طلب بطاقة قيد المعالجة
#                     </div>

#                     <div>
#                         <b>الموظف:</b>
#                         {0}
#                     </div>

#                     <div>
#                         <b>الرقم الوظيفي:</b>
#                         {1}
#                     </div>

#                     <div>
#                         <b>رقم الطلب السابق:</b>
#                         {2}
#                     </div>

#                     <div>
#                         <b>نوع الطلب السابق:</b>
#                         {3}
#                     </div>

#                     <div>
#                         <b>حالة الطلب:</b>
#                         {4}
#                     </div>

#                     <br>

#                     <div style="
#                         background:#fff3cd;
#                         padding:12px;
#                         border-radius:6px;
#                         border:1px solid #ffe69c;
#                     ">

#                         لا يمكن تقديم طلب
#                         <b>{5}</b>
#                         حاليًا؛ لأن هناك طلبًا سابقًا
#                         للموظف ما زال قيد المعالجة.

#                     </div>

#                     <br>

#                     <div>
#                         يرجى إكمال الطلب السابق حتى يصل
#                         إلى مرحلة الطباعة أو التسليم،
#                         أو إلغاؤه حسب الصلاحيات المعتمدة،
#                         ثم تقديم الطلب الجديد.
#                     </div>

#                 </div>
#                 """).format(
#                 self.doc.employee_name or self.doc.employee or "-",
#                 self.doc.employee_number or "-",
#                 existing_request.name or "-",
#                 previous_request_type_name or existing_request.request_type or "-",
#                 existing_request.workflow_state or "-",
#                 request_type or "-",
#             ),
#             title=_("يوجد طلب سابق"),
#         )

#     # =====================================================
#     # البحث عن البطاقة الحالية
#     #
#     # يتم البحث مباشرة داخل:
#     #
#     # Employee Identity Card
#     #
#     # بدون limit.
#     # =====================================================

#     def get_current_card(self):

#         if not self.doc.employee:
#             return None

#         # =================================================
#         # الحالات التي تعتبر البطاقة موجودة
#         # =================================================

#         active_card_statuses = [
#             "جديدة",
#             "بانتظار تقنية المعلومات",
#             "قيد التجهيز",
#             "جاهزة للطباعة",
#             "تمت الطباعة",
#             "تم التسليم",
#             "نشطة",
#         ]

#         # =================================================
#         # البحث المباشر من قاعدة البيانات
#         # =================================================

#         current_card = frappe.db.get_value(
#             "Employee Identity Card",
#             {
#                 "employee": self.doc.employee,
#                 "card_status": ["in", active_card_statuses],
#             },
#             ["name", "card_number", "card_status", "issue_date", "expiry_date"],
#             as_dict=True,
#         )

#         return current_card

#     # =====================================================
#     # التحقق من اكتمال البطاقة
#     #
#     # هذه الدالة مهمة للطلبات:
#     #
#     # بدل فاقد
#     # تجديد
#     # تعديل بيانات
#     # إلغاء
#     #
#     # يجب أن تكون البطاقة السابقة قد اكتملت.
#     #
#     # الحالة المكتملة:
#     #
#     # تمت الطباعة
#     # أو
#     # تم التسليم
#     # =====================================================

#     def validate_card_completed_for_new_request(self, request_type, current_card):

#         if not current_card:

#             frappe.throw(
#                 _("""
#                     <div style="
#                         direction:rtl;
#                         text-align:right;
#                         line-height:2;
#                         font-size:14px;
#                     ">

#                         <div style="
#                             text-align:center;
#                             font-size:18px;
#                             font-weight:700;
#                             color:#dc3545;
#                             margin-bottom:15px;
#                         ">
#                             ⚠ لا توجد بطاقة مكتملة
#                         </div>

#                         <div>
#                             <b>الموظف:</b>
#                             {0}
#                         </div>

#                         <div>
#                             <b>الرقم الوظيفي:</b>
#                             {1}
#                         </div>

#                         <div>
#                             <b>نوع الطلب المطلوب:</b>
#                             {2}
#                         </div>

#                         <br>

#                         <div style="
#                             background:#fff3cd;
#                             padding:12px;
#                             border-radius:6px;
#                             border:1px solid #ffe69c;
#                         ">

#                             لا يمكن تنفيذ طلب
#                             <b>{2}</b>
#                             لأن الموظف لا توجد لديه
#                             بطاقة حالية مكتملة.

#                         </div>

#                         <br>

#                         <div>
#                             يجب أولاً إصدار البطاقة الحالية
#                             وإكمال إجراءات تجهيزها وطباعتها
#                             وتسليمها حسب الإجراءات المعتمدة.
#                         </div>

#                     </div>
#                     """).format(
#                     self.doc.employee_name or self.doc.employee or "-",
#                     self.doc.employee_number or "-",
#                     request_type or "-",
#                 ),
#                 title=_("البطاقة الحالية غير مكتملة"),
#             )

#         # =================================================
#         # الحالات التي تعتبر البطاقة مكتملة
#         # =================================================

#         completed_card_statuses = ["تمت الطباعة", "تم التسليم"]

#         # =================================================
#         # البطاقة لم تصل إلى مرحلة الاكتمال
#         # =================================================

#         if current_card.card_status not in completed_card_statuses:

#             action_message = (
#                 "يجب إكمال إجراءات البطاقة الحالية "
#                 "حتى يتم طباعة البطاقة على الأقل "
#                 "قبل تقديم هذا الطلب."
#             )

#             if request_type == "إلغاء":

#                 action_message = (
#                     "لا يمكن إلغاء البطاقة الحالية "
#                     "في هذه المرحلة. يجب إكمال إجراءات "
#                     "البطاقة الحالية وفق دورة العمل المعتمدة."
#                 )

#             elif request_type == "بدل فاقد":

#                 action_message = (
#                     "لا يمكن تقديم طلب بدل فاقد "
#                     "لأن البطاقة الحالية لم تكتمل طباعتها "
#                     "أو لم تصل إلى مرحلة التسليم."
#                 )

#             elif request_type == "تجديد":

#                 action_message = (
#                     "لا يمكن تقديم طلب تجديد "
#                     "لأن البطاقة الحالية لم تكتمل "
#                     "ولم يتم طباعة البطاقة."
#                 )

#             elif request_type == "تعديل بيانات":

#                 action_message = (
#                     "لا يمكن تقديم طلب تعديل بيانات "
#                     "لأن البطاقة الحالية لم تكتمل "
#                     "إجراءات إصدارها وطباعتها."
#                 )

#             frappe.throw(
#                 _("""
#                     <div style="
#                         direction:rtl;
#                         text-align:right;
#                         line-height:2;
#                         font-size:14px;
#                     ">

#                         <div style="
#                             text-align:center;
#                             font-size:18px;
#                             font-weight:700;
#                             color:#dc3545;
#                             margin-bottom:15px;
#                         ">
#                             ⚠ لا يمكن تقديم طلب {0}
#                         </div>

#                         <div>
#                             <b>الموظف:</b>
#                             {1}
#                         </div>

#                         <div>
#                             <b>الرقم الوظيفي:</b>
#                             {2}
#                         </div>

#                         <div>
#                             <b>نوع الطلب المطلوب:</b>
#                             {0}
#                         </div>

#                         <br>

#                         <div style="
#                             background:#fff3cd;
#                             padding:12px;
#                             border-radius:6px;
#                             border:1px solid #ffe69c;
#                         ">

#                             <b>البطاقة الحالية:</b>
#                             {3}

#                             <br>

#                             <b>حالة البطاقة:</b>
#                             {4}

#                         </div>

#                         <br>

#                         <div>
#                             {5}
#                         </div>

#                         <br>

#                         <div style="
#                             background:#e7f1ff;
#                             padding:12px;
#                             border-radius:6px;
#                             border:1px solid #b6d4fe;
#                         ">

#                             <b>الإجراء المطلوب:</b><br>
#                             يجب إكمال دورة البطاقة الحالية
#                             والوصول بها إلى مرحلة
#                             <b>تمت الطباعة</b>
#                             أو
#                             <b>تم التسليم</b>
#                             قبل تقديم طلب جديد من نوع
#                             <b>{0}</b>.

#                         </div>

#                     </div>
#                     """).format(
#                     request_type or "-",
#                     self.doc.employee_name or self.doc.employee or "-",
#                     self.doc.employee_number or "-",
#                     current_card.card_number or "-",
#                     current_card.card_status or "-",
#                     action_message,
#                 ),
#                 title=_("البطاقة لم تكتمل"),
#             )

#         # =================================================
#         # البطاقة مكتملة
#         # =================================================

#         return True

#     # =====================================================
#     # التحقق من البطاقة الحالية
#     # =====================================================

#     def validate_existing_card(self):

#         request_type = self.get_request_type_name()

#         current_card = self.get_current_card()

#         # =================================================
#         # إصدار جديد
#         #
#         # يجب ألا توجد بطاقة حالية.
#         # =================================================

#         if request_type == "إصدار جديد":

#             if current_card:

#                 frappe.throw(
#                     _("""
#                         <div style="
#                             direction:rtl;
#                             text-align:right;
#                             line-height:2;
#                             font-size:14px;
#                         ">

#                             <div style="
#                                 text-align:center;
#                                 font-size:18px;
#                                 font-weight:700;
#                                 color:#dc3545;
#                                 margin-bottom:15px;
#                             ">
#                                 ⚠️ توجد بطاقة حالية للموظف
#                             </div>

#                             <div>
#                                 <b>الموظف:</b>
#                                 {0}
#                             </div>

#                             <div>
#                                 <b>الرقم الوظيفي:</b>
#                                 {1}
#                             </div>

#                             <div>
#                                 <b>رقم البطاقة:</b>
#                                 {2}
#                             </div>

#                             <div>
#                                 <b>حالة البطاقة:</b>
#                                 {3}
#                             </div>

#                             <br>

#                             <div style="
#                                 background:#fff3cd;
#                                 padding:10px;
#                                 border-radius:6px;
#                                 border:1px solid #ffe69c;
#                             ">

#                                 لا يمكن تقديم طلب إصدار جديد
#                                 لأن الموظف لديه بطاقة حالية.

#                             </div>

#                             <br>

#                             <div>
#                                 يجب إكمال البطاقة الحالية
#                                 أو اتخاذ الإجراء الإداري المناسب
#                                 قبل إصدار بطاقة جديدة.
#                             </div>

#                         </div>
#                         """).format(
#                         self.doc.employee_name or self.doc.employee or "-",
#                         self.doc.employee_number or "-",
#                         current_card.card_number or "-",
#                         current_card.card_status or "-",
#                     ),
#                     title=_("توجد بطاقة حالية"),
#                 )

#             return

#         # =================================================
#         # الطلبات التي تحتاج بطاقة حالية مكتملة
#         # =================================================

#         requests_require_completed_card = ["بدل فاقد", "تجديد", "تعديل بيانات", "إلغاء"]

#         # =================================================
#         # التحقق من البطاقة للطلبات الخاصة
#         # =================================================

#         if request_type in requests_require_completed_card:

#             self.validate_card_completed_for_new_request(request_type, current_card)

#             return

#     # =====================================================
#     # التحقق من بيانات الطلب
#     # =====================================================

#     def validate_request_data(self):

#         request_type = self.get_request_type_name()

#         # =================================================
#         # الأنواع التي تحتاج سبب
#         # =================================================

#         request_types_with_reason = ["بدل فاقد", "تجديد", "تعديل بيانات", "إلغاء"]

#         # =================================================
#         # التحقق من السبب
#         # =================================================

#         if request_type in request_types_with_reason:

#             if not self.doc.reason:

#                 messages = {
#                     "بدل فاقد": "يجب إدخال سبب فقدان البطاقة.",
#                     "تجديد": "يجب إدخال سبب التجديد.",
#                     "تعديل بيانات": "يجب إدخال سبب تعديل بيانات البطاقة.",
#                     "إلغاء": "يجب إدخال سبب إلغاء البطاقة.",
#                 }

#                 message = messages.get(request_type, "يجب إدخال سبب الطلب.")

#                 frappe.throw(
#                     _(message), title=_("سبب الطلب مطلوب"), exc=frappe.MandatoryError
#                 )

#         # =================================================
#         # خطاب التوجيه
#         # =================================================

#         if not self.doc.directive_attachment:

#             frappe.throw(_("يجب إرفاق خطاب التوجيه."), title=_("خطاب التوجيه مطلوب"))

#         # =================================================
#         # رقم خطاب التوجيه
#         # =================================================

#         if not self.doc.directive_number:

#             frappe.throw(_("يجب إدخال رقم خطاب التوجيه."), title=_("رقم الخطاب مطلوب"))

#         # =================================================
#         # تاريخ خطاب التوجيه
#         # =================================================

#         if not self.doc.directive_date:

#             frappe.throw(
#                 _("يجب إدخال تاريخ خطاب التوجيه."), title=_("تاريخ الخطاب مطلوب")
#             )
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

        # 5. التحقق من وجود طلب سابق قيد المعالجة
        self.validate_existing_request()

        # 6. التحقق من البطاقة الحالية
        self.validate_existing_card()

        # 7. التحقق من قرار التعيين / الترقية
        #
        # مهم:
        # يتم تنفيذ هذا التحقق بعد التأكد من الموظف
        # ونوع الطلب والطلبات السابقة والبطاقة الحالية.
        #
        self.validate_appointment_promotion_decision()

        # 8. التحقق من بيانات الطلب
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

        # =================================================
        # صورة الموظف من Employee
        #
        # الصورة غير إلزامية.
        #
        # إذا كانت موجودة في Employee يتم جلبها إلى
        # Card Request فقط إذا لم تكن هناك صورة موجودة.
        # =================================================

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
    # =====================================================

    def get_request_type_name(self):

        if not self.doc.request_type:
            return None

        return frappe.db.get_value(
            "Card Request Type", self.doc.request_type, "request_type_name"
        )

    # =====================================================
    # التحقق من وجود طلب سابق قيد المعالجة
    #
    # الطلبات التي وصلت إلى:
    #
    # Printed
    # Delivered
    #
    # تعتبر مكتملة ولا تمنع الطلب الجديد.
    # =====================================================

    def validate_existing_request(self):

        if not self.doc.employee:
            return

        request_type = self.get_request_type_name()

        # =================================================
        # الحالات التي تعتبر الطلب فيها ما زال مفتوحًا
        # =================================================

        active_request_states = [
            "Submitted",
            "HR Review",
            "HR Approved",
            "IT Pending",
            "Card Preparation",
            "Ready for Print",
        ]

        # =================================================
        # البحث المباشر في قاعدة البيانات
        # =================================================

        filters = {
            "employee": self.doc.employee,
            "workflow_state": ["in", active_request_states],
        }

        # =================================================
        # استبعاد الطلب الحالي
        # =================================================

        if self.doc.name and self.doc.name != "new-card-request":

            filters["name"] = ["!=", self.doc.name]

        # =================================================
        # البحث عن طلب سابق
        # =================================================

        existing_request = frappe.db.get_value(
            "Card Request",
            filters,
            ["name", "workflow_state", "request_type", "request_date"],
            as_dict=True,
        )

        # =================================================
        # لا يوجد طلب سابق
        # =================================================

        if not existing_request:
            return

        # =================================================
        # الحصول على اسم نوع الطلب السابق
        # =================================================

        previous_request_type_name = None

        if existing_request.request_type:

            previous_request_type_name = frappe.db.get_value(
                "Card Request Type", existing_request.request_type, "request_type_name"
            )

        # =================================================
        # رسالة المنع
        # =================================================

        frappe.throw(
            _("""
                <div style="
                    direction:rtl;
                    text-align:right;
                    line-height:2;
                    font-size:14px;
                ">

                    <div style="
                        text-align:center;
                        font-size:18px;
                        font-weight:700;
                        color:#dc3545;
                        margin-bottom:15px;
                    ">
                        ⚠ يوجد طلب بطاقة قيد المعالجة
                    </div>

                    <div>
                        <b>الموظف:</b>
                        {0}
                    </div>

                    <div>
                        <b>الرقم الوظيفي:</b>
                        {1}
                    </div>

                    <div>
                        <b>رقم الطلب السابق:</b>
                        {2}
                    </div>

                    <div>
                        <b>نوع الطلب السابق:</b>
                        {3}
                    </div>

                    <div>
                        <b>حالة الطلب:</b>
                        {4}
                    </div>

                    <br>

                    <div style="
                        background:#fff3cd;
                        padding:12px;
                        border-radius:6px;
                        border:1px solid #ffe69c;
                    ">

                        لا يمكن تقديم طلب
                        <b>{5}</b>
                        حاليًا؛ لأن هناك طلبًا سابقًا
                        للموظف ما زال قيد المعالجة.

                    </div>

                    <br>

                    <div>
                        يرجى إكمال الطلب السابق حتى يصل
                        إلى مرحلة الطباعة أو التسليم،
                        أو إلغاؤه حسب الصلاحيات المعتمدة،
                        ثم تقديم الطلب الجديد.
                    </div>

                </div>
                """).format(
                self.doc.employee_name or self.doc.employee or "-",
                self.doc.employee_number or "-",
                existing_request.name or "-",
                previous_request_type_name or existing_request.request_type or "-",
                existing_request.workflow_state or "-",
                request_type or "-",
            ),
            title=_("يوجد طلب سابق"),
        )

    # =====================================================
    # البحث عن البطاقة الحالية
    # =====================================================

    def get_current_card(self):

        if not self.doc.employee:
            return None

        # =================================================
        # الحالات التي تعتبر البطاقة موجودة
        # =================================================

        active_card_statuses = [
            "جديدة",
            "بانتظار تقنية المعلومات",
            "قيد التجهيز",
            "جاهزة للطباعة",
            "تمت الطباعة",
            "تم التسليم",
            "نشطة",
        ]

        # =================================================
        # البحث المباشر من قاعدة البيانات
        # =================================================

        current_card = frappe.db.get_value(
            "Employee Identity Card",
            {
                "employee": self.doc.employee,
                "card_status": ["in", active_card_statuses],
            },
            ["name", "card_number", "card_status", "issue_date", "expiry_date"],
            as_dict=True,
        )

        return current_card

    # =====================================================
    # التحقق من اكتمال البطاقة
    # =====================================================

    def validate_card_completed_for_new_request(self, request_type, current_card):

        if not current_card:

            frappe.throw(
                _("""
                    <div style="
                        direction:rtl;
                        text-align:right;
                        line-height:2;
                        font-size:14px;
                    ">

                        <div style="
                            text-align:center;
                            font-size:18px;
                            font-weight:700;
                            color:#dc3545;
                            margin-bottom:15px;
                        ">
                            ⚠ لا توجد بطاقة مكتملة
                        </div>

                        <div>
                            <b>الموظف:</b>
                            {0}
                        </div>

                        <div>
                            <b>الرقم الوظيفي:</b>
                            {1}
                        </div>

                        <div>
                            <b>نوع الطلب المطلوب:</b>
                            {2}
                        </div>

                        <br>

                        <div style="
                            background:#fff3cd;
                            padding:12px;
                            border-radius:6px;
                            border:1px solid #ffe69c;
                        ">

                            لا يمكن تنفيذ طلب
                            <b>{2}</b>
                            لأن الموظف لا توجد لديه
                            بطاقة حالية مكتملة.

                        </div>

                        <br>

                        <div>
                            يجب أولاً إصدار البطاقة الحالية
                            وإكمال إجراءات تجهيزها وطباعتها
                            وتسليمها حسب الإجراءات المعتمدة.
                        </div>

                    </div>
                    """).format(
                    self.doc.employee_name or self.doc.employee or "-",
                    self.doc.employee_number or "-",
                    request_type or "-",
                ),
                title=_("البطاقة الحالية غير مكتملة"),
            )

        # =================================================
        # الحالات التي تعتبر البطاقة مكتملة
        # =================================================

        completed_card_statuses = ["تمت الطباعة", "تم التسليم"]

        # =================================================
        # البطاقة لم تصل إلى مرحلة الاكتمال
        # =================================================

        if current_card.card_status not in completed_card_statuses:

            action_message = (
                "يجب إكمال إجراءات البطاقة الحالية "
                "حتى يتم طباعة البطاقة على الأقل "
                "قبل تقديم هذا الطلب."
            )

            if request_type == "إلغاء":

                action_message = (
                    "لا يمكن إلغاء البطاقة الحالية "
                    "في هذه المرحلة. يجب إكمال إجراءات "
                    "البطاقة الحالية وفق دورة العمل المعتمدة."
                )

            elif request_type == "بدل فاقد":

                action_message = (
                    "لا يمكن تقديم طلب بدل فاقد "
                    "لأن البطاقة الحالية لم تكتمل طباعتها "
                    "أو لم تصل إلى مرحلة التسليم."
                )

            elif request_type == "تجديد":

                action_message = (
                    "لا يمكن تقديم طلب تجديد "
                    "لأن البطاقة الحالية لم تكتمل "
                    "ولم يتم طباعة البطاقة."
                )

            elif request_type == "تعديل بيانات":

                action_message = (
                    "لا يمكن تقديم طلب تعديل بيانات "
                    "لأن البطاقة الحالية لم تكتمل "
                    "إجراءات إصدارها وطباعتها."
                )

            frappe.throw(
                _("""
                    <div style="
                        direction:rtl;
                        text-align:right;
                        line-height:2;
                        font-size:14px;
                    ">

                        <div style="
                            text-align:center;
                            font-size:18px;
                            font-weight:700;
                            color:#dc3545;
                            margin-bottom:15px;
                        ">
                            ⚠ لا يمكن تقديم طلب {0}
                        </div>

                        <div>
                            <b>الموظف:</b>
                            {1}
                        </div>

                        <div>
                            <b>الرقم الوظيفي:</b>
                            {2}
                        </div>

                        <div>
                            <b>نوع الطلب المطلوب:</b>
                            {0}
                        </div>

                        <br>

                        <div style="
                            background:#fff3cd;
                            padding:12px;
                            border-radius:6px;
                            border:1px solid #ffe69c;
                        ">

                            <b>البطاقة الحالية:</b>
                            {3}

                            <br>

                            <b>حالة البطاقة:</b>
                            {4}

                        </div>

                        <br>

                        <div>
                            {5}
                        </div>

                        <br>

                        <div style="
                            background:#e7f1ff;
                            padding:12px;
                            border-radius:6px;
                            border:1px solid #b6d4fe;
                        ">

                            <b>الإجراء المطلوب:</b><br>

                            يجب إكمال دورة البطاقة الحالية
                            والوصول بها إلى مرحلة
                            <b>تمت الطباعة</b>
                            أو
                            <b>تم التسليم</b>
                            قبل تقديم طلب جديد من نوع
                            <b>{0}</b>.

                        </div>

                    </div>
                    """).format(
                    request_type or "-",
                    self.doc.employee_name or self.doc.employee or "-",
                    self.doc.employee_number or "-",
                    current_card.card_number or "-",
                    current_card.card_status or "-",
                    action_message,
                ),
                title=_("البطاقة لم تكتمل"),
            )

        return True

    # =====================================================
    # التحقق من البطاقة الحالية
    # =====================================================

    def validate_existing_card(self):

        request_type = self.get_request_type_name()

        current_card = self.get_current_card()

        # =================================================
        # إصدار جديد
        #
        # يجب ألا توجد بطاقة حالية.
        # =================================================

        if request_type == "إصدار جديد":

            if current_card:

                frappe.throw(
                    _("""
                        <div style="
                            direction:rtl;
                            text-align:right;
                            line-height:2;
                            font-size:14px;
                        ">

                            <div style="
                                text-align:center;
                                font-size:18px;
                                font-weight:700;
                                color:#dc3545;
                                margin-bottom:15px;
                            ">
                                ⚠️ توجد بطاقة حالية للموظف
                            </div>

                            <div>
                                <b>الموظف:</b>
                                {0}
                            </div>

                            <div>
                                <b>الرقم الوظيفي:</b>
                                {1}
                            </div>

                            <div>
                                <b>رقم البطاقة:</b>
                                {2}
                            </div>

                            <div>
                                <b>حالة البطاقة:</b>
                                {3}
                            </div>

                            <br>

                            <div style="
                                background:#fff3cd;
                                padding:10px;
                                border-radius:6px;
                                border:1px solid #ffe69c;
                            ">

                                لا يمكن تقديم طلب إصدار جديد
                                لأن الموظف لديه بطاقة حالية.

                            </div>

                            <br>

                            <div>
                                يجب إكمال البطاقة الحالية
                                أو اتخاذ الإجراء الإداري المناسب
                                قبل إصدار بطاقة جديدة.
                            </div>

                        </div>
                        """).format(
                        self.doc.employee_name or self.doc.employee or "-",
                        self.doc.employee_number or "-",
                        current_card.card_number or "-",
                        current_card.card_status or "-",
                    ),
                    title=_("توجد بطاقة حالية"),
                )

            return

        # =================================================
        # الطلبات التي تحتاج بطاقة حالية مكتملة
        # =================================================

        requests_require_completed_card = ["بدل فاقد", "تجديد", "تعديل بيانات", "إلغاء"]

        # =================================================
        # التحقق من البطاقة للطلبات الخاصة
        # =================================================

        if request_type in requests_require_completed_card:

            self.validate_card_completed_for_new_request(request_type, current_card)

            return

    # =====================================================
    # التحقق من قرار التعيين / الترقية
    #
    # هذه الدالة يتم تنفيذها بعد:
    #
    # 1. التحقق من الموظف
    # 2. التحقق من نوع الطلب
    # 3. التحقق من الطلبات السابقة
    # 4. التحقق من البطاقة الحالية
    #
    # وبالتالي لن تظهر رسالة القرار قبل معرفة
    # أن الموظف مؤهل لتقديم الطلب.
    #
    # =====================================================

    def validate_appointment_promotion_decision(self):

        # =================================================
        # التأكد من وجود الموظف
        # =================================================

        if not self.doc.employee:
            return

        # =================================================
        # الحصول على نوع الطلب
        # =================================================

        request_type = self.get_request_type_name()

        # =================================================
        # إذا لم يتم تحديد نوع الطلب
        # نترك التحقق للدالة الخاصة بنوع الطلب.
        # =================================================

        if not request_type:
            return

        # =================================================
        # اسم حقل قرار التعيين / الترقية
        #
        # يجب أن يكون Fieldname في Card Request:
        #
        # appointment_promotion_decision
        # =================================================

        decision_attachment = getattr(self.doc, "appointment_promotion_decision", None)

        # =================================================
        # تنظيف القيمة
        #
        # نعتبر None أو قيمة فارغة أو مسافات فقط
        # على أنها غير موجودة.
        # =================================================

        if decision_attachment:
            decision_attachment = str(decision_attachment).strip()

        # =================================================
        # إذا كان القرار موجودًا
        # يسمح النظام بالاستمرار.
        # =================================================

        if decision_attachment:
            return

        # =================================================
        # القرار غير موجود
        #
        # نوقف العملية الآن.
        # =================================================

        frappe.throw(
            _("""
                <div style="
                    direction:rtl;
                    text-align:right;
                    line-height:2;
                    font-size:14px;
                ">

                    <div style="
                        text-align:center;
                        font-size:19px;
                        font-weight:700;
                        color:#dc3545;
                        margin-bottom:15px;
                    ">
                        ⚠ يجب إرفاق قرار التعيين / الترقية
                    </div>

                    <div>
                        <b>الموظف:</b>
                        {0}
                    </div>

                    <div>
                        <b>الرقم الوظيفي:</b>
                        {1}
                    </div>

                    <div>
                        <b>نوع الطلب:</b>
                        {2}
                    </div>

                    <br>

                    <div style="
                        background:#fff3cd;
                        padding:12px;
                        border-radius:6px;
                        border:1px solid #ffe69c;
                    ">

                        لم يتم إرفاق
                        <b>قرار التعيين / الترقية</b>
                        في طلب البطاقة.

                    </div>

                    <br>

                    <div>
                        يرجى إرفاق القرار في الحقل المخصص
                        ثم حفظ الطلب مرة أخرى.
                    </div>

                </div>
                """).format(
                self.doc.employee_name or self.doc.employee or "-",
                self.doc.employee_number or "-",
                request_type or "-",
            ),
            title=_("قرار التعيين / الترقية مطلوب"),
        )

    # =====================================================
    # التحقق من بيانات الطلب
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
                    _(message), title=_("سبب الطلب مطلوب"), exc=frappe.MandatoryError
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
