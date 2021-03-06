# ---- Base python ----
FROM python:3.6.1-alpine3.6 as base
# Create app directory
WORKDIR /app

# ---- Dependencies ----
FROM base AS dependencies
RUN apk add --no-cache curl pkgconfig openssl-dev libffi-dev musl-dev make gcc krb5-dev
COPY requirements/requirements.txt ./
# install app dependencies
RUN pip install -r requirements.txt

# ---- Copy Files/Build ----
FROM dependencies AS build
WORKDIR /app
COPY api /app/api
COPY wsgi.py /app/.

# --- Release with Alpine ----
FROM python:3.6.1-alpine3.6 AS release
RUN apk add --no-cache curl pkgconfig openssl-dev libffi-dev musl-dev make gcc krb5-dev
# Create app directory
WORKDIR /app

COPY --from=dependencies /app/requirements.txt ./
COPY --from=dependencies /root/.cache /root/.cache

# Install app dependencies
RUN pip install -r requirements.txt
COPY --from=build /app/ ./

EXPOSE 4003

CMD ["gunicorn", "--bind", "0.0.0.0:4003", "--timeout", "90", "wsgi"]
