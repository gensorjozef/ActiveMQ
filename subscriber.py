import time
import sys
import stomp
import ssl


class MsgListener(stomp.ConnectionListener):
    def on_error(self, message):
        print('received an error "%s"' % message.body)

    def on_message(self, frame):
        print('received a message "%s"' % frame.body)


# Rozdiel medzi topic a queue spocita v tom ze pri topic musi byt subscriber pripojeny a cakat na spravu zato pri
# fronte(queue) publisher spravu odosle do fronty s tym, ze sprava je v nej ulozena dokym sa consument nepripoji(
# PUSH-PULL)

# destination = "/topic/topic-1"
destination = "/queue/queue-1"

conn = stomp.Connection()
conn.set_listener('stomp_listener', MsgListener())

conn.connect("admin", "admin", wait=True, headers={'client-id': 'jgensor'})

conn.subscribe(id='simple_listener', destination=destination, ack='auto')

print("Waiting for messages...")

time.sleep(320)
conn.disconnect()
