FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY services/api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && groupadd --gid 10001 lsk && useradd --uid 10001 --gid 10001 --no-create-home --shell /usr/sbin/nologin lsk
COPY --chown=10001:10001 services/api/app ./app
COPY --chown=10001:10001 services/api/tests ./tests
USER 10001:10001
EXPOSE 18474
CMD ["uvicorn","app.entrypoint:app","--host","0.0.0.0","--port","18474"]
