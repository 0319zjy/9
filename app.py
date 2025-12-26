import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
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
    """加载Excel数据，处理时间格式"""
    try:
        # 读取Excel文件（需确保文件在同一目录）
        df = pd.read_excel('supermarket_sales.xlsx', sheet_name='销售数据', skiprows=1)
        # 处理日期格式
        df['日期'] = pd.to_datetime(df['日期'], format='%m/%d/%y')
        # 提取小时（从时间字符串如"10:29"转换）
        df['小时'] = pd.to_datetime(df['时间'], format='%H:%M').dt.hour
        return df
    except FileNotFoundError:
        st.warning("未找到Excel文件，使用示例数据")
        # 生成示例数据（模拟真实数据结构）
        data = {
            '订单号': [f'1123-19-{i}' for i in range(1176, 1476)],
            '分店': np.random.choice(['1号店', '2号店', '3号店'], 300),
            '城市': np.random.choice(['太原', '临汾', '大同'], 300),
            '顾客类型': np.random.choice(['会员用户', '普通用户'], 300),
            '性别': np.random.choice(['男性', '女性'], 300),
            '产品类型': np.random.choice(['健康美容', '电子配件', '食品饮料', '时尚配饰', '家居生活', '运动旅行'], 300),
            '单价': np.random.uniform(10, 100, 300).round(2),
            '数量': np.random.randint(1, 10, 300),
            '总价': np.random.uniform(30, 1000, 300).round(2),
            '日期': pd.date_range('2022-01-01', periods=300, freq='D'),
            '时间': [f'{np.random.randint(9, 21)}:{np.random.randint(0, 60):02d}' for _ in range(300)],
            '评分': np.random.uniform(4, 10, 300).round(1)
        }
        df = pd.DataFrame(data)
        df['小时'] = pd.to_datetime(df['时间'], format='%H:%M').dt.hour
        return df

# 加载数据
df = load_data()

# 数据预处理
df['月份'] = df['日期'].dt.month
df['月份名称'] = df['日期'].dt.month_name()
df['星期'] = df['日期'].dt.day_name()

# 侧边栏筛选器
st.sidebar.header("🔍 数据筛选")

# 多维度筛选
cities = st.sidebar.multiselect(
    "选择城市:",
    options=df['城市'].unique(),
    default=df['城市'].unique()
)

stores = st.sidebar.multiselect(
    "选择分店:",
    options=df['分店'].unique(),
    default=df['分店'].unique()
)

product_types = st.sidebar.multiselect(
    "选择产品类型:",
    options=df['产品类型'].unique(),
    default=df['产品类型'].unique()
)

customer_types = st.sidebar.multiselect(
    "选择顾客类型:",
    options=df['顾客类型'].unique(),
    default=df['顾客类型'].unique()
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

# 应用筛选条件
df_filtered = df[
    (df['城市'].isin(cities)) &
    (df['分店'].isin(stores)) &
    (df['产品类型'].isin(product_types)) &
    (df['顾客类型'].isin(customer_types)) &
    (df['日期'] >= pd.to_datetime(start_date)) &
    (df['日期'] <= pd.to_datetime(end_date))
]

# 核心KPI指标展示
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_sales = df_filtered['总价'].sum()
    st.metric("总销售额", f"¥{total_sales:,.2f}")
with col2:
    total_orders = len(df_filtered)
    st.metric("总订单数", f"{total_orders:,}")
with col3:
    avg_rating = df_filtered['评分'].mean()
    st.metric("平均评分", f"{avg_rating:.1f}☆")
with col4:
    avg_transaction = df_filtered['总价'].mean()
    st.metric("平均客单价", f"¥{avg_transaction:.2f}")

# 图表区域（分标签页展示）
tab1, tab2, tab3, tab4, tab5 = st.tabs(["销售概览", "产品分析", "客户分析", "时间分析", "详细数据"])

with tab1:
    """销售概览：分店+产品+趋势"""
    col1, col2 = st.columns(2)
    
    with col1:
        # 各分店销售额对比
        store_sales = df_filtered.groupby('分店')['总价'].sum().reset_index()
        fig1 = px.bar(store_sales, x='分店', y='总价', 
                      title='各分店销售额', color='分店',
                      labels={'总价': '销售额（元）'},
                      template='plotly_white')
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # 产品类型销售额占比
        fig2 = px.pie(df_filtered, names='产品类型', values='总价',
                     title='各产品类型销售额占比',
                     template='plotly_white')
        st.plotly_chart(fig2, use_container_width=True)
    
    # 每日销售额趋势
    daily_sales = df_filtered.groupby('日期')['总价'].sum().reset_index()
    fig3 = px.line(daily_sales, x='日期', y='总价', 
                   title='每日销售额趋势',
                   labels={'总价': '销售额（元）', '日期': '日期'},
                   template='plotly_white')
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    """产品分析：销量+评分+单价"""
    col1, col2 = st.columns(2)
    
    with col1:
        # 各产品销售额与销量对比
        product_stats = df_filtered.groupby('产品类型').agg({
            '总价': 'sum',
            '数量': 'sum'
        }).reset_index()
        fig4 = px.bar(product_stats, x='产品类型', y='总价',
                      title='各产品类型销售额',
                      labels={'总价': '销售额（元）'},
                      template='plotly_white')
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        # 产品评分分布
        fig5 = px.box(df_filtered, x='产品类型', y='评分',
                     title='各产品类型评分分布',
                     labels={'评分': '评分（1-10分）'},
                     template='plotly_white')
        st.plotly_chart(fig5, use_container_width=True)
    
    # 产品单价分布
    fig6 = px.histogram(df_filtered, x='单价', color='产品类型',
                       title='产品单价分布',
                       labels={'单价': '单价（元）'},
                       template='plotly_white',
                       opacity=0.7)
    st.plotly_chart(fig6, use_container_width=True)

with tab3:
    """客户分析：类型+性别+消费习惯"""
    col1, col2 = st.columns(2)
    
    with col1:
        # 顾客类型分析
        customer_analysis = df_filtered.groupby('顾客类型').agg({
            '总价': 'sum',
            '订单号': 'count',
            '评分': 'mean'
        }).reset_index()
        customer_analysis.columns = ['顾客类型', '总销售额', '订单数', '平均评分']
        fig7 = px.bar(customer_analysis, x='顾客类型', y='总销售额',
                     title='不同顾客类型销售额',
                     labels={'总销售额': '销售额（元）'},
                     template='plotly_white')
        st.plotly_chart(fig7, use_container_width=True)
    
    with col2:
        # 性别消费分布
        gender_sales = df_filtered.groupby('性别').agg({
            '总价': 'sum',
            '订单号': 'count'
        }).reset_index()
        fig8 = px.pie(gender_sales, names='性别', values='总价',
                     title='性别销售额分布',
                     template='plotly_white')
        st.plotly_chart(fig8, use_container_width=True)

with tab4:
    """时间分析：月度+小时+星期"""
    col1, col2 = st.columns(2)
    
    with col1:
        # 月度销售趋势
        monthly_sales = df_filtered.groupby('月份名称')['总价'].sum().reset_index()
        month_order = ['January', 'February', 'March']  # 2022年前3个月
        monthly_sales['月份名称'] = pd.Categorical(monthly_sales['月份名称'], 
                                               categories=month_order, 
                                               ordered=True)
        monthly_sales = monthly_sales.sort_values('月份名称')
        fig9 = px.line(monthly_sales, x='月份名称', y='总价',
                      title='月度销售额趋势',
                      labels={'总价': '销售额（元）', '月份名称': '月份'},
                      template='plotly_white')
        st.plotly_chart(fig9, use_container_width=True)
    
    with col2:
        # 小时销售分布
        hourly_sales = df_filtered.groupby('小时')['总价'].sum().reset_index()
        fig10 = px.bar(hourly_sales, x='小时', y='总价',
                      title='小时销售额分布',
                      labels={'总价': '销售额（元）', '小时': '小时（24小时制）'},
                      template='plotly_white')
        st.plotly_chart(fig10, use_container_width=True)
    
    # 星期销售分布
    weekday_sales = df_filtered.groupby('星期')['总价'].sum().reset_index()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                     'Friday', 'Saturday', 'Sunday']
    weekday_sales['星期'] = pd.Categorical(weekday_sales['星期'], 
                                           categories=weekday_order, 
                                           ordered=True)
    weekday_sales = weekday_sales.sort_values('星期')
    fig11 = px.bar(weekday_sales, x='星期', y='总价',
                   title='星期销售额分布',
                   labels={'总价': '销售额（元）', '星期': '星期'},
                   template='plotly_white')
    st.plotly_chart(fig11, use_container_width=True)

with tab5:
    """详细数据表格"""
    st.dataframe(df_filtered[['订单号', '分店', '城市', '顾客类型', '性别', 
                             '产品类型', '单价', '数量', '总价', '日期', '时间', '评分']],
                 use_container_width=True)
    
    # 数据下载功能
    csv = df_filtered.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="下载筛选后数据 (CSV格式)",
        data=csv,
        file_name=f"商场销售数据_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
