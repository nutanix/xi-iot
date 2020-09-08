import logging

counter=0

def main(ctx, msg):
        global counter
        logging.info("This is message number %d", counter)
        counter+=1
        # Forward to next stage in pipeline.
        ctx.send(msg)
