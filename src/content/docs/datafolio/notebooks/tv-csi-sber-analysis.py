#!/usr/bin/env python
# coding: utf-8

# # Анализ данных по телевизорам Sber CSI октябрь - январь 2025

# In[4]:


import pandas as pd
import duckdb
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from IPython.display import display, HTML



# In[5]:


type = "white"
pallete = [
    "#0068f0",
    "#fe0462",
    "#08bb6b",
    "#ff7901",
    "#9ef354",
    "#faee02",
    "#72f0d8",
    "#2c404a",
]
font = "SB Sans Display"
pio.templates["sd_theme"] = go.layout.Template(
    layout=dict(
        font_family=font,
        colorway=pallete,
        # minreducedwidth=250,
        # minreducedheight=250,
        width=800,
        height=400,
    )
)
pio.templates.default = f"plotly_{type}+sd_theme"

pio.renderers.default = 'notebook'


# In[6]:


try:
    # Close any existing connection
    conn.close()
except:
    pass

# Create a new connection
conn = duckdb.connect('data/tv_eda.duckdb')

# Load data from DuckDB to df
df = conn.execute("SELECT * FROM tv_data").fetchdf()
print(f"Loaded {len(df)} rows from DuckDB")

# Close the connection after reading the data
conn.close()

# Verify the data
# print("\nFirst few rows:")
# display(df.head(2))




# In[7]:


# df.info()


# In[8]:


# Преобразование activation_date в месяцы
df['activation_date'] = pd.to_datetime(df['activation_date']).dt.strftime('%Y-%m')


# В этом исследовании рассматриваем только бренд Сбер
# 

# In[9]:


df = df[df['brand'] == 'sber']
# df.info()


# In[10]:


questions = df[['question_num', 'question']].sort_values(by='question_num')
# Get unique pairs of question_num and question
unique_questions = questions.drop_duplicates()

# Filter unique questions where question_num is less than 12 and not equal to 2
filtered_questions = unique_questions[(unique_questions['question_num'] < 12) & 
                                     (unique_questions['question_num'] != 2)].copy()

# Create a new column without the prefix 'Оцените, насколько вы довольны'
filtered_questions.loc[:, 'question_clean'] = filtered_questions['question'].str.replace('Оцените, насколько вы довольны', '').str.strip()

# Replace unique_questions with the filtered version
unique_questions = filtered_questions


# display(unique_questions)


# ## 1. Основной вопрос: Насколько вы довольны телевизором на платформе Салют ТВ?

# Вопросы начинаются с одинакового пассажа "Оцените, насколько вы довольны " - уберём его для краткости

# In[11]:


current_question = unique_questions[unique_questions['question_num'] == 1]
display(current_question)


# In[12]:


def get_question_data(current_question):
    question_data = df[df['question_num'] == current_question['question_num'].values[0]].copy()

    if question_data['answer_txt'].dtype == 'object':
        try:
            question_data.loc[:, 'answer_txt_numeric'] = pd.to_numeric(
                question_data['answer_txt'])
            answer_column = 'answer_txt_numeric'
        except Exception:
            print("Warning: Не могу преобразовать answer_txt в числовую форму. ")
    else:
        answer_column = 'answer_txt'

    cleaned_question = current_question['question_clean'].values[0]

    return question_data, answer_column, cleaned_question


# In[13]:


question_data, answer_column, cleaned_question = get_question_data(current_question)


# ### Срез 1: Показатели по бренду

# In[14]:


current_segment = 'brand'


# In[15]:


def display_pivot(question_data, answer_column, current_segment):
    pivot = question_data.pivot_table(
        index=current_segment, 
        values=answer_column,
        aggfunc=['mean', 'count']
    )

    # Сортировка по count (descending) для первых наиболее часто встречающихся значений brand
    pivot = pivot.sort_values(('count', answer_column), ascending=False)

    # Вывод первых 10 наиболее часто встречающихся значений brand и их средних ответов
    display(pivot.head(10))
    return pivot


# Средние оценки по брендам за всё время в датасете

# In[16]:


pivot = display_pivot(question_data, answer_column, current_segment)


# In[17]:


def show_spread(question_data, answer_column, current_segment, pivot, cleaned_question, n_top=10):
    # Визуализация взаимосвязи для первых 10 значений 
    top_values = pivot.head(n_top).index.tolist()

    # Сортировка для обеспечения последовательного порядка по оси x
    top_values.sort()

    # Создаем копию данных, чтобы избежать SettingWithCopyWarning
    filtered_data = question_data[question_data[current_segment].isin(top_values)].copy()
    
    # Используем .loc для установки значений в DataFrame
    filtered_data.loc[:, 'month'] = filtered_data['answer_dt'].dt.to_period('M').astype(str)

    
    fig = px.box(filtered_data, x=current_segment, y=answer_column, 
                    title='Распределение оценок за всё время (октябрь 2024 - январь 2025)',
                    width=900)
    fig.update_layout(
        xaxis_title=current_segment,
        yaxis_title='Оценка',
        xaxis_tickangle=45,
        xaxis={'categoryorder': 'array', 'categoryarray': top_values}
    )
    fig.show()
    fig.write_html('chart_00.html', include_plotlyjs='cdn')
    
    return top_values, filtered_data


# In[18]:


top_values, filtered_data = show_spread(question_data, answer_column, current_segment, pivot, cleaned_question)


# In[19]:


def show_time_series(filtered_data, answer_column, current_segment, top_values, cleaned_question):
    # Добавление столбца временного периода (месяц)
    # Создаем копию данных, чтобы избежать SettingWithCopyWarning
    filtered_data = filtered_data.copy()

    # Создание таблицы Pivot: месяц vs средний ответ для каждой группы
    time_pivot = filtered_data.pivot_table(
        index='month',
        columns=current_segment,
        values=answer_column,
        aggfunc='mean'
    )

    # Визуализация временных рядов
    fig = go.Figure()

    for brand_value in top_values:
        if brand_value in time_pivot.columns:
            fig.add_trace(go.Scatter(
                x=time_pivot.index,
                y=time_pivot[brand_value],
                mode='lines+markers',
                name=f'{brand_value}'
            ))

    fig.update_layout(
        title='Среденяя оценка по бренду во времени',
        xaxis_title='Месяц ответа',
        yaxis_title='Средняя оценка',
        width=1000,
        height=600,
        legend_title='brand'
    )
    fig.show()
    fig.write_html('chart_01.html', include_plotlyjs='cdn')


# In[20]:


def show_time_series_amount(filtered_data, answer_column, current_segment, top_values, cleaned_question):
    # Добавление столбца временного периода (месяц)
    # Создаем копию данных, чтобы избежать SettingWithCopyWarning
    filtered_data = filtered_data.copy()

    # Создание таблицы Pivot: месяц vs средний ответ для каждой группы
    time_pivot_mean = filtered_data.pivot_table(
        index='month',
        columns=current_segment,
        values=answer_column,
        aggfunc='mean'
    )
    
    # Создание таблицы Pivot: месяц vs количество ответов для каждой группы
    time_pivot_count = filtered_data.pivot_table(
        index='month',
        columns=current_segment,
        values=answer_column,
        aggfunc='count'
    )

    # Создаем подграфики: один для средних значений, другой для количества
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        subplot_titles=('Средняя оценка', 'Количество ответов'),
                        vertical_spacing=0.1)
    
    # Создаем цветовую карту для сегментов
    colors = px.colors.qualitative.Plotly
    color_map = {segment: colors[i % len(colors)] for i, segment in enumerate(top_values)}

    # Добавляем линии для средних значений
    for brand_value in top_values:
        if brand_value in time_pivot_mean.columns:
            segment_color = color_map[brand_value]
            
            fig.add_trace(
                go.Scatter(
                    x=time_pivot_mean.index,
                    y=time_pivot_mean[brand_value],
                    mode='lines+markers',
                    name=f'{brand_value} (mean)',
                    legendgroup=brand_value,
                    line=dict(color=segment_color)
                ),
                row=1, col=1
            )
            
            # Добавляем линии для количества ответов
            fig.add_trace(
                go.Bar(
                    x=time_pivot_count.index,
                    y=time_pivot_count[brand_value],
                    name=f'{brand_value} (count)',
                    legendgroup=brand_value,
                    marker_color=segment_color,  # Используем тот же цвет из карты
                    showlegend=False
                ),
                row=2, col=1
            )

    fig.update_layout(
        title=f'{cleaned_question[:50]}...' if len(cleaned_question) > 50 else cleaned_question,
        width=1000,
        height=800,
        legend_title=current_segment
    )
    
    fig.update_xaxes(title_text='Месяц ответа', row=2, col=1)
    fig.update_yaxes(title_text='Средняя оценка', row=1, col=1)
    fig.update_yaxes(title_text='Количество ответов', row=2, col=1)
    
    fig.show()
    fig.write_html('chart_02.html', include_plotlyjs='cdn')


# In[21]:


def show_time_series_corrected(filtered_data, answer_column, current_segment, top_values, cleaned_question):
    # Добавление столбца временного периода (месяц)
    # Создаем копию данных, чтобы избежать SettingWithCopyWarning
    filtered_data = filtered_data.copy()
    
    # Группировка данных по месяцам для расчета общего среднего
    monthly_data = filtered_data.groupby('month')[answer_column].mean()
    
    # Визуализация временных рядов
    fig = go.Figure()
    
    for segment_value in top_values:
        # Создаем датафрейм без текущего сегмента
        data_without_segment = filtered_data[filtered_data[current_segment] != segment_value]
        
        # Рассчитываем среднее значение по месяцам без текущего сегмента
        if not data_without_segment.empty:
            mean_without_segment = data_without_segment.groupby('month')[answer_column].mean()
            
            fig.add_trace(go.Scatter(
                x=mean_without_segment.index,
                y=mean_without_segment.values,
                mode='lines+markers',
                name=f'Без {segment_value}'
            ))
    
    # Добавляем линию общего среднего для сравнения
    fig.add_trace(go.Scatter(
        x=monthly_data.index,
        y=monthly_data.values,
        mode='lines+markers',
        name='Общее среднее',
        line=dict(dash='dash', color='black')
    ))
    
    fig.update_layout(
        title=f'{cleaned_question[:50]}...' if len(cleaned_question) > 50 else cleaned_question,
        xaxis_title='Месяц ответа',
        yaxis_title='Средняя оценка (без сегмента)',
        width=1000,
        height=600,
        legend_title=current_segment
    )
    fig.show()


# Оценки по бренду во времени

# In[22]:


show_time_series(filtered_data, answer_column, current_segment, top_values, cleaned_question)


# Оценка растёт с октября 2024 по декабрь 2024 и припадает в январе 2025

# In[23]:


def show_heatmap(filtered_data, answer_column, current_segment, cleaned_question):
    # Создание тепловой карты ответов по времени по группам v23
    heatmap_pivot = filtered_data.pivot_table(
        index='month',
        columns=current_segment,
        values=answer_column,
        aggfunc='mean'
    )

    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x=current_segment, y="Месяц ответа", color="Средний ответ"),
        title=f'{cleaned_question[:50]}...' if len(cleaned_question) > 50 else cleaned_question,
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )
    fig.update_layout(width=900, height=600)
    fig.show()
    fig.write_html('chart_03.html', include_plotlyjs='cdn')


# ### Срез 2: влияние аппаратных платформ

# Средние оценки и количество ответов по платформам

# In[24]:


current_segment = 'device_plate'
pivot = display_pivot(question_data, answer_column, current_segment)


# Низкие оценки у плат CV 6681

# In[25]:


# Create a pivot table to count unique device_ids by device_plate and answer month
device_plate_time_data = question_data.copy()
device_plate_time_data['answer_month'] = device_plate_time_data['answer_dt'].dt.strftime('%Y-%m')

# Group by device_plate and answer_month to get count of unique device_ids
plate_time_counts = device_plate_time_data.groupby(['device_plate', 'answer_month'])['device_id'].nunique().reset_index(name='unique_devices')

# Calculate total unique devices per answer_month
total_devices_per_month = device_plate_time_data.groupby('answer_month')['device_id'].nunique().reset_index(name='total_devices')

# Merge the counts with totals
plate_time_counts = plate_time_counts.merge(total_devices_per_month, on='answer_month')

# Calculate percentage
plate_time_counts['percentage'] = (plate_time_counts['unique_devices'] / plate_time_counts['total_devices'] * 100).round(2)

# Create a heatmap to visualize the distribution of percentages
plate_time_pivot = plate_time_counts.pivot_table(
    index='device_plate',
    columns='answer_month',
    values='percentage',
    aggfunc='sum',
    fill_value=0
)

# Plot the heatmap
fig = px.imshow(
    plate_time_pivot,
    labels=dict(x="Месяц ответа", y="Платформа", color="% от общего количества устройств"),
    title=f'Распределение плат по времени (вклад в общее количество ответов)',
    color_continuous_scale="Viridis",
    aspect="auto"
)
fig.update_layout(width=900, height=600)
fig.show()
fig.write_html('chart_04.html', include_plotlyjs='cdn')


# In[26]:


top_values, filtered_data = show_spread(question_data, answer_column, current_segment, pivot, cleaned_question)


# Распределение оценок у CV 6681 в зоне от 1 до 4х - ниже чем у других, 9256 тоже получает низкие оценки

# Рассмотрим вклад платформ в оценки с учётом количества ответов

# In[27]:


show_time_series_amount(filtered_data, answer_column, current_segment, top_values, cleaned_question)


# В зоне негатива - (CVTE 9256 и CV6681). В ноябре и январе увеличен вклад платы 9256. Вклад CV6681 низкий. Вклад CVTE 9256 уменьшается.

# In[28]:


show_time_series_corrected(filtered_data, answer_column, current_segment, top_values, cleaned_question)


# Платы CVTE 9256 , CV 9632, и CV6681 одинаково негативно влияют на оценки, несмотря на разницу в количестве ответов. 

# In[29]:


show_heatmap(filtered_data, answer_column, current_segment, cleaned_question)


# ### Срез 3: Зависимость от даты активации (activation_date)

# In[30]:


current_segment = 'activation_date'

pivot = question_data.pivot_table(
    index=[current_segment, 'device_plate'], 
    values=answer_column,
    aggfunc=['mean', 'count']
)

# Сортировка по count (descending) для первых наиболее часто встречающихся значений
pivot = pivot.sort_values(('count', answer_column), ascending=False)

# Вывод первых 10 наиболее часто встречающихся значений и их средних ответов
display(pivot.head(10))


# In[31]:


# Convert answer_dt to month format and activation_date to month format
question_data['answer_month'] = question_data['answer_dt'].dt.strftime('%Y-%m')
question_data['activation_month'] = pd.to_datetime(question_data['activation_date']).dt.strftime('%Y-%m')

# Calculate lifetime in months (difference between answer_month and activation_month)
question_data['answer_month_dt'] = pd.to_datetime(question_data['answer_month'])
question_data['activation_month_dt'] = pd.to_datetime(question_data['activation_month'])
question_data['lifetime_months'] = ((question_data['answer_month_dt'].dt.year - question_data['activation_month_dt'].dt.year) * 12 + 
                                   (question_data['answer_month_dt'].dt.month - question_data['activation_month_dt'].dt.month))

# Get unique device_plates for dropdown selector
device_plates = sorted(question_data['device_plate'].unique())
device_plates_options = [{'label': 'All', 'value': 'All'}] + [{'label': plate, 'value': plate} for plate in device_plates]

# Create a function to generate the plot based on selected device_plate
def create_plot(device_plate='All'):
    # Filter data based on selected device_plate
    if device_plate == 'All':
        filtered_data = question_data
    else:
        filtered_data = question_data[question_data['device_plate'] == device_plate]
    
    # Group by lifetime_months and answer_month to get count of unique device_ids
    grouped_data = filtered_data.groupby(['lifetime_months', 'answer_month'])['device_id'].nunique().reset_index(name='unique_devices')
    
    # Calculate total unique devices per answer_month
    activation_totals = filtered_data.groupby('answer_month')['device_id'].nunique().reset_index(name='total_devices')
    
    # Merge to get the totals alongside the grouped data
    grouped_data = grouped_data.merge(activation_totals, on='answer_month', how='left')
    
    # Calculate percentage of unique devices
    grouped_data['percentage'] = (grouped_data['unique_devices'] / grouped_data['total_devices'] * 100).round(2)
    
    # Create scatterplot
    title_suffix = f" - {device_plate}" if device_plate != 'All' else ""
    fig = px.scatter(
        grouped_data,
        x='lifetime_months',
        y='answer_month',
        size='percentage',
        color='percentage',
        title=f'Процент устройств от общего количества по времени использования и месяцу ответа{title_suffix}',
        labels={
            'lifetime_months': 'Время использования (месяцы)',
            'answer_month': 'Месяц ответа',
            'percentage': 'Процент устройств (%)'
        },
        color_continuous_scale='Viridis',
        opacity=0.7,
        hover_data=['unique_devices', 'total_devices', 'percentage']
    )
    
    # Ensure y-axis shows months in chronological order
    all_months = sorted(grouped_data['answer_month'].unique())
    fig.update_layout(
        width=1000,
        height=600,
        xaxis_title='Lifetime (months)',
        yaxis_title='Answer Month',
        yaxis=dict(
            categoryorder='array',
            categoryarray=all_months
        )
    )
    
    return fig

# Create the initial plot
fig = create_plot()

# Add dropdown to the figure
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(
                    args=[{
                        'x': [create_plot(device_plate).data[0].x],
                        'y': [create_plot(device_plate).data[0].y],
                        'marker.size': [create_plot(device_plate).data[0].marker.size],
                        'marker.color': [create_plot(device_plate).data[0].marker.color]
                    }],
                    label=device_plate,
                    method="restyle"
                ) for device_plate in ['All'] + list(device_plates)
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top",
            bgcolor="white",
            bordercolor="lightgray",
            font=dict(size=12)
        ),
    ],
    annotations=[
        dict(text="Device Plate:", x=0, y=1.15, xref="paper", yref="paper", 
             showarrow=False, font=dict(size=14))
    ]
)

fig.show()
fig.write_html('chart_05.html', include_plotlyjs='cdn')


# В целом, на оценки больше всего влияют свежие устройства, но есть значимые группы устройств с LT 10-15 месяцев в каждом опросе.

# In[32]:


# Визуализация взаимосвязи
top_values = pivot.head(50).index.tolist()

# Извлекаем уникальные даты и device_plate из top_values
dates = sorted(list(set([val[0] for val in top_values])))
device_plates = sorted(list(set([val[1] for val in top_values])))

# Создаем копию данных, чтобы избежать SettingWithCopyWarning
filtered_data = question_data[
    pd.to_datetime(question_data['activation_date']).dt.strftime('%Y-%m').isin([val[0] for val in top_values]) & 
    question_data['device_plate'].isin([val[1] for val in top_values])
].copy()

# Используем .loc для установки значений в DataFrame
filtered_data.loc[:, 'activation_month'] = pd.to_datetime(filtered_data['activation_date']).dt.strftime('%Y-%m')
filtered_data.loc[:, 'answer_month'] = pd.to_datetime(filtered_data['answer_dt']).dt.strftime('%Y-%m')

# Вычисляем lifetime в месяцах
# Преобразуем результат в int32 для совместимости типов данных
lifetime_days = (pd.to_datetime(filtered_data['answer_month']) - 
                pd.to_datetime(filtered_data['activation_month'])).dt.days
filtered_data.loc[:, 'lifetime_months'] = (lifetime_days // 30).astype('int32')

# Создаем функцию для генерации графика на основе выбранного device_plate
def create_device_plot(device_plate='All'):
    if device_plate == 'All':
        plot_data = filtered_data
        title_suffix = ""
    else:
        plot_data = filtered_data[filtered_data['device_plate'] == device_plate]
        title_suffix = f" - {device_plate}"
    
    fig = px.box(plot_data, x='lifetime_months', y=answer_column, 
                title=f'{cleaned_question[:50]}...{title_suffix}' if len(cleaned_question) > 50 
                else f'{cleaned_question}{title_suffix}',
                width=900)
    fig.update_layout(
        xaxis_title='Lifetime (months)',
        yaxis_title='Оценка',
        xaxis_tickangle=45
    )
    return fig

# Создаем начальный график
fig = create_device_plot()

# Добавляем выпадающий список к графику
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(
                    args=[{
                        'x': [create_device_plot(device_plate).data[0].x],
                        'y': [create_device_plot(device_plate).data[0].y],
                        'marker.color': [create_device_plot(device_plate).data[0].marker.color]
                    }],
                    label=device_plate,
                    method="restyle"
                ) for device_plate in ['All'] + device_plates
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top",
            bgcolor="white",
            bordercolor="lightgray",
            font=dict(size=12)
        ),
    ],
    annotations=[
        dict(text="Device Plate:", x=0, y=1.15, xref="paper", yref="paper", 
             showarrow=False, font=dict(size=14))
    ]
)

fig.show()
fig.write_html('chart_06.html', include_plotlyjs='cdn')


# Чем больше время использования устройства, тем шире распределение оценок (вариативность).

# In[33]:


# Добавление столбца временного периода (месяц)
# Создаем копию данных, чтобы избежать SettingWithCopyWarning
filtered_data = filtered_data.copy()

# Проверяем, есть ли столбец 'answer_month', если нет - добавляем
if 'answer_month' not in filtered_data.columns:
    filtered_data['answer_month'] = pd.to_datetime(filtered_data['answer_dt']).dt.strftime('%Y-%m')

# Добавляем столбец activation_month, если его нет
if 'activation_month' not in filtered_data.columns:
    filtered_data['activation_month'] = pd.to_datetime(filtered_data['activation_date']).dt.strftime('%Y-%m')

# Рассчитываем lifetime (разница между месяцем ответа и месяцем активации)
filtered_data['answer_month_dt'] = pd.to_datetime(filtered_data['answer_month'])
filtered_data['activation_month_dt'] = pd.to_datetime(filtered_data['activation_month'])
filtered_data['lifetime_months'] = ((filtered_data['answer_month_dt'].dt.year - filtered_data['activation_month_dt'].dt.year) * 12 + 
                                   (filtered_data['answer_month_dt'].dt.month - filtered_data['activation_month_dt'].dt.month))

# Получаем уникальные device_plates для выпадающего списка
device_plates = sorted(filtered_data['device_plate'].unique())

# Создаем функцию для генерации графика на основе выбранного device_plate
def create_time_series_plot(device_plate='All'):
    # Фильтруем данные по выбранному device_plate
    if device_plate == 'All':
        plot_data = filtered_data
        title_suffix = ""
    else:
        plot_data = filtered_data[filtered_data['device_plate'] == device_plate]
        title_suffix = f" - {device_plate}"
    
    # Создание таблицы Pivot: месяц vs средний ответ для каждой группы
    time_pivot = plot_data.pivot_table(
        index='answer_month',
        columns='lifetime_months',
        values=answer_column,
        aggfunc='mean'
    )
    
    # Визуализация временных рядов
    fig = go.Figure()
    
    for segment_value in time_pivot.columns:
        fig.add_trace(go.Scatter(
            x=time_pivot.index,
            y=time_pivot[segment_value],
            mode='lines+markers',
            name=f'{segment_value} месяцев'
        ))
    
    fig.update_layout(
        title=f'{cleaned_question[:50]}...{title_suffix}' if len(cleaned_question) > 50 else f'{cleaned_question}{title_suffix}',
        xaxis_title='Месяц ответа',
        yaxis_title='Средняя оценка',
        width=1000,
        height=600,
        legend_title='Срок использования (месяцы)'
    )
    
    return fig

# Создаем начальный график
fig = create_time_series_plot()

# Добавляем выпадающий список к графику
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(
                    args=[{
                        'x': [create_time_series_plot(device_plate).data[i].x for i in range(len(create_time_series_plot(device_plate).data))],
                        'y': [create_time_series_plot(device_plate).data[i].y for i in range(len(create_time_series_plot(device_plate).data))],
                        'name': [create_time_series_plot(device_plate).data[i].name for i in range(len(create_time_series_plot(device_plate).data))]
                    }],
                    label=device_plate,
                    method="restyle"
                ) for device_plate in ['All'] + list(device_plates)
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top",
            bgcolor="white",
            bordercolor="lightgray",
            font=dict(size=12)
        ),
    ],
    annotations=[
        dict(text="Device Plate:", x=0, y=1.15, xref="paper", yref="paper", 
             showarrow=False, font=dict(size=14))
    ]
)

fig.show()
fig.write_html('chart_07.html', include_plotlyjs='cdn')


# Чем раньше активирован девайс - тем "холоднее" у него оценки по датам опросов

# In[34]:


# Создание тепловой карты ответов по времени по группам v23
# Создаем начальный график для всех устройств
def create_heatmap(device_plate='All'):
    # Фильтруем данные по выбранному device_plate
    if device_plate == 'All':
        plot_data = filtered_data
        title_suffix = ""
    else:
        plot_data = filtered_data[filtered_data['device_plate'] == device_plate]
        title_suffix = f" - {device_plate}"
    
    # Вычисляем lifetime (разница между месяцем ответа и месяцем активации)
    plot_data = plot_data.copy()
    
    # Преобразуем строковые месяцы в datetime объекты перед вычитанием
    plot_data['answer_month_dt'] = pd.to_datetime(plot_data['answer_month'])
    plot_data['activation_month_dt'] = pd.to_datetime(plot_data['activation_month'])
    
    # Вычисляем разницу в месяцах
    plot_data['lifetime'] = ((plot_data['answer_month_dt'].dt.year - plot_data['activation_month_dt'].dt.year) * 12 + 
                             (plot_data['answer_month_dt'].dt.month - plot_data['activation_month_dt'].dt.month))
    
    # Создание тепловой карты
    heatmap_pivot = plot_data.pivot_table(
        index='answer_month',
        columns='lifetime',
        values=answer_column,
        aggfunc='mean'
    )
    
    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x='Lifetime (месяцы)', y="Месяц ответа", color="Средний ответ"),
        title=f'{cleaned_question[:50]}...{title_suffix}' if len(cleaned_question) > 50 else f'{cleaned_question}{title_suffix}',
        color_continuous_scale="RdBu_r",
        aspect="auto"
    )
    fig.update_layout(width=900, height=600)
    
    return fig

# Создаем начальный график
fig = create_heatmap()

# Добавляем выпадающий список к графику
fig.update_layout(
    updatemenus=[
        dict(
            buttons=[
                dict(
                    args=[{
                        'z': [create_heatmap(device_plate).data[0].z],
                        'x': [create_heatmap(device_plate).data[0].x],
                        'y': [create_heatmap(device_plate).data[0].y],
                        'colorscale': [create_heatmap(device_plate).data[0].colorscale]
                    }],
                    label=device_plate,
                    method="restyle"
                ) for device_plate in ['All'] + sorted(list(set(filtered_data['device_plate'].unique())))
            ],
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.15,
            yanchor="top",
            bgcolor="white",
            bordercolor="lightgray",
            font=dict(size=12)
        ),
    ],
    annotations=[
        dict(text="Device Plate:", x=0, y=1.15, xref="paper", yref="paper", 
             showarrow=False, font=dict(size=14))
    ]
)

fig.show()
fig.write_html('chart_08.html', include_plotlyjs='cdn')


# Чем раньше активирован девайс - тем "холоднее" у него оценки по датам опросов

# ### group_name

# In[35]:


question_data['group_name_slice'] = question_data['group_name'].str.slice(0, 30)
current_segment = 'group_name_slice'
pivot = display_pivot(question_data, answer_column, current_segment)



# In[36]:


top_values, filtered_data = show_spread(question_data, answer_column, current_segment, pivot, cleaned_question)


# In[37]:


show_time_series(filtered_data, answer_column, current_segment, top_values, cleaned_question)


# Группы на 9256 и 6681 - в нижней зоне по оценкам

# In[38]:


show_heatmap(filtered_data, answer_column, current_segment, cleaned_question)


# ### Основные выводы:

# 1. Динамика общей оценки:
# - Наблюдается рост оценок с октября 2024 по декабрь 2024
# - В январе 2025 происходит снижение оценок
# 
# 2. Влияние аппаратных платформ:
# - Выявлены проблемные платформы с низкими оценками:
#   - CV 6681 (оценки в зоне 1-4)
#   - CVTE 9256 (также получает низкие оценки)
# - Вклад CV6681 в общее количество ответов низкий
# - Вклад CVTE 9256 постепенно уменьшается
# - Платы CVTE 9256, CV 9632 и CV6681 одинаково негативно влияют на оценки, несмотря на разницу в количестве ответов
# 
# 3. Зависимость от времени использования (lifetime):
# - Чем больше время использования устройства, тем шире распределение оценок (выше вариативность)
# - Устройства с более ранней датой активации демонстрируют более низкие ("холодные") оценки по датам опросов
# - В каждом опросе присутствуют значимые группы устройств с длительностью использования 10-15 месяцев
# 
# 4. Группы устройств:
# - Группы устройств на платформах 9256 и 6681 показывают стабильно низкие оценки
# - Прослеживается четкая корреляция между аппаратной платформой и оценками пользователей
# 
# Общий тренд указывает на наличие системных проблем с определенными аппаратными платформами, которые негативно влияют на пользовательский опыт. Особое внимание следует уделить платформам CV 6681 и CVTE 9256, так как они демонстрируют наиболее низкие показатели удовлетворенности пользователей.
# 
# На основе проведенного анализа, для получения актуальных результатов опроса следует учитывать следующие требования к выборке:
# 
# 1. По времени использования (lifetime):
# - Ограничить выборку устройствами с lifetime до 10-15 месяцев (на усмотрение продуктовой команды)
# - Сделать акцент на устройствах с небольшим сроком использования (0-6 месяцев), так как они дают более стабильные оценки
# - Учитывать, что устройства с большим сроком использования показывают более вариативные результаты
# 
# 2. По аппаратным платформам:
# - Обеспечить пропорциональное представление всех актуальных платформ
# - Отдельно анализировать результаты по проблемным платформам (CV 6681, CVTE 9256)
# - Исключить устаревшие/снятые с производства платформы
# 
# 3. По времени проведения опроса:
# - Обеспечить равномерное распределение участников опросов по месяцам
# 
# 4. По объему выборки:
# - Следить за репрезентативностью выборки по отношению к общей базе установленных устройств
# 
# 5. По группам устройств:
# - Учитывать различные группы пользователей
# - Обеспечить представительство всех актуальных моделей устройств
# - Отслеживать корреляцию между группами и платформами
# 
# 
# 
# 

# 
