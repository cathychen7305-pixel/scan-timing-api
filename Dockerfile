FROM python:3.12-slim AS runtime
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py timing.py ./
USER 65534
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM runtime AS test
USER root
COPY requirements-test.txt .
RUN pip install --no-cache-dir -r requirements-test.txt
COPY test_api.py .
USER 65534
CMD ["python", "-m", "pytest", "-q", "-p", "no:cacheprovider"]

FROM runtime AS release
