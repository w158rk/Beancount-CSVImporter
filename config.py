#!/usr/bin/env python3
import sys
import os

path = os.path.abspath(os.path.dirname(__file__))
sys.path.append(f"{path}/importers")
from CSVImporter import Col, Importer, Drcr

currency = "CNY"

drcr_dict = {"支出": Drcr.DEBIT, "收入": Drcr.CREDIT, "已支出": Drcr.DEBIT, "已收入": Drcr.CREDIT, "其他": Drcr.CREDIT, "不计收支": Drcr.DEBIT}
refund_keyword = "退款"

iconfig_wechat = {
    Col.DATE: "交易时间",
    Col.PAYEE: "交易对方",
    Col.NARRATION: "商品",
    Col.ACCOUNT: "支付方式",
    Col.AMOUNT: "金额(元)",
    Col.DRCR: "收/支",
    Col.STATUS: "当前状态",
    Col.TXN_TIME: "交易时间",
    Col.TXN_DATE: "交易时间",
    Col.TYPE: "交易类型",
}

iconfig_alipay = {
    Col.DATE: "交易时间",
    Col.PAYEE: "交易对方",
    Col.NARRATION: "商品说明",
    Col.ACCOUNT: "收/付款方式",
    Col.AMOUNT: "金额",
    Col.DRCR: "收/支",
    Col.STATUS: "交易状态",
    Col.TXN_TIME: "交易时间",
    Col.TXN_DATE: "交易时间",
    Col.TYPE: "交易分类",
}

iconfig_hisdetail = {
    Col.DATE: "交易日期",
    Col.PAYEE: "对方户名",
    Col.NARRATION: "摘要",
    Col.ACCOUNT: "交易场所",
    Col.AMOUNT_CREDIT: "记账金额(收入)",
    Col.AMOUNT_DEBIT: "记账金额(支出)",
    Col.TXN_TIME: "交易日期",
    Col.TXN_DATE: "交易日期",
}

iconfig_hqmx = {
    Col.DATE: "交易日期",
    Col.PAYEE: "对方账号与户名",
    Col.NARRATION: "交易地点/附言",
    Col.ACCOUNT: "钞汇",
    Col.AMOUNT: "交易金额",
    Col.TXN_TIME: "交易日期",
    Col.TXN_DATE: "交易日期",
    Col.DRCR: "摘要",
}

account_map = {
    "assets": {
        "DEFAULT": "Unknown",
        "0000|春田花花银行": "Liabilities:CreditCard:SFFB:0000",
        "余额宝": "Assets:Alipay:YuEBao",
        "零钱": "Assets:Wechat:MiniFund",
    },
    "debit": {
        "DEFAULT": "Expenses:Unknown",
        "自动宝|全家|友礼汇|茶叶": "Expenses:Food:Snacks",
        "天猫超市|牙刷|茶杯|海狸先生": "Expenses:DailyNecessities",
        "近视眼镜": "Expenses:Clothing:Glasses",
        "饿了么": "Expenses:Food:Delivery",
        "医院": "Expenses:Health:Hospital",
        "中国邮政": "Expenses:ExpressPostage",
        "耳机": "Expenses:DigitalEquipment:Audio",
        "显示器": "Expenses:DigitalEquipment:Display",
        "火车票": "Expenses:Transport:Railway",
        "打车": "Expenses:Transport:Taxi",
        "台灯": "Expenses:Appliances",
        "手机": "Expenses:DigitalEquipment:MobilePhone",
        "Naturehike": "Expenses:Clothing:Outdoor",
    },
    "credit": {
        "DEFAULT": "Income:Unknown",
        "余额宝": "Income:MoneyFund:Alipay:YuEBao",
        "转账": "Income:TransferIn",
        "退款": "Income:Unknown",  # need manual confirmation
    },
}

wechat_importer = Importer(
    iconfig_wechat,
    "",
    currency,
    "微信支付账单",
    16,
    drcr_dict,
    refund_keyword,
    account_map,
)

alipay_importer = Importer(
    iconfig_alipay,
    "",
    currency,
    "alipay_record",
    24,
    drcr_dict,
    refund_keyword,
    account_map,
)

hisdetail_importer = Importer(
    iconfig_hisdetail,
    "",
    currency,
    "hisdetail",
    6,
    drcr_dict,
    refund_keyword,
    account_map=account_map,
    allow_zero_amounts = True,
)

hqmx_importer = Importer(
    iconfig_hqmx,
    "",
    currency,
    "hqmx",
    2,
    {
        "利息存入": Drcr.CREDIT,
        "跨行转出": Drcr.DEBIT,
        "电子汇入": Drcr.CREDIT,
        "消费": Drcr.DEBIT,
    },
    refund_keyword,
    account_map=account_map,
    allow_zero_amounts = True,
)

CONFIG = [wechat_importer, alipay_importer, hisdetail_importer, hqmx_importer]
