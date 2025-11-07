ARG PYTHON_VERSION=3.12
ARG VARIANT=slim-bookworm
FROM docker.io/python:${PYTHON_VERSION}-{VARIANT}

LABEL maintainer="LSEG Developer Relations"

COPY requirements.txt .

# install dependencies to the local user directory (eg. /root/.local)
#RUN pip install --upgrade pip && \
#    pip install --no-cache-dir --user -r requirements.txt
RUN pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --no-cache-dir --upgrade pip && \
    pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --no-cache-dir --no-warn-script-location --user -r requirements.txt

WORKDIR /app

# Update PATH environment variable + set Python buffer to make Docker print every message instantly.
ENV PATH=/root/.local:$PATH \
    PYTHONUNBUFFERED=1\
    PYTHONIOENCODING=utf-8\
    PYTHONLEGACYWINDOWSSTDIO=utf-8
#Copy application files
COPY ["ld_app.py", "lseg-data.config.json", "/app/"]

#Run Python
ENTRYPOINT ["python", "/app/ld_app.py"]