import json
import time
import random
from datetime import datetime, timezone
import boto3

AWS_REGION = 'us-east-1' 

STREAM_NAME = 'DroneTelemetryStream'

kinesis_client = boto3.client('kinesis', region_name=AWS_REGION) 

def generate_drone_data(drone_id):
    """Rastgele drone telemetri verisi üretir."""
    return {
        'drone_id': drone_id,
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'altitude': round(random.uniform(100.0, 500.0), 2),      
        'speed': round(random.uniform(0.0, 80.0), 2),            
        'battery_level': round(random.uniform(10.0, 100.0), 2),  
        'latitude': round(random.uniform(38.0, 42.0), 6),        
        'longitude': round(random.uniform(26.0, 45.0), 6)        
    }

print(f"Bulut bağlantısı kuruluyor... Bölge: {AWS_REGION}, Kanal: {STREAM_NAME}\n")

try:
    while True:
        payload = generate_drone_data("UAV-ANKARA-01")
        
        response = kinesis_client.put_record(
            StreamName=STREAM_NAME,
            Data=json.dumps(payload),
            PartitionKey=payload['drone_id']
        )
        
        print(f"[BAŞARILI] Hız: {payload['speed']} km/h, İrtifa: {payload['altitude']}m --> Shard ID: {response['ShardId']}")
        
        time.sleep(2)
        
except KeyboardInterrupt:
    print("\nSimülasyon durduruldu.")
except Exception as e:
    print(f"\n[HATA] Bir sorun oluştu: {e}")