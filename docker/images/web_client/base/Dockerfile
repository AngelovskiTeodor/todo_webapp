FROM node:19-alpine as base

# Set the env to "production" or "development"
ENV NODE_ENV development

# Setting up the work directory
WORKDIR /web-client-react

# Installing dependencies  
# Must build from parrent directory because "../" is not working
COPY ./client/web-client-react/package.json /web-client-react
RUN npm install