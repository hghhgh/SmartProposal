# Dockerfile برای فرانت‌اند React
FROM node:18-alpine

WORKDIR /app

# کپی package files
COPY package*.json ./

# نصب وابستگی‌ها
RUN npm install

# کپی کد برنامه
COPY . .

# پورت پیش‌فرض
EXPOSE 3000

# اجرای برنامه در حالت توسعه
CMD ["npm", "start"]




