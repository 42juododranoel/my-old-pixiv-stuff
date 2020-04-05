FROM python:3.7 AS common

ARG HOST_USER_ID

RUN echo "Europe/Moscow" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    \
    apt -y update && \
    apt -y install gettext && \
    \
    useradd -u ${HOST_USER_ID} -ms /bin/bash user

USER user
ENV PATH=/home/user/.local/bin:$PATH


FROM common AS development

COPY --from=kirisame_django --chown=user /home/user/.cache /home/user/.cache
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --user -r /tmp/requirements.txt

COPY --chown=user application /application
WORKDIR /application


FROM common AS production

COPY --from=development --chown=user /home/user/.cache /home/user/.cache
COPY --from=development --chown=user /tmp/requirements.txt /tmp/requirements.txt
RUN pip3 install --user -r /tmp/requirements.txt

COPY --chown=user application /application
WORKDIR /application
