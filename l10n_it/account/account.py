from osv import fields, osv

class account_account_template(osv.osv):
    _inherit = "account.account.template"
    _columns =  {
        'child_consol_ids': fields.many2many('account.account.template', 'account_account_template_consol_rel', 'child_id', 'parent_id', 'Consolidated Children'),
    }
account_account_template()

class wizard_multi_charts_accounts(osv.osv_memory):
    _inherit = 'wizard.multi.charts.accounts'
    _defaults = {
        'code_digits': lambda *a:0,
    }
    def execute(self, cr, uid, ids, context=None):
        super(wizard_multi_charts_accounts, self).execute(cr, uid, ids, context=None)

        obj_multi = self.browse(cr, uid, ids[0])
        obj_acc = self.pool.get('account.account')
        obj_acc_template = self.pool.get('account.account.template')
        obj_acc_root = obj_multi.chart_template_id.account_root_id
        children_acc_template = obj_acc_template.search(cr, uid, [('parent_id','child_of',[obj_acc_root.id]),('nocreate','!=',True)])
        children_acc_template.sort()
        for account_template in obj_acc_template.browse(cr, uid, children_acc_template):
            if(account_template.child_consol_ids):
                dig = obj_multi.code_digits
                code_main = account_template.code and len(account_template.code) or 0
                code_acc = account_template.code or ''
                if code_main>0 and code_main<=dig and account_template.type != 'view':
                    code_acc=str(code_acc) + (str('0'*(dig-code_main)))
                account_id = obj_acc.search(cr, uid, [('code','=',code_acc)])
                child_consol_ids = []
                for child in account_template.child_consol_ids:
                    child_consol_ids.append(child.id)
                obj_acc.write(cr, uid, account_id, {'child_consol_ids': [(6, 0, child_consol_ids)]})

wizard_multi_charts_accounts()
