import requests

def get_my_ip():
 try:
  # ยิง request ไปยัง api เพื่อดึง IP 
  response = requests.get('https://api.ipify.org?format=json')
  
  # ตรวจสอบว่าสถานะการตอบกลับเป็น 200 (OK)
  if response.status_code == 200:
   ip_data = response.json()
   return ip_data['ip']
  else:
   return "ไม่สามารถดึง IP ได้"
 except Exception as e:
  return f"เกิดข้อผิดพลาด: {e}"
 
if __name__ == "__main__":
 print("--- My IP Checker Program ---")
 ip = get_my_ip()
 print(f"My Public IP Address is: {ip}")
  