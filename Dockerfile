FROM python:3.10-slim

# ติดตั้ง dependencies ที่จำเป็นสำหรับ pandas, numpy และระบบแสดงผล (optional)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# ตั้ง working directory
WORKDIR /app

# คัดลอกไฟล์ requirements และติดตั้ง package
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกโค้ดทั้งหมดเข้าไปใน container
COPY . .

# เปิด port 8000 ให้ container
EXPOSE 8000

# คำสั่งเริ่มรันแอป FastAPI ผ่าน uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]