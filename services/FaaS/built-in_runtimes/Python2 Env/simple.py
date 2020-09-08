import logging

# Python function are invoked with context and message payload.
# The context can be used to retrieve metadata about the message and allows
# function to send mesagges to next stage in stream. In this sample we just
# log message payload and forward it as is to next stage.
def main(ctx, msg):
        logging.info("Parameters: %s", ctx.get_config())
        logging.info("Process %d bytes from %s at %s", len(msg), ctx.get_topic(), ctx.get_timestamp())
        # Forward to next stage in pipeline.
        ctx.send(msg)
