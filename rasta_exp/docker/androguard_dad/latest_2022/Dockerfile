FROM python:3.11-slim
RUN apt-get update && apt-get -y install time python3-pip git
COPY run.sh /


RUN mkdir /workspace

RUN git init /workspace/androguard && \
    cd /workspace/androguard && \
    git remote add origin https://github.com/androguard/androguard.git && \
    git fetch --depth=1 origin 832104db3eb5dc3cc66b30883fa8ce8712dfa200 && \
    git reset --hard FETCH_HEAD
RUN cd /workspace/androguard && \
    python3 -m pip install -r requirements.txt
