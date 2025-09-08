import pandas as pd

# 读取CSV文件
file_path = "/home/jiwei/Desktop/Thesis/EMA & Bayes/EMA/priors_log_ema.csv"   # 改成你的文件路径
df = pd.read_csv(file_path, sep="\t")

# 对每个key只保留第一次出现
first_old_priors = df.groupby("key").first()["old_prior"]

# 打印结果
print(first_old_priors)

# 如果要保存到文件
first_old_priors.to_csv("first_old_prior.csv", header=True)
