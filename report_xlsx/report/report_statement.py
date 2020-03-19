from odoo.http import request
from odoo import models, api
import logging
import time
from odoo import fields

_logger = logging.getLogger(__name__)

ROW_LIST = {
    'row_1': 'A1:Q1',
    'row_2': 'A2:Q2',
    'row_3_col_1': 'A3:H3',
    'row_3_col_2': 'I3:Q3',
    'row_4_col_1': 'A4:B4',
    'row_4_col_2': 'C4:G4',
    'row_4_col_3': 'H4:J4',
    'row_4_col_4': 'K4:Q4',
    'col_1': 'A5:C5',
    'col_2': 3,
    'col_3': 'E5:G5',
    'col_4': 'H5:K5',
    'col_5': 11,
    'col_6': 'M5:O5',
    'col_7': 15,
    'col_8': 16,
}

MERGE_FORMAT = {
    'bold': True,
    'border': 1,
    'align': 'center',
    'valign': 'center'
}

DATE_MERGE_FORMAT = {
    'bold': True,
    'border': 1,
    'align': 'center',
    'valign': 'center',
    'num_format': 'yyyy-mm-dd'
}


class ReportStatement(models.AbstractModel):
    _name = 'report.report_xlsx.standard_statement_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, orde_ids):
        records = self.env['sale.order'].browse(data.get('record', []))

        # initial sheet
        sheet = workbook.add_worksheet('statement01')

        # 格式化
        merge_format = workbook.add_format(MERGE_FORMAT)
        date_merge_format = workbook.add_format(DATE_MERGE_FORMAT)

        border = workbook.add_format({
            'border': 1
        })

        sheet = self._format_sheet_head(sheet, merge_format, date_merge_format)
        # for obj in records:
        #     report_name = obj.name
        #     # One sheet by order
        #     sheet = workbook.add_worksheet(report_name[:31])
        #     bold = workbook.add_format({'bold': True})
        #     sheet.write(0, 0, obj.name, bold)

    def _format_sheet_head(self, sheet, merge_format, date_merge_format):
        sheet.merge_range(ROW_LIST.get('row_1'), u'生产费用报销单', merge_format)
        sheet.merge_range(ROW_LIST.get('row_2'), u'报销单位：重庆中集-重庆中集汽车物流有限责任公司', merge_format)
        sheet.merge_range(ROW_LIST.get('row_3_col_1'), fields.Datetime.now(), date_merge_format)
        sheet.merge_range(ROW_LIST.get('row_3_col_2'), u'报销单号： ' + str(time.time()), merge_format)
        sheet.merge_range(ROW_LIST.get('row_4_col_1'), u'销售体系', merge_format)
        sheet.merge_range(ROW_LIST.get('row_4_col_2'), u'长安福特', merge_format)
        sheet.merge_range(ROW_LIST.get('row_4_col_3'), u'运输方式', merge_format)
        sheet.merge_range(ROW_LIST.get('row_4_col_4'), u'联运第二段GL', merge_format)

        # 交接单			数量	起始地-目的地			车型				单价	金额			扣款	过海费

        sheet.merge_range(ROW_LIST.get('col_1'), u'交接单', merge_format)
        sheet.write(4, ROW_LIST.get('col_2'), u'数量', merge_format)
        sheet.merge_range(ROW_LIST.get('col_3'), u'起始地-目的地', merge_format)
        sheet.merge_range(ROW_LIST.get('col_4'), u'车型', merge_format)
        sheet.write(4, ROW_LIST.get('col_5'), u'单价', merge_format)
        sheet.merge_range(ROW_LIST.get('col_6'), u'金额', merge_format)
        sheet.write(4, ROW_LIST.get('col_7'), u'扣款', merge_format)
        sheet.write(4, ROW_LIST.get('col_8'), u'过海费', merge_format)
        return sheet
