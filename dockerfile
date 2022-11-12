FROM rabbitmq:3.7.18-management
COPY ./rabbitmq_delayed_message_exchange-20171201-3.7.x.ez /opt/rabbitmq/plugins/
RUN rabbitmq-plugins enable rabbitmq_delayed_message_exchange