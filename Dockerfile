FROM python:3.6


COPY requirements.txt /
RUN pip install -r requirements.txt

ADD . /app
COPY . /app

WORKDIR /app
	
ENV NAME World

ENV PYTHONPATH "${PYTHONPATH}:/elecsim"

ENTRYPOINT ["python", "test/test_model/test_world.py"]

CMD ["python", "test/test_model/test_world.py"]



