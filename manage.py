#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from threading import Thread
import pusher
import time
from simulation import Environment


pusher_client = pusher.Pusher(
  app_id='816618',
  key='d31544dff3c77506346e',
  secret='abcdc31eb34b60ae065f',
  cluster='us2',
  ssl=True
)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sim_creatures.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator

@start_new_thread
def foo():
    #init the simulation
    env_playground = Environment()
   
    while True:
        time.sleep(1)
        env_playground.update()
        pusher_client.trigger('my-channel', 'my-event', env_playground.send_update())

if __name__ == '__main__':
    foo()
    main()
   

    

