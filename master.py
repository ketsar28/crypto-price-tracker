# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 00:03:56 2025
@author: KETSAR - Improved by Gemini
"""
import streamlit as st
import pandas as pd
from PIL import Image
import requests
import json
from bs4 import BeautifulSoup
import plotly.express as px

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Harga Kripto Real-Time",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Tampilan Header ---
st.title('📈 Aplikasi Harga Kripto')
st.markdown("Aplikasi ini mengambil data harga 100 Kripto teratas secara *real-time* dari **CoinMarketCap**.")
st.divider()

# --- Fungsi Pengambilan Data ---
@st.cache_data(ttl=600) # Cache data selama 10 menit
def load_data(currency_unit):
    try:
        cmc = requests.get('https://coinmarketcap.com')
        cmc.raise_for_status()
        soup = BeautifulSoup(cmc.content, 'html.parser')

        data = soup.find('script', id='__NEXT_DATA__', type='application/json')
        coin_data = json.loads(data.contents[0])
        listings = coin_data['props']['dehydratedState']['queries'][1]['state']['data']['data']['listing']['cryptoCurrencyList']

        coin_name, coin_symbol, market_cap, price, volume_24h = [], [], [], [], []
        percent_change_1h, percent_change_24h, percent_change_7d = [], [], []

        for coin in listings:
            coin_name.append(coin['name'])
            coin_symbol.append(coin['symbol'])
            
            quote_unit = next((quote for quote in coin['quotes'] if quote['name'] == currency_unit), None)
            
            if quote_unit:
                price.append(quote_unit.get('price'))
                percent_change_1h.append(quote_unit.get('percentChange1h'))
                percent_change_24h.append(quote_unit.get('percentChange24h'))
                percent_change_7d.append(quote_unit.get('percentChange7d'))
                market_cap.append(quote_unit.get('marketCap'))
                volume_24h.append(quote_unit.get('volume24h'))
            else:
                price.append(None); market_cap.append(None); volume_24h.append(None)
                percent_change_1h.append(None); percent_change_24h.append(None); percent_change_7d.append(None)
        
        df = pd.DataFrame({
            'Nama Koin': coin_name, 'Simbol': coin_symbol,
            f'Kapitalisasi Pasar ({currency_unit})': market_cap, f'Harga ({currency_unit})': price,
            f'Volume 24j ({currency_unit})': volume_24h, 'Perubahan 1j (%)': percent_change_1h,
            'Perubahan 24j (%)': percent_change_24h, 'Perubahan 7h (%)': percent_change_7d
        })
        
        return df.dropna()
    except (requests.exceptions.RequestException, KeyError, IndexError, json.JSONDecodeError) as e:
        st.error(f"Gagal mengambil data: {e}")
        return pd.DataFrame()

# --- Sidebar ---
with st.sidebar:
    st.image('logo.jpg', width=200)
    st.header('⚙️ Opsi Tampilan')
    currency_price_unit = st.selectbox('Pilih Mata Uang:', ('USD', 'IDR', 'BTC', 'ETH'))
    
    with st.spinner(f'Mengambil data dalam {currency_price_unit}...'):
        df = load_data(currency_price_unit)

    if not df.empty:
        sorted_coin = sorted(df['Simbol'])
        selected_coin = st.multiselect('Pilih Kripto', sorted_coin, ['BTC', 'ETH', 'XRP', 'DOGE', 'SOL'])
        num_coin = st.slider('Tampilkan N Koin Teratas', 1, 100, 10)
        percent_timeframe = st.selectbox('Periode Perubahan Harga', ['7h', '24j', '1j'])
        sort_values = st.selectbox('Urutkan nilai?', ['Tidak', 'Ya'])
    
    st.divider()
    with st.expander('About Aplikasi'):
        st.markdown("""
        * **Sumber Data:** [CoinMarketCap](http://coinmarketcap.com).
        * **Dibuat dengan:** Python, Streamlit, Pandas, BeautifulSoup, Plotly.
        """)

# --- Konten Utama ---
if not df.empty:
    df_selected_coin = df[df['Simbol'].isin(selected_coin)]
    df_coins = df_selected_coin[:num_coin]
    selected_percent_timeframe = f'Perubahan {percent_timeframe} (%)'

    st.subheader("Ringkasan Pasar")
    cols = st.columns(len(df_coins) if len(df_coins) <= 4 else 4)
    for i, col in enumerate(cols):
        if i < len(df_coins):
            coin = df_coins.iloc[i]
            col.metric(
                label=f"{coin['Nama Koin']} ({coin['Simbol']})",
                value=f"{coin[f'Harga ({currency_price_unit})']:,.2f}",
                delta=f"{coin['Perubahan 24j (%)']:.2f}% (24j)"
            )
    st.divider()

    tab1, tab2, tab3 = st.tabs(["📊 Data Lengkap", "📈 Grafik Perubahan", "💰 Dominasi Pasar"])

    with tab1:
        st.subheader('Data Harga Koin Kripto Pilihan')
        
        def style_dataframe(df_to_style, currency_unit):
            def color_change(val):
                if pd.isna(val): return ''
                color = 'red' if val < 0 else '#00D084'
                return f'color: {color}'

            format_dict = {
                f'Harga ({currency_unit})': '{:,.2f}', f'Kapitalisasi Pasar ({currency_unit})': '{:,.0f}',
                f'Volume 24j ({currency_unit})': '{:,.0f}', 'Perubahan 1j (%)': '{:+.2f}%',
                'Perubahan 24j (%)': '{:+.2f}%', 'Perubahan 7h (%)': '{:+.2f}%'
            }
            change_cols = ['Perubahan 1j (%)', 'Perubahan 24j (%)', 'Perubahan 7h (%)']
            
            styled_df = df_to_style.style.format(format_dict).apply(
                lambda x: [color_change(v) for v in x], subset=change_cols
            ).background_gradient(
                cmap='viridis', subset=[f'Kapitalisasi Pasar ({currency_unit})']
            )
            return styled_df
            
        if sort_values == 'Ya':
            df_coins_sorted = df_coins.sort_values(by=selected_percent_timeframe, ascending=False)
        else:
            df_coins_sorted = df_coins
        
        st.dataframe(style_dataframe(df_coins_sorted, currency_price_unit), use_container_width=True, hide_index=True)

        @st.cache_data
        def to_csv(df_to_convert):
            return df_to_convert.to_csv(index=False).encode('utf-8')

        csv_data = to_csv(df_selected_coin)
        st.download_button(
            label="📥 Download Data Lengkap (CSV)", data=csv_data,
            file_name=f'crypto_data_{currency_price_unit.lower()}.csv', mime='text/csv'
        )

    with tab2:
        st.subheader(f'Grafik Perubahan Harga (%) - Periode {percent_timeframe}')
        
        df_plot = df_coins[['Simbol', selected_percent_timeframe]].set_index('Simbol').copy()

        df_plot['Naik'] = df_plot[selected_percent_timeframe].where(df_plot[selected_percent_timeframe] > 0, 0)
        df_plot['Turun'] = df_plot[selected_percent_timeframe].where(df_plot[selected_percent_timeframe] < 0, 0)
        
        if sort_values == 'Ya':
            df_plot = df_plot.sort_values(by=selected_percent_timeframe)
            
        st.bar_chart(
            df_plot[['Naik', 'Turun']],
            color=['#00D084', '#FF4B4B']
        )

    with tab3:
        st.subheader('Distribusi Kapitalisasi Pasar')
        market_cap_col = f'Kapitalisasi Pasar ({currency_price_unit})'
        pie_df = df_coins[['Simbol', market_cap_col]].copy()
        pie_df[market_cap_col] = pd.to_numeric(pie_df[market_cap_col])

        fig = px.pie(pie_df, values=market_cap_col, names='Simbol',
                     title='Dominasi Pasar dari Koin Pilihan', hole=.3)
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)

else:
    st.warning("Gagal memuat data. Periksa koneksi internet Anda atau coba lagi nanti.")