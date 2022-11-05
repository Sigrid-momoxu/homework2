"""
DFP HW2 TEAM20
TEAM MEMBER: Xu Longyang, Xu Purui
TIME: 05/11/2022
"""
import pandas as pd

df = pd.read_table('cme.20210709.c.pa2')
df['type'] = df.apply(lambda row:row[0][0],axis=1)
# print(df.groupby('lenth').head(1))
groups = df.groupby(df.type)
df_B = groups.get_group('B')
df_eight = groups.get_group('8')
df['type2'] = df_eight.apply(lambda row:row[0][1],axis=1)
groups = df.groupby(df.type2)
df_eight_one = groups.get_group('1')

header1 = '''Futures   Contract   Contract   Futures     Options   Options
Code      Month      Type       Exp Date    Code      Exp Date
-------   --------   --------   --------    -------   --------
'''
header2 = '''Futures   Contract   Contract   Strike   Settlement
Code      Month      Type       Price    Price
-------   --------   --------   ------   ----------
'''
fout = open('CL_expirations_and_settlements.txt','w')
fout.write(header1)

print("Futures    Contract   Contract   Futures    Options    Options")
print("Code       Month      Type       Exp Date    Code       Exp Date")
print("-------    -------    -------    -------    -------    -------")
for id,data in df_B.iterrows():
    rec = data[0]
    rec_list = str(rec).split()
    future_code = rec_list[1][3:]
    options_code = rec_list[1][3:]
    contract_type = rec_list[2][:3]
    contract_month = rec_list[2][3:10]
    fut_exp_date = rec_list[3][-10:-2]
    options_exp_date = rec_list[4][-10:-2]
    if future_code == 'CL' and int(contract_month)>=202109 and int(contract_month)<=202312:
        contract_month = contract_month[:4] + '-' + contract_month[4:]
        contract_type = contract_type[0]+contract_type[1:].lower()
        fut_exp_date = fut_exp_date[:4] +'-' +fut_exp_date[4:6] + '-'+fut_exp_date[6:]
        print("{}         {}    {}        {}".format(future_code,contract_month,contract_type,fut_exp_date))
        fout.write("{}         {}    {}        {}\n".format(future_code,contract_month,contract_type,fut_exp_date))
    if options_code == 'LO' and int(contract_month)>=202109 and int(contract_month)<=202312:
        contract_month = contract_month[:4] + '-' + contract_month[4:]
        contract_type = 'Opt'
        options_exp_date = options_exp_date[:4] +'-' +options_exp_date[4:6] + '-'+options_exp_date[6:]
        print("{}         {}    {}                   {}        {}".format('CL', contract_month, contract_type, options_code, options_exp_date))
        fout.write("{}         {}    {}                   {}        {}\n".format('CL', contract_month, contract_type, options_code, options_exp_date))

print("Futures    Contract   Contract   Strike     Settlement")
print("Code       Month      Type       Price       Price")
print("-------    -------    -------    -------    -------")
fout.write(header2)
for id, data in df_eight_one.iterrows():
    rec = data[0]
    rec_list = str(rec).split()
    future_code = rec_list[1]
    contract_type = rec_list[2]
    product_type = rec_list[2][:3]
    contract_month = rec_list[3]
    if future_code == 'CL':
        if contract_type == 'FUT'and int(contract_month) >= 202109 and int(contract_month) <= 202312:
            contract_month = contract_month[:4] + '-' + contract_month[4:]
            contract_type = contract_type[0] + contract_type[1:].lower()
            price_str = rec_list[4].split('+')[-1][:-1]
            settlement_price = int(price_str)/100
            print("{}         {}    {}                   {}".format(future_code, contract_month,
                                                                    contract_type, settlement_price))
            fout.write("{}         {}    {}                   {}\n".format(future_code, contract_month,
                                                                    contract_type, settlement_price))
        if product_type == 'OOF':
            contract_month2 = rec_list[2][4:]
            if contract_month == contract_month2 and int(contract_month2) >= 202109 and int(contract_month2) <= 202312:
                if contract_type[3] == 'C':
                    contract_type = 'Call'
                elif contract_type[3] == 'P':
                    contract_type = 'Put '
                contract_month2 = contract_month2[:4] + '-' + contract_month2[4:]
                strike_price = int(rec_list[4][:7])/100
                settlement_price = int(rec_list[4][-14:-1])/100
                print("{}         {}    {}       {:.2f}        {}".format(future_code, contract_month2,
                                                                          contract_type,strike_price,settlement_price))
                fout.write("{}         {}    {}       {:.2f}        {}\n".format(future_code, contract_month2,
                                                                        contract_type,strike_price,settlement_price))
fout.close()

