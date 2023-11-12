import numpy as np
import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly

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
    max_temp = df['TEM_Max'].tolist()
    min_temp = df['TEM_Min'].tolist()
    avg_temp = df['TEM'].tolist()
    cold_wave = df['cold_wave'].tolist()
    # 创建图形对象
    fig = plt.figure(figsize=(12, 6))
    # 绘制最高气温和最低气温曲线
    plt.plot(date, max_temp, label='最高温度')
    plt.plot(date, min_temp, label='最低温度')
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
    sql = f'SELECT * FROM {tbl} LIMIT 1000'
    cursor.execute(sql)

    #获取查询结果
    data = cursor.fetchall()

    #将结果转化为datafream对象
    df0 = pd.DataFrame(data)
    return df0

########################
#交互式图像
def plot_temperature(df):
    # 获取日期，最高气温，最低气温，平均气温和寒潮的列表
    date = df['date'].tolist()
    max_temp = df['TEM_Max'].tolist()
    min_temp = df['TEM_Min'].tolist()
    avg_temp = df['TEM'].tolist()
    cold_wave = df['cold_wave'].tolist()
    # 创建一个子图对象
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("温度变化曲线", "寒潮发生时间"))
    # 创建温度变化曲线的图形对象
    trace1 = go.Scatter(x=date, y=max_temp, name='最高温度', line=dict(color='red', width=2))
    trace2 = go.Scatter(x=date, y=min_temp, name='最低温度', line=dict(color='blue', width=2))
    trace3 = go.Scatter(x=date, y=avg_temp, name='平均气温', line=dict(color='green', width=2))
    # 创建寒潮的分布的图形对象
    trace4 = go.Bar(x=date, y=cold_wave, name='寒潮分布时间', marker=dict(color='lightcoral', opacity=0.5))
    # 将图形对象添加到子图对象中
    fig.add_trace(trace1, row=1, col=1)
    fig.add_trace(trace2, row=1, col=1)
    fig.add_trace(trace3, row=1, col=1)
    fig.add_trace(trace4, row=2, col=1)
    # 更新子图对象的布局
    fig.update_layout(title='寒潮', xaxis_title='Date', yaxis_title='Temperature (℃)', legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1), showlegend=True, grid=dict(rows=2, columns=1, pattern='independent'))
    # 返回子图对象
    return fig


