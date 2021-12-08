FROM public.ecr.aws/lambda/python:3.8

WORKDIR /utilities/aws

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

WORKDIR /utilities/messaging

RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

WORKDIR /

COPY main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.main" ]