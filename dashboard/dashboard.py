import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Menyiapkan data day_df

day_df = pd.read_csv(r"C:\Users\ACER\submission\Bike-sharing-dataset\day.csv")
day_df.head()

drop_col = ['instant']

for i in day_df.columns:
    if i in drop_col:
        day_df.drop(labels = i, axis = 1, inplace = True)

day_df.rename(columns={'dteday':'datetime',
                        'weathersit':'weather_condition',
                        'hum':'humidity',
                        'mnth':'month',
                        'cnt':'total_count',
                        'yr':'year'},inplace=True)

day_df['weather_condition']= day_df['weather_condition'].map({1: 'Clear to partly cloudy', 2: 'Misty and cloudy',
                                                              3: 'Light rain or snow', 4: 'Heavy rain or snow'})

day_df['season']= day_df['season'].map({1:'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})

day_df['month']= day_df['month'].map({1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'})

day_df['weekday']= day_df['weekday'].map({0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'})

day_df[['temp', 'atemp', 'humidity', 'windspeed']] = day_df[['temp', 'atemp', 'humidity', 'windspeed']].multiply([41, 50, 100, 67], axis=1)

# Menyiapkan daily_rent_df
daily_rent_df= day_df.groupby(by= ['datetime']).agg({
    'total_count':['sum']
})

# Menyiapkan daily_casual_rent_df
daily_casual_rent_df= day_df.groupby(by= ['datetime']).agg({
    'casual':['sum']
})

# Menyiapkan daily_registered_rent_df
daily_registered_rent_df= day_df.groupby(by= ['datetime']).agg({
    'registered':['sum']
})
    
# Menyiapkan season_rent_df
season_rent_df= day_df.groupby(by= ['season']).agg({
    'total_count':['sum']
})

# Menyiapkan monthly_rent_df
monthly_rent_df= day_df.groupby(by= ['month']).agg({
    'total_count':'sum'
})

# Menyiapkan goly_df
goly_df= day_df.pivot_table(index= 'month', columns= 'year', values= 'total_count', aggfunc= 'mean')
goly_df.columns=['2011', '2012']
goly_df['percent growth']= round(((goly_df['2012'] - goly_df['2011'])/goly_df['2011'])*100,2)
goly_df = goly_df.sort_values(by= 'percent growth', ascending= False)

# membuat komponen filter

min_date = pd.to_datetime(day_df['datetime']).dt.date.min()
max_date = pd.to_datetime(day_df['datetime']).dt.date.max()
 
with st.sidebar:
    st.image('https://www.flaticon.com/free-icon/bicycle-rider_71422')
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value= min_date,
        max_value= max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df['datetime'] >= str(start_date)) & 
                (day_df['datetime'] <= str(end_date))]

# melengkapi dashboard

st.header('Bikesharing Rental')

# membuat jumlah peminjaman harian
st.subheader('Daily rent')
 
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = main_df['casual'].sum()
    st.metric('Casual user', value= daily_rent_casual)

with col2:
    daily_rent_registered = main_df['registered'].sum()
    st.metric('Registered user', value= daily_rent_registered)
 
with col3:
    daily_rent_total = main_df['total_count'].sum()
    st.metric('Total user', value= daily_rent_total)
 

# plot daily rent grafik
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df.index,
    main_df['total_count'],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

# Membuat jumlah peminjaman berdasarkan season
st.subheader('Season rent')

plt.figure(figsize=(8,4))

ax = sns.barplot(data= day_df.groupby(by= ['season']).agg({
    'casual':['mean'],'registered':['mean'],
    'total_count':['sum','max','min','mean']}).reset_index(),
    x= 'season', y= ('total_count', 'sum'), palette= 'Purples')

ax.set_title('Variation of count with season')
ax.set_ylabel('')
ax.set_xlabel('')
ax.tick_params(axis='x', labelsize= 35)
ax.tick_params(axis='y', labelsize= 30)
st.pyplot(plt.gcf())

[deprecation]
showPyplotGlobalUse = false
