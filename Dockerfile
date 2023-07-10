FROM public.ecr.aws/lambda/python:3.10

RUN yum install -y cairo

COPY requirements.txt  .
RUN  pip3 install --upgrade pip
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

COPY app.py ${LAMBDA_TASK_ROOT}

RUN chmod +x ${LAMBDA_TASK_ROOT}/app.py

CMD [ "app.lambda_handler" ]
