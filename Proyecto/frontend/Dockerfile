FROM node:18-alpine

WORKDIR /app

COPY package.json package-lock.json* ./
RUN npm install

COPY . .

EXPOSE 5173

# En producción sustituiríamos esto por npm run build y servir estáticos. 
# Para demostración de MVP mantendremos Vite dev server con enlace 0.0.0.0
CMD ["npm", "run", "dev", "--", "--host"]
