import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 页面设置
st.set_page_config(
    page_title="商场销售数据仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 页面设置
st.set_page_config(
    page_title="商场销售数据仪表板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS样式
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown('<div class="main-header">🏪 商场销售数据仪表板</div>', unsafe_allow_html=True)

# 数据加载函数
@st.cache_data
def load_data():
    # 这里使用示例数据，实际应该从Excel文件读取
    # 由于数据量很大，这里创建一个示例数据结构
    data = {
        '订单号': ['1123-19-1176', '1226-31-3081', '1692-92-5582'] * 100,
        '分店': ['1号店', '3号店', '2号店'] * 100,
        '城市': ['太原', '临汾', '大同'] * 100,
        '顾客类型': ['会员用户', '普通用户', '会员用户'] * 100,
        '性别': ['男性', '女性', '女性'] * 100,
        '产品类型': ['健康美容', '电子配件', '食品饮料'] * 100,
        '单价': [58.22, 15.28, 54.84] * 100,
        '数量': [8, 5, 3] * 100,
        '总价': [465.76, 76.4, 164.52] * 100,
        '日期': pd.date_range('2022-01-01', periods=300, freq='D'),
        '时间': [0.85625, 0.43681, 0.56042] * 100,
        '评分': [8.4, 9.6, 5.9] * 100
    }
    df = pd.DataFrame(data)
    return df

# 加载数据
try:
    # 尝试从Excel文件读取
    df = pd.read_excel('supermarket_sales.xlsx')
except:
    # 如果文件不存在，使用示例数据
    df = load_data()

# 数据预处理
df['月份'] = df['日期'].dt.month
df['月份名称'] = df['日期'].dt.month_name()
df['星期'] = df['日期'].dt.day_name()

# 侧边栏筛选器
st.sidebar.header("🔍 数据筛选")

# 分店筛选
stores = st.sidebar.multiselect(
    "选择分店:",
    options=df['分店'].unique(),
    default=df['分店'].unique()
)

# 产品类型筛选
product_types = st.sidebar.multiselect(
    "选择产品类型:",
    options=df['产品类型'].unique(),
    default=df['产品类型'].unique()
)

# 日期范围筛选
min_date = df['日期'].min()
max_date = df['日期'].max()
start_date, end_date = st.sidebar.date_input(
    "选择日期范围:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# 应用筛选
df_filtered = df[
    (df['分店'].isin(stores)) &
    (df['产品类型'].isin(product_types)) &
    (df['日期'] >= pd.to_datetime(start_date)) &
    (df['日期'] <= pd.to_datetime(end_date))
]

# 主仪表板
# KPI指标行
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = df_filtered['总价'].sum()
    st.metric("总销售额", f"¥{total_sales:,.2f}")

with col2:
    total_orders = len(df_filtered)
    st.metric("总订单数", f"{total_orders:,}")

with col3:
    avg_rating = df_filtered['评分'].mean()
    st.metric("平均评分", f"{avg_rating:.1f}")

with col4:
    avg_transaction = df_filtered['总价'].mean()
    st.metric("平均客单价", f"¥{avg_transaction:.2f}")

# 图表区域
tab1, tab2, tab3, tab4 = st.tabs(["销售概览", "产品分析", "客户分析", "时间分析"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # 各分店销售额
        st.subheader("各分店销售额")
        store_sales = df_filtered.groupby('分店')['总价'].sum()
        fig, ax = plt.subplots(figsize=(8, 4))
        bars = ax.bar(store_sales.index, store_sales.values)
        ax.set_xlabel('分店')
        ax.set_ylabel('销售额')
        ax.set_title('各分店销售额对比')
        
        # 添加数值标签
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'¥{height:,.0f}', ha='center', va='bottom')
        
        plt.xticks(rotation=45)
        plt.tight_layout
""", unsafe_allow_html=True)

# 标题
st.markdown('<div class="main-header">🏪 商场销售数据仪表板</div>', unsafe_allow_html=True)

# 数据加载函数
@st.cache_data
def load_data():
    # 这里使用示例数据，实际应该从Excel文件读取
    # 由于数据量很大，这里创建一个示例数据结构
    data = {
        '订单号': ['1123-19-1176', '1226-31-3081', '1692-92-5582'] * 100,
        '分店': ['1号店', '3号店', '2号店'] * 100,
        '城市': ['太原', '临汾', '大同'] * 100,
        '顾客类型': ['会员用户', '普通用户', '会员用户'] * 100,
        '性别': ['男性', '女性', '女性'] * 100,
        '产品类型': ['健康美容', '电子配件', '食品饮料'] * 100,
        '单价': [58.22, 15.28, 54.84] * 100,
        '数量': [8, 5, 3] * 100,
        '总价': [465.76, 76.4, 164.52] * 100,
        '日期': pd.date_range('2022-01-01', periods=300, freq='D'),
        '时间': [0.85625, 0.43681, 0.56042] * 100,
        '评分': [8.4, 9.6, 5.9] * 100
    }
    df = pd.DataFrame(data)
    return df

# 加载数据
try:
    # 尝试从Excel文件读取
    df = pd.read_excel('supermarket_sales.xlsx')
except:
    # 如果文件不存在，使用示例数据
    df = load_data()

# 数据预处理
df['月份'] = df['日期'].dt.month
df['月份名称'] = df['日期'].dt.month_name()
df['星期'] = df['日期'].dt.day_name()

# 侧边栏筛选器
st.sidebar.header("🔍 数据筛选")

# 分店筛选
stores = st.sidebar.multiselect(
    "选择分店:",
    options=df['分店'].unique(),
    default=df['分店'].unique()
)

# 产品类型筛选
product_types = st.sidebar.multiselect(
    "选择产品类型:",
    options=df['产品类型'].unique(),
    default=df['产品类型'].unique()
)

# 日期范围筛选
min_date = df['日期'].min()
max_date = df['日期'].max()
start_date, end_date = st.sidebar.date_input(
    "选择日期范围:",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

# 应用筛选
df_filtered = df[
    (df['分店'].isin(stores)) &
    (df['产品类型'].isin(product_types)) &
    (df['日期'] >= pd.to_datetime(start_date)) &
    (df['日期'] <= pd.to_datetime(end_date))
]

# 主仪表板
# KPI指标行
col1, col2, col3, col4 = st.columns(4)

with col1:
    total_sales = df_filtered['总价'].sum()
    st.metric("总销售额", f"¥{total_sales:,.2f}")

with col2:
    total_orders = len(df_filtered)
    st.metric("总订单数", f"{total_orders:,}")

with col3:
    avg_rating = df_filtered['评分'].mean()
    st.metric("平均评分", f"{avg_rating:.1f}")

with col4:
    avg_transaction = df_filtered['总价'].mean()
    st.metric("平均客单价", f"¥{avg_transaction:.2f}")

# 图表区域
tab1, tab2, tab3, tab4 = st.tabs(["销售概览", "产品分析", "客户分析", "时间分析"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # 各分店销售额
        store_sales = df_filtered.groupby('分店')['总价'].sum().reset_index()
        fig1 = px.bar(store_sales, x='分店', y='总价', 
                      title='各分店销售额', color='分店')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 销售额分布
        fig2 = px.pie(df_filtered, names='产品类型', values='总价',
                     title='各产品类型销售额占比')
        st.plotly_chart(fig2, use_container_width=True)
    
    # 时间趋势图
    daily_sales = df_filtered.groupby('日期')['总价'].sum().reset_index()
    fig3 = px.line(daily_sales, x='日期', y='总价', 
                   title='每日销售额趋势')
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        # 各产品类型销售情况
        product_stats = df_filtered.groupby('产品类型').agg({
            '总价': 'sum',
            '数量': 'sum',
            '评分': 'mean'
        }).reset_index()
        fig4 = px.bar(product_stats, x='产品类型', y='总价',
                      title='各产品类型销售额')
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        # 产品评分分布
        fig5 = px.box(df_filtered, x='产品类型', y='评分',
                     title='各产品类型评分分布')
        st.plotly_chart(fig5, use_container_width=True)

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # 顾客类型分析
        customer_analysis = df_filtered.groupby('顾客类型').agg({
            '总价': 'sum',
            '订单号': 'count',
            '评分': 'mean'
        }).reset_index()
        customer_analysis.columns = ['顾客类型', '总销售额', '订单数', '平均评分']
        
        fig6 = px.bar(customer_analysis, x='顾客类型', y='总销售额',
                     title='不同顾客类型销售额')
        st.plotly_chart(fig6, use_container_width=True)
    
    with col2:
        # 性别分布
        gender_sales = df_filtered.groupby('性别')['总价'].sum().reset_index()
        fig7 = px.pie(gender_sales, names='性别', values='总价',
                     title='性别销售额分布')
        st.plotly_chart(fig7, use_container_width=True)

with tab4:
    col1, col2 = st.columns(2)
    
    with col1:
        # 月度趋势
        monthly_sales = df_filtered.groupby('月份名称')['总价'].sum().reset_index()
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        monthly_sales['月份名称'] = pd.Categorical(monthly_sales['月份名称'], 
                                               categories=month_order, 
                                               ordered=True)
        monthly_sales = monthly_sales.sort_values('月份名称')
        
        fig8 = px.line(monthly_sales, x='月份名称', y='总价',
                      title='月度销售额趋势')
        st.plotly_chart(fig8, use_container_width=True)
    
    with col2:
        # 星期销售分布
        weekday_sales = df_filtered.groupby('星期')['总价'].sum().reset_index()
        weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                         'Friday', 'Saturday', 'Sunday']
        weekday_sales['星期'] = pd.Categorical(weekday_sales['星期'], 
                                           categories=weekday_order, 
                                           ordered=True)
        weekday_sales = weekday_sales.sort_values('星期')
        
        fig9 = px.bar(weekday_sales, x='星期', y='总价',
                     title='星期销售额分布')
        st.plotly_chart(fig9, use_container_width=True)

# 数据表格
st.header("📋 详细数据")
st.dataframe(df_filtered, use_container_width=True)

# 数据下载
csv = df_filtered.to_csv(index=False)
st.download_button(
    label="下载筛选后数据 (CSV)",
    data=csv,
    file_name="filtered_sales_data.csv",
    mime="text/csv"
)
