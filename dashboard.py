import streamlit as st
import boto3
import pandas as pd


st.set_page_config(page_title="İHA Telemetri Paneli", layout="wide")
st.title("🚁 İHA Gerçek Zamanlı Telemetri Paneli")
st.markdown("Bu panel, simülasyondan üretilip AWS DynamoDB'ye kaydedilen verileri anlık olarak çeker.")

#aws bağlantısı 
AWS_REGION = 'us-east-1' 
dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)
table = dynamodb.Table('DroneData')

#veri çekme fonksiyonu
def load_data():
    # DynamoDB'den tüm verileri tara ve getir
    response = table.scan()
    items = response.get('Items', [])
    
    if not items:
        return pd.DataFrame() # Veri yoksa boş tablo dön
    
    # Verileri Pandas tablosuna çevir ve zamana göre sırala
    df = pd.DataFrame(items)
    df = df.sort_values(by='timestamp', ascending=True)
    
    # DynamoDB'den gelen Decimal (Ondalıklı) sayıları Streamlit'in çizebilmesi için float'a çevir
    df['altitude'] = df['altitude'].astype(float)
    df['speed'] = df['speed'].astype(float)
    df['battery_level'] = df['battery_level'].astype(float)
    df['lat'] = df['latitude'].astype(float)
    df['lon'] = df['longitude'].astype(float)
    
    return df

#yenileme butonu
if st.button("🔄 Verileri Yenile"):
    st.toast("Veriler AWS'den çekiliyor...", icon="⏳")

# Verileri yükle
df = load_data()

#ekran çizimi
if df.empty:
    st.warning("⚠️ Veritabanında henüz veri bulunmuyor. Lütfen Python simülasyonunu (drone_sim.py) çalıştırın.")
else:
    # En güncel veriyi alma
    latest_data = df.iloc[-1]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Kimlik (Drone ID)", latest_data['drone_id'])
    col2.metric("Güncel İrtifa", f"{latest_data['altitude']:.2f} m")
    col3.metric("Güncel Hız", f"{latest_data['speed']:.2f} km/h")
    col4.metric("Batarya", f"% {latest_data['battery_level']:.2f}")

    st.divider()

    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📈 İrtifa Değişimi (m)")
        st.line_chart(df.set_index('timestamp')['altitude'], color="#FF4B4B")

    with col_chart2:
        st.subheader("🚀 Hız Değişimi (km/h)")
        st.line_chart(df.set_index('timestamp')['speed'], color="#0068C9")
        
    st.divider()
    
    st.subheader("📍 İHA Konum Geçmişi")
    st.markdown("İHA'nın simüle edilen uçuş rotası (Türkiye Koordinatları):")
    st.map(df[['lat', 'lon']], zoom=5)