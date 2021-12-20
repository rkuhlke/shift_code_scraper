FROM public.ecr.aws/lambda/python:3.8

COPY . .

RUN python3 -m pip install --upgrade pip

WORKDIR /utilities/aws/
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

WORKDIR /utilities/messaging/
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

WORKDIR /

COPY main.py ${LAMBDA_TASK_ROOT}

CMD [ "main.main" ]