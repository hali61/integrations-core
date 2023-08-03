ARG RAY_VERSION

FROM rayproject/ray-ml:${RAY_VERSION}-cpu

COPY main.py /home/ray/main.py

CMD ["python", "/home/ray/main.py"]