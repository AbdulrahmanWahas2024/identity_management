frappe.query_reports["تقرير طلبات إصدار البطاقات"] = {
    onload: function (report) {
        setTimeout(() => {
            const style = document.createElement("style");

            style.innerHTML = `
                /* منطقة الفلاتر */
                .query-report .report-filters {
                    width: 100% !important;
                }

                /* حقول الفلاتر */
                .query-report .report-filter {
                    min-width: 180px;
                }

                /* قائمة الفرع */
                .query-report .awesomplete > ul {
                    max-height: 100px !important;
                    overflow-y: auto !important;
                    overflow-x: hidden !important;
                    z-index: 9999 !important;
                }

                /* منع القائمة من توسيع الصفحة */
                .query-report .awesomplete {
                    position: relative;
                }
            `;

            document.head.appendChild(style);
        }, 500);
    }
};