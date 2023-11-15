FROM python:3.11-slim
RUN apt-get update && apt-get -y install time python3-pip git
COPY run.sh /


RUN mkdir /workspace

RUN git clone --depth 1 --branch v3.3.5 https://github.com/androguard/androguard.git /workspace/androguard
RUN sed -i '396i\\    print("ee3d6c7015b83b3dc84b21a2e79506175f07c00ecf03e7b3b8edea4e445618bd: END OF ANALYSIS.")' /workspace/androguard/androguard/cli/entry_points.py && \
    python3 -m pip install -e /workspace/androguard
