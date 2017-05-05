import pandas
path = "E:/Manhole/training data/original data/4-12/2/2017-04-12_16-39-49/2017-04-12_16-39-49.csv"

data = pandas.read_csv(path)
print(data)
stm32_data = list(data.iloc[:,3])
print(stm32_data)
