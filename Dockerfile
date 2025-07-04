FROM node:18

RUN apt-get update && apt-get install -y python3 python3-pip

WORKDIR /app

COPY package*.json ./
RUN npm install

# Copia as pastas que têm código Python (ex: controllers e scripts)
COPY controllers ./controllers
COPY scripts ./scripts

# Copia o restante do código
COPY . .

# Instala as dependências Python
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["node", "app.js"]
