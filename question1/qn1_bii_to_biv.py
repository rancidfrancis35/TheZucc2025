import pandas as pd

data_path = "New Microsoft Excel Worksheet.xlsx"
df = pd.read_excel(data_path)


capex = {

"A":3,
"B":6,
"C":2.2,
"D":3,
"E":3.5,
"F":6,
"G":2.1,
"H":1.8,
"I":3,
"J":8

}

##print(capex)


# get total Capex per each row
df_price = df.mul(pd.Series(capex), axis=1)
print(df_price)

# Get total price per quarter
df_total = df_price.sum(axis=1).to_frame(name="Total Price")
print(df_total)

# Get net profit

# Sum of Capex
capex_sum = df_total['Total Price'].sum()
capex_sum = capex_sum/1000 # store as billions
print("expenditure" + str(capex_sum))


tam = (21.8 + 27.4 + 34.9 + 39 + 44.7 + 51.5 + 52.5 + 43.5) * 0.002 * 13
print("revenue =" + str(tam))


profit = tam - capex_sum
print("proft =" + str(profit))


##output##

# Total Price Data:
# 0: 156.9
# 1: 147.9
# 2: 144.1
# 3: 156.4
# 4: 156.9
# 5: 146.1
# 6: 156.9
#
# Expenditure: 1.0652
# Revenue: 8.1978
# Profit: 7.1326


