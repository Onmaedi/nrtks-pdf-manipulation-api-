# Use the Nginx image
FROM nginx

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf
ADD ./default.conf /etc/nginx/conf.d/000-default.conf

# Replace with our own nginx.conf
# COPY nginx.conf /etc/nginx/conf.d/