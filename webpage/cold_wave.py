import streamlit as st
import matplotlib.pyplot as plt
import pymysql
from main_pkgs import *
import pandas as pd
import numpy as np
import seaborn as sns
from analysis_pkgs import *

# pyyaml
db = pymysql.connect(host='xxx',user='xxx',passwd='xxx',port=0000,db='xxx')

#创建游标对象
cursor = db.cursor()
table_name = 'China_Mete2000_daily_2020_2022'
#读取
df0 = read_data(db, tbl=table_name)
#网页
st.title('寒潮分析')
#选择站点
option = st.selectbox('请选择要查询的站点：', list(set(df0[1])))
'当前查询站点：', option

#查询数据并转化为DataFrame对象
df = query_data_site(cursor=cursor, tbl=table_name, site=option)
#显示数据表格
st.write(df)

#判断是否有寒潮
df['cold_wave'] = is_cold_wave(df)

#绘图
plt.rcParams['font.sans-serif']=['SimHei']
fig = plot_temperature(df)

#显示图像
st.plotly_chart(fig)
