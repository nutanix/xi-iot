import logging

# Transformation can send more messages than they receive. 
def main(ctx, msg):
        logging.info("Process %d bytes from %s at %s", len(msg), ctx.get_topic(), ctx.get_timestamp())
        m = len(msg) / 2
        # split message in two halves
        ctx.send(msg[:m])
        ctx.send(msg[m:])
