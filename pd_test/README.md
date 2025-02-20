以下是一个适合新手的 Pandas 入门教程，涵盖基础操作和常用功能：

---

### **1. 安装 Pandas**
```bash
pip install pandas
```

---

### **2. 导入 Pandas**
```python
import pandas as pd
```

---

### **3. 核心数据结构**
#### **3.1 Series（一维数据）**
类似一维数组，带索引：
```python
s = pd.Series([1, 3, 5, 7], name="MySeries")
print(s)
```

#### **3.2 DataFrame（二维数据）**
类似 Excel 表格或 SQL 表：
```python
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Paris", "Tokyo"]
}
df = pd.DataFrame(data)
print(df)
```

---

### **4. 基础操作**
#### **4.1 读取数据**
```python
# 读取 CSV 文件
df = pd.read_csv("data.csv")

# 读取 Excel 文件
df = pd.read_excel("data.xlsx")
```

#### **4.2 查看数据**
```python
df.head()     # 查看前5行
df.tail(3)    # 查看后3行
df.info()     # 查看数据信息（列名、类型、非空值等）
df.describe() # 统计摘要（均值、标准差等）
```

#### **4.3 选择数据**
```python
# 选择单列
df["Name"]

# 选择多列
df[["Name", "Age"]]

# 按行选择（第0行到第2行）
df.iloc[0:3]

# 按条件筛选（年龄大于25）
df[df["Age"] > 25]
```

---

### **5. 数据清洗**
#### **5.1 处理缺失值**
```python
# 检查缺失值
df.isnull()

# 删除包含缺失值的行
df.dropna()

# 填充缺失值（用0填充）
df.fillna(0)
```

#### **5.2 删除重复值**
```python
df.drop_duplicates()
```

#### **5.3 修改列名**
```python
df.columns = ["name", "age", "city"]
```

---

### **6. 数据操作**
#### **6.1 排序**
```python
# 按年龄升序排序
df.sort_values("Age")

# 按年龄降序排序
df.sort_values("Age", ascending=False)
```

#### **6.2 分组统计**
```python
# 按城市分组，计算平均年龄
df.groupby("City")["Age"].mean()
```

#### **6.3 合并数据**
```python
# 合并两个 DataFrame（类似 SQL JOIN）
pd.merge(df1, df2, on="key_column")
```

---

### **7. 实战案例：处理销售数据**
假设有一个 `sales.csv` 文件：
```csv
Date,Product,Price,Quantity
2023-01-01,A,100,5
2023-01-02,B,200,3
2023-01-03,A,100,2
```

```python
# 读取数据
df = pd.read_csv("sales.csv")

# 计算总销售额
df["Total"] = df["Price"] * df["Quantity"]

# 按产品统计总销售额
product_sales = df.groupby("Product")["Total"].sum()
print(product_sales)
```

---

### **8. 学习资源**
- **官方文档**: [Pandas Documentation](https://pandas.pydata.org/docs/)
- **书籍推荐**: 《利用Python进行数据分析》（含Pandas详细教程）
- **练习平台**: Kaggle、LeetCode

---

### **9. 总结**
Pandas 核心功能：
1. **数据读取/写入**：支持 CSV、Excel、SQL 等格式。
2. **数据清洗**：处理缺失值、重复值、异常值。
3. **数据操作**：筛选、排序、分组、合并。
4. **数据分析**：统计、聚合、可视化（配合 Matplotlib/Seaborn）。

逐步练习，从简单操作到复杂分析，你会快速掌握 Pandas！

### **10. 数据可视化**
#### **10.1 基本绘图**
```python
import matplotlib.pyplot as plt

# 绘制柱状图
df["Age"].value_counts().plot(kind='bar')
plt.title("年龄分布")
plt.xlabel("年龄")
plt.ylabel("人数")
plt.show()

# 绘制折线图
df.groupby("City")["Age"].mean().plot(kind='line')
plt.title("各城市平均年龄")
plt.xlabel("城市")
plt.ylabel("平均年龄")
plt.show()
```