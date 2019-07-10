#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from threading import Thread
import time
from simulation import Environment

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync






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
    fps = 60
    env_playground = Environment(fps)
    
   
    while True:
        time.sleep(1/fps)
        channel_layer = get_channel_layer()
        env_playground.update()
        async_to_sync(channel_layer.group_send)("connected_users", {"type": "receive_data", "data" :env_playground.send_update()})
        
    

if __name__ == '__main__':
    foo()
    main()
   

    

