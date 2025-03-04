FROM python:3.10-slim
ENV WORKDIR /WORK
WORKDIR $WORKDIR

COPY . .
RUN pip install --no-cache-dir -r ./requirements.txt
RUN apt update -y && apt install curl git -y
RUN curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin
