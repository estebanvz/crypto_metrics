FROM python:3.7.9-slim
RUN pip install numpy==1.18.2
RUN pip install pandas==1.0.4
RUN pip install scipy==1.7.3
RUN pip install bta-lib==1.0.0