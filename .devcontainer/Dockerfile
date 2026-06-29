FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:1
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y \
    wget curl gnupg2 ca-certificates \
    xvfb x11vnc xdotool scrot \
    openbox \
    novnc websockify \
    python3 python3-pip \
    xterm fonts-liberation fonts-noto-core \
    libxss1 libnss3 libatk-bridge2.0-0 libgtk-3-0 \
    libgbm1 libasound2 \
    libvulkan1 xdg-utils \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Google Chrome (includes Widevine for Netflix/Disney+)
RUN apt-get update \
    && wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /opt/desktop/requirements.txt
RUN pip3 install --no-cache-dir -r /opt/desktop/requirements.txt

COPY api.py /opt/desktop/api.py
COPY restore-state.py /opt/desktop/restore-state.py
COPY start.sh /opt/desktop/start.sh
RUN chmod +x /opt/desktop/start.sh

EXPOSE 6080 8080
