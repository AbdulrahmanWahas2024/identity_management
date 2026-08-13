# # Copyright (c) 2026, Abdulrahman and contributors
# # For license information, please see license.txt

# import frappe
# from frappe.model.document import Document
# from identity_management.id_card_system.services.card_request_service import CardRequestService

# class CardRequest(Document):

#     def validate(self):
#         # يتم تشغيل التحقق دائماً قبل الحفظ
#         CardRequestService(self).validate_request()

#     def on_update(self):
#         # يُفضل استخدام on_update أو on_submit بدلاً من on_update_after_submit
#         # لضمان التقاط تغيير الـ workflow_state بشكل مضمون
#         CardRequestService(self).process_workflow()
# Copyright (c) 2026, Abdulrahman
# For license information, please see license.txt

# import frappe

# from frappe.model.document import Document

# from identity_management.id_card_system.services.card_request_service import (
#     CardRequestService
# )


# class CardRequest(Document):
    
#     def before_save(self):

#        service = CardRequestService(self)

#        service.validate_request()
    

#     def validate(self):
#         """
#         يعمل عند حفظ الطلب.
#         يستخدم للتحقق قبل اعتماد الموارد البشرية.
#         """

#         service = CardRequestService(self)

#         service.validate_request()



#     def on_update_after_submit(self):
#         """
#         يعمل بعد انتقال Workflow.
#         """

#         service = CardRequestService(self)

#         service.process_workflow()
 # Copyright (c) 2026, Abdulrahman and contributors
# For license information, please see license.txt


from frappe.model.document import Document

from identity_management.id_card_system.services.validation_service import ValidationService

from identity_management.id_card_system.services.workflow_service import WorkflowService

from identity_management.id_card_system.services.tracking_service import TrackingService




class CardRequest(Document):

    # ==================================================
    # قبل الحفظ
    # ==================================================

    def validate(self):


        validation = ValidationService(
            self
        )


        validation.validate_request()



    # ==================================================
    # بعد تغيير حالة Workflow
    # ==================================================

    def on_update(self):

        if self.flags.in_tracking:

         return


        self.flags.in_tracking = True


        tracking = TrackingService(self)

        tracking.record_workflow_change()
    #     self.save(
    #       ignore_permissions=True
    # )

        workflow = WorkflowService(self)

        workflow.process()
        frappe.flags.in_tracking = False