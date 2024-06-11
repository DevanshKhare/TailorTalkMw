FROM python:3

WORKDIR /app

COPY ./requirements.txt ./
COPY . .

RUN apt-get update && apt-get install -y libgl1-mesa-glx
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "app.py"]