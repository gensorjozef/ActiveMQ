import time
import stomp

# Rozdiel medzi topic a queue spocita v tom ze pri topic musi byt subscriber pripojeny a cakat na spravu zato pri
# fronte(queue) publisher spravu odosle do fronty s tym, ze sprava je v nej ulozena dokym sa consument nepripoji(
# PUSH-PULL)

# destination = "/topic/topic-1"
destination = "/queue/queue-1"

MESSAGES = 10

conn = stomp.Connection()
conn.connect(login="admin", passcode="admin")

for i in range(0, MESSAGES):
    message = "This is message number #{i}!".format(i=i)
    conn.send(destination, message, persistent='true')

conn.disconnect()
