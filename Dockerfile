FROM python:3.13-slim AS runtime

WORKDIR /app

COPY src/ /app/
COPY test/test_data /app/test_data

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FORCE_COLOR=1


ENTRYPOINT ["python", "-m", "lockdiff"]
CMD ["-h"]
