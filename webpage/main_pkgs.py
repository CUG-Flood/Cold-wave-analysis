import yaml
import pymysql
import os
import pandas as pd
import numpy as np
import pymysql
import matplotlib.pyplot as plt

def db_load_config(f = "env/db_userinfo.yml"):
  with open(f, 'r') as fid:
    uInfo = yaml.load(fid, Loader=yaml.FullLoader)
  return uInfo


def db_open(dbinfo=None, which_db=0):
  return pymysql.connect(
      host=dbinfo["host"],
      user=dbinfo["user"],
      port=dbinfo["port"],
      password=dbinfo["pwd"],
      database=dbinfo["dbname"][which_db]
    )


def query_table_columns(cursor, table_name):
  query = f"DESCRIBE {table_name}"
  cursor.execute(query)
  # Fetch the results
  column_names = [row[0] for row in cursor.fetchall()]
  return column_names


def query_data_site(cursor, tbl, site=None):
  """
  - `site`: integer, 站点编号
  - `tbl` : string, 数据库名
  """
  if site is None:
    sql = f"SELECT * FROM {tbl}"
  else:
    sql = "SELECT * FROM %s WHERE (`site` = %d)" % (tbl, site)

  cursor.execute(sql) 
  # 检索查询结果
  data = cursor.fetchall()
  vars = query_table_columns(cursor, tbl) # column names
  df = pd.DataFrame(data, columns=vars)
  return df



def hello():
  print("hello")

#判断寒潮是否发生
def is_cold_wave(df):
    # 计算平均气温的下降幅度
    df['TEMdrop'] = df['TEM'].diff()
    # 判断是否满足寒潮的条件
    df['cold_wave'] = ((df['TEMdrop'] <= -10) & (df['TEM'] <= 4)) | \
                      ((df['TEMdrop'] <= -12) & (df['TEM'] <= 10)) | \
                      ((df['TEMdrop'] <= -14) & (df['TEM'] <= 16)) | \
                      (df['TEMdrop'] <= -16)
    # 返回布尔值列表
    return df['cold_wave'].tolist()

############

#绘制温度变化曲线
def plot_temperature(df):
    # 获取日期，最高气温，最低气温，平均气温和寒潮列表
    date = df.index.tolist()
    max_temp = df['TEM_max'].tolist()
    min_temp = df['TEM_min'].tolist()
    avg_temp = df['TEM'].tolist()
    cold_wave = df['cold_wave'].tolist()
    # 创建图形对象
    fig = plt.figure(figsize=(12, 6))
    # 绘制最高气温和最低气温曲线
    plt.plot(date, max_temp, label='Max Temperature')
    plt.plot(date, min_temp, label='Min Temperature')
    # 绘制平均气温和寒潮的背景
    plt.fill_between(date, avg_temp, color='lightblue', label='平均温度')
    plt.fill_between(date, cold_wave, color='lightcoral', label='寒潮')
    # 有寒潮的天高亮
    for i in range(len(date)):
        if cold_wave[i]:
            plt.axvspan(date[i], date[i+1], color='red', alpha=0.3)
    # 设置图形的标题，坐标轴标签，图例和网格线
    plt.title('温度变化')
    plt.xlabel('日期')
    plt.ylabel('温度 (℃)')
    plt.legend()
    plt.grid()
    # 返回图形对象
    return fig

#####################

#读取数据库数据
def read_data(db, tbl):
    #开启一个游标cursor
    cursor = db.cursor()
    #获取表内所有数据
    sql = f'SELECT * FROM {tbl}'
    cursor.execute(sql)

    #获取查询结果
    data = cursor.fetchall()

    #将结果转化为datafream对象
    df0 = pd.DataFrame(data)
    return df0