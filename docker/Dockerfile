FROM python:3.9

WORKDIR /FileStore/indeed

COPY filestore/landing  /FileStore/indeed/landing
COPY filestore/gold  /FileStore/indeed/gold
COPY filestore/config.yml  /FileStore/indeed/config.yml

COPY dist/* /workspace/
RUN pip install /workspace/*.whl && rm /workspace/*.whl

RUN python -m indeed.tests
CMD ["/bin/bash"]