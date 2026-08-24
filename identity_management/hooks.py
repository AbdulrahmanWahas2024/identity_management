# app_name = "identity_management"
# app_title = "ID_Card_System"
# app_publisher = "Abdulrahman"
# app_description = "ID for Staff"
# app_email = "al.wahaas2200@gmail.com"
# app_license = "mit"
# # قائمة الموديولات المعنية لتجميع التصدير الآلي
# MODULES = ["ID_Card_System", "ID Card System", "Identity Management"]

# # Apps
# # ------------------

# # required_apps = []

# # Each item in the list will be shown as an app in the apps page
# # add_to_apps_screen = [
# # 	{
# # 		"name": "identity_management",
# # 		"logo": "/assets/identity_management/logo.png",
# # 		"title": "ID_Card_System",
# # 		"route": "/identity_management",
# # 		"has_permission": "identity_management.api.permission.has_app_permission"
# # 	}
# # ]

# # Includes in <head>
# # ------------------

# # include js, css files in header of desk.html
# # app_include_css = "/assets/identity_management/css/identity_management.css"
# # app_include_js = "/assets/identity_management/js/identity_management.js"

# # include js, css files in header of web template
# # web_include_css = "/assets/identity_management/css/identity_management.css"
# # web_include_js = "/assets/identity_management/js/identity_management.js"

# # include custom scss in every website theme (without file extension ".scss")
# # website_theme_scss = "identity_management/public/scss/website"

# # include js, css files in header of web form
# # webform_include_js = {"doctype": "public/js/doctype.js"}
# # webform_include_css = {"doctype": "public/css/doctype.css"}

# # include js in page
# # page_js = {"page" : "public/js/file.js"}

# # include js in doctype views
# # doctype_js = {"doctype" : "public/js/doctype.js"}
# # doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# # doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# # doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# # Svg Icons
# # ------------------
# # include app icons in desk
# # app_include_icons = "identity_management/public/icons.svg"

# # Home Pages
# # ----------

# # application home page (will override Website Settings)
# # home_page = "login"

# # website user home page (by Role)
# # role_home_page = {
# # 	"Role": "home_page"
# # }

# # Generators
# # ----------

# # automatically create page for each record of this doctype
# # website_generators = ["Web Page"]

# # Jinja
# # ----------

# # add methods and filters to jinja environment
# # jinja = {
# # 	"methods": "identity_management.utils.jinja_methods",
# # 	"filters": "identity_management.utils.jinja_filters"
# # }

# # Installation
# # ------------

# # before_install = "identity_management.install.before_install"
# # after_install = "identity_management.install.after_install"

# # Uninstallation
# # ------------

# # before_uninstall = "identity_management.uninstall.before_uninstall"
# # after_uninstall = "identity_management.uninstall.after_uninstall"

# # Integration Setup
# # ------------------
# # To set up dependencies/integrations with other apps
# # Name of the app being installed is passed as an argument

# # before_app_install = "identity_management.utils.before_app_install"
# # after_app_install = "identity_management.utils.after_app_install"

# # Integration Cleanup
# # -------------------
# # To clean up dependencies/integrations with other apps
# # Name of the app being uninstalled is passed as an argument

# # before_app_uninstall = "identity_management.utils.before_app_uninstall"
# # after_app_uninstall = "identity_management.utils.after_app_uninstall"

# # Desk Notifications
# # ------------------
# # See frappe.core.notifications.get_notification_config

# # notification_config = "identity_management.notifications.get_notification_config"

# # Permissions
# # -----------
# # Permissions evaluated in scripted ways

# # permission_query_conditions = {
# # 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# # }
# #
# # has_permission = {
# # 	"Event": "frappe.desk.doctype.event.event.has_permission",
# # }

# # DocType Class
# # ---------------
# # Override standard doctype classes

# # override_doctype_class = {
# # 	"ToDo": "custom_app.overrides.CustomToDo"
# # }

# # Document Events
# # ---------------
# # Hook on document methods and events

# # doc_events = {
# # 	"*": {
# # 		"on_update": "identity_management.id_card_system.services.card_request_service.update",
# # 		"on_cancel": "identity_management.id_card_system.services.card_request_service.cancel",
# # 		"on_cancel": "method",
# # 		"on_trash": "method",
# #     "validate": "identity_management.id_card_system.services.card_request_service.validate",
# # 	}
# # }

# # Scheduled Tasks
# # ---------------

# # scheduler_events = {
# # 	"all": [
# # 		"identity_management.tasks.all"
# # 	],
# # 	"daily": [
# # 		"identity_management.tasks.daily"
# # 	],
# # 	"hourly": [
# # 		"identity_management.tasks.hourly"
# # 	],
# # 	"weekly": [
# # 		"identity_management.tasks.weekly"
# # 	],
# # 	"monthly": [
# # 		"identity_management.tasks.monthly"
# # 	],
# # }

# # Testing
# # -------

# # before_tests = "identity_management.install.before_tests"

# # Overriding Methods
# # ------------------------------
# #
# # override_whitelisted_methods = {
# # 	"frappe.desk.doctype.event.event.get_events": "identity_management.event.get_events"
# # }
# #
# # each overriding function accepts a `data` argument;
# # generated from the base implementation of the doctype dashboard,
# # along with any modifications made in other Frappe apps
# # override_doctype_dashboards = {
# # 	"Task": "identity_management.task.get_dashboard_data"
# # }

# # exempt linked doctypes from being automatically cancelled
# #
# # auto_cancel_exempted_doctypes = ["Auto Repeat"]

# # Ignore links to specified DocTypes when deleting documents
# # -----------------------------------------------------------

# # ignore_links_on_delete = ["Communication", "ToDo"]

# # Request Events
# # ----------------
# # before_request = ["identity_management.utils.before_request"]
# # after_request = ["identity_management.utils.after_request"]

# # Job Events
# # ----------
# # before_job = ["identity_management.utils.before_job"]
# # after_job = ["identity_management.utils.after_job"]

# # User Data Protection
# # --------------------

# # user_data_fields = [
# # 	{
# # 		"doctype": "{doctype_1}",
# # 		"filter_by": "{filter_by}",
# # 		"redact_fields": ["{field_1}", "{field_2}"],
# # 		"partial": 1,
# # 	},
# # 	{
# # 		"doctype": "{doctype_2}",
# # 		"filter_by": "{filter_by}",
# # 		"partial": 1,
# # 	},
# # 	{
# # 		"doctype": "{doctype_3}",
# # 		"strict": False,
# # 	},
# # 	{
# # 		"doctype": "{doctype_4}"
# # 	}
# # ]

# # Authentication and authorization
# # --------------------------------

# # auth_hooks = [
# # 	"identity_management.auth.validate"
# # ]

# # Automatically update python controller files with type annotations for this app.
# # export_python_type_annotations = True

# # default_log_clearing_doctypes = {
# # 	"Logging DocType Name": 30  # days to retain logs
# # }

# fixtures = [
#     # 1. التعديلات الهيكلية والحقول المخصصة
#     "Custom Field",
#     "Property Setter",
#     # 2. دورات وسير العمل بالتفصيل (Workflows)
#     "Workflow",
#     "Workflow State",
#     "Workflow Action Master",
#     # 3. خدمات وتصاميم البطائق والتقارير
#     {"dt": "Print Format", "filters": [["module", "in", MODULES]]},
#     {"dt": "Client Script", "filters": [["module", "in", MODULES]]},
#     {"dt": "Server Script", "filters": [["module", "in", MODULES]]},
#     {"dt": "Report", "filters": [["module", "in", MODULES]]},
#     # 4. الأدوار والصلاحيات المخصصة للنظام (Roles & Permissions)
#     {
#         "dt": "Role",
#         "filters": [
#             ["name", "in", ["Card Issuer", "Card Approver", "Identity Manager"]]
#         ],
#     },
#     "Custom DocPerm",
# ]
# doc_events = {
#     "Card Request": {
#         "on_update": "identity_management.id_card_system.services.workflow_tracking.handle_workflow"
#     }
# }
app_name = "identity_management"
app_title = "ID_Card_System"
app_publisher = "Abdulrahman"
app_description = "ID for Staff"
app_email = "al.wahaas2200@gmail.com"
app_license = "mit"

# قائمة الموديولات المعنية لتجميع التصدير الآلي
MODULES = ["ID_Card_System", "ID Card System", "Identity Management"]

# -----------------------------------------------------------
# Fixtures (تصدير التعديلات والتصاميم وتصاريح النظام تلقائياً)
# -----------------------------------------------------------

fixtures = [
    # 1. نقل الـ DocTypes المخصصة لنظام البطائق فقط
    {"dt": "DocType", "filters": [["custom", "=", 1], ["module", "in", MODULES]]},
    # 2. نقل الحقول المخصصة المرتبطة بنظام البطائق والموظفين
    {"dt": "Custom Field", "filters": [["module", "in", MODULES]]},
    {"dt": "Property Setter", "filters": [["module", "in", MODULES]]},
    # 3. دورات وسير العمل (Workflows)
    "Workflow",
    "Workflow State",
    "Workflow Action Master",
    # 4. خدمات وتصاميم البطائق والتقارير والسكريبتات
    {"dt": "Print Format", "filters": [["module", "in", MODULES]]},
    {"dt": "Client Script", "filters": [["module", "in", MODULES]]},
    {"dt": "Server Script", "filters": [["module", "in", MODULES]]},
    {"dt": "Report", "filters": [["module", "in", MODULES]]},
    {
        "dt": "Role",
        "filters": [
            ["name", "in", ["Card Issuer", "Card Approver", "Identity Manager"]]
        ],
    },
    "Custom DocPerm",
]
# -----------------------------------------------------------
# Document Events (أحداث المستندات المحددة فقط)
# -----------------------------------------------------------
doc_events = {
    "Card Request": {
        "on_update": "identity_management.id_card_system.services.workflow_tracking.handle_workflow"
    }
}
