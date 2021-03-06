# -*- coding: utf-8 -*-
from openerp.tests.common import TransactionCase
from openerp.exceptions import except_orm


class test_trial_balance(TransactionCase):

    def setUp(self):
        super(test_trial_balance, self).setUp()
        self.period_last_year = self.env.ref('finance.period_201512')
        self.period_first_year = self.env.ref('finance.period_201601')
        self.period_201511 = self.env.ref('finance.period_201511')
        self.period_last = self.env.ref('finance.period_201603')
        self.period_now = self.env.ref('finance.period_201604')

        subject_name_id_1 = self.env.ref('finance.finance_account_1')
        subject_name_id_4 = self.env.ref('finance.finance_account_4')
        subject_name_id_11 = self.env.ref('finance.finance_account_11')
        self.trial_balance_wizard_now = self.env['create.trial.balance.wizard'].create({'period_id': self.period_now.id})
        self.trial_balance_wizard_last = self.env['create.trial.balance.wizard'].create({'period_id': self.period_last.id})
        # self.trial_balance_wizard_period_first_year = self.env['create.trial.balance.wizard'].create({'period_id': self.period_first_year.id})
        self.trial_balance_wizard_period_last_year = self.env['create.trial.balance.wizard'].create({'period_id': self.period_last_year.id})
        self.period_201511_wizard = self.env['create.trial.balance.wizard'].create({'period_id': self.period_201511.id})

        self.period_2016__01_03 = self.env['create.vouchers.summary.wizard'].create({'period_begin_id': self.period_last.id,
                                                                                     'period_end_id': self.period_last.id, 'subject_name_id': subject_name_id_1.id})
        self.period_2016_01_04 = self.env['create.vouchers.summary.wizard'].create({'period_begin_id': self.period_first_year.id,
                                                                                    'period_end_id': self.period_now.id, 'subject_name_id': subject_name_id_1.id})
        self.period_2016_01_03_04 = self.env['create.vouchers.summary.wizard'].create({'period_begin_id': self.period_last.id,
                                                                                       'period_end_id': self.period_now.id, 'subject_name_id': subject_name_id_1.id})
        self.period_2016_01_04_04 = self.env['create.vouchers.summary.wizard'].create({'period_begin_id': self.period_last.id,
                                                                                       'period_end_id': self.period_now.id, 'subject_name_id': subject_name_id_1.id})
        self.period_2016_04_04 = self.env['create.vouchers.summary.wizard'].create({'period_begin_id': self.period_now.id,
                                                                                    'period_end_id': self.period_now.id, 'subject_name_id': subject_name_id_4.id})

        self.period_2016_11_03 = self.env['create.vouchers.summary.wizard'].create({'period_begin_id': self.period_last.id,
                                                                                    'period_end_id': self.period_now.id, 'subject_name_id': subject_name_id_4.id})

    def test_creare_trial_balance(self):
        '''创建科目余额表'''

        self.env['create.trial.balance.wizard'].compute_last_period_id(self.period_first_year)
        self.env['create.trial.balance.wizard'].compute_next_period_id(self.period_last_year)
        self.env['create.trial.balance.wizard'].compute_last_period_id(self.period_last)
        self.env['create.trial.balance.wizard'].compute_next_period_id(self.period_last)
        with self.assertRaises(except_orm):
            self.period_201511_wizard.create_trial_balance()
        self.trial_balance_wizard_last.create_trial_balance()
        self.period_last.is_closed = True
        self.trial_balance_wizard_now.create_trial_balance()

        with self.assertRaises(except_orm):
            self.trial_balance_wizard_period_last_year.create_trial_balance()

    def test_create_vouchers_summary(self):
        """测试创建明细帐"""
        self.period_2016__01_03.create_vouchers_summary()
        self.period_last.is_closed = True

        self.period_2016_01_03_04.create_vouchers_summary()
        self.period_2016_04_04.create_vouchers_summary()
        with self.assertRaises(except_orm):
            self.period_2016_01_04.create_vouchers_summary()

        self.period_2016__01_03.period_end_id = self.period_201511.id
        self.period_2016__01_03.onchange_period()
        self.period_2016__01_03.period_begin_id = self.period_201511.id
        with self.assertRaises(except_orm):
            self.period_2016__01_03.create_vouchers_summary()
        self.period_last.is_closed = False
        self.period_2016_11_03.create_vouchers_summary()
        #   22 24
