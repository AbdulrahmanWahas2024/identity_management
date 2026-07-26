# Copyright (c) 2026, Abdulrahman and contributors
# For license information, please see license.txt

# import frappe
import frappe
from frappe.model.document import Document

from identity_management.id_card_system.services.card_request_service import (
    CardRequestService,
)


class CardRequest(Document):

    def on_update_after_submit(self):

        if self.workflow_state == "Card Preparation":

            service = CardRequestService(self)

            service.create_employee_identity_card()