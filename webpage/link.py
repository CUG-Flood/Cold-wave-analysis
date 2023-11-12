import streamlit as st
import matplotlib.pyplot as plt
import pymysql
from main_pkgs import *
import pandas as pd
import numpy as np
import seaborn as sns

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

st.markdown('一, *历年数据* :sunglasses:')
#@st.cache(allow_output_mutation=True, hash_funcs={"_thread.RLock": lambda _: None})

#链接数据库
db = pymysql.connect(host='xxx',user='xxx',passwd='xxxxx',port=xxxx,db='xxxx')

#开启一个游标cursor
cursor = db.cursor()

#@st.cache(ttl=600)
#获取China_Mete2000_daily_1951_2019表内所有数据
sql = 'select * from China_Mete2000_daily_1951_2019'
cursor.execute(sql)

#获取查询结果
data = cursor.fetchall()

#将结果转化为datafream对象
df = pd.DataFrame(data)

st.write(cursor.description)
st.write(df)

#获取站点
df_site = list(set(df['site']))


#不同站点历年信息查询
st.markdown('二, *不同站点信息查询* :sunglasses::sunglasses:')
option = st.selectbox('请选择站点',df_site)
'当前选择的站点为：',option
new_df = df['site'][df['site']==option]
