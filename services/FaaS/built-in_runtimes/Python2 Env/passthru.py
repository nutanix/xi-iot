import logging

# Python function are invoked with context and message payload.
# The context can be used to retrieve metadata about the message and allows
# function to send mesagges to next stage in stream. In this sample we just
# log message payload and forward it as is to next stage.
def main(ctx, msg):
        logging.info(msg)
        ctx.send(msg)
