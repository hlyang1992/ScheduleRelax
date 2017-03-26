#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from time import sleep
from datetime import datetime

class MonitorStatus:
    def __init__(self, mouseId, keyboardId, 
            interval=1, max_on_time=10, max_off_time=5, 
            sleep_time="23:30", debug = True):
        """
        mouseId: the device ID of mouse, can get using 'xinput list'
        keyboardId: the device ID of keyboard
        interval: change monitor status of every this time
        max_on_time: the time which monitor is on
        max_off_time: the time which monitor if off
        the unit of time is second.
        """
        self.interval = interval
        self.max_on_time = max_on_time  
        self.max_off_time = max_off_time
        self.mouseId = mouseId
        self.keyboardId = keyboardId
        tmp = [int(i) for i in sleep_time.split(":")]
        self.sleep_time = tmp[0] + tmp[1] / 60 

        self.status = self.check_status()
        self.debug = debug
        self.monitor_on_time = 0
        self.monitor_off_time = 0

    def __iter__(self):
        return self

    def __next__(self):
        # if computer if idle, sleep longer and enable mouse and keyboard
        if self.idle_time() > self.interval*3:
            self.change_monitor_status(status=0)
            self.change_xinput_status(self.mouseId)
            self.change_xinput_status(self.keyboardId)
            self.monitor_off_time = self.monitor_on_time = 0
            sleep(self.interval*3)
            return self.idle_time()

        now_time = datetime.now().hour + datetime.now().minute / 60
        sleep_con = now_time > self.sleep_time or now_time < 5.0
        # MUST GO TO BED, DISABLE EVERYTHING!
        if sleep_con:
            self.change_monitor_status(status=0, mouse = False, keyboard = False)
            self.monitor_off_time = self.monitor_on_time = 0
            sleep(self.interval*3)
            return self.idle_time()

        self.status = self.check_status()
        on_condition = self.monitor_on_time < self.max_on_time
        off_condition = self.monitor_off_time < self.max_off_time

        interval = self.interval if self.status and on_condition else 1

        if self.status: # monitor is on
            if on_condition: # if monitor should on, sleep
                self.monitor_on_time += interval
                sleep(interval)
            elif not on_condition: # should start relax
                self.monitor_off_time = 0
                self.change_monitor_status(status = 0, mouse=self.debug, keyboard=self.debug)
            elif off_condition:
                self.change_monitor_status(status = 1, mouse=self.debug, keyboard=self.debug)
                self.monitor_off_time += interval
                sleep(interval)
        else: # monitor is off
            if off_condition:
                self.monitor_off_time += interval
                sleep(interval)
            else:
                self.monitor_on_time = 0
                self.change_monitor_status(status = 1, mouse=self.debug, keyboard=self.debug)
        print("status: {}\n monitor_on_time: {}\n monitor_off_time: {}\n"
                .format(self.status, self.monitor_on_time, self.monitor_off_time))
        return self.status
    
    def change_monitor_status(self, status, mouse = True, keyboard = True):
        """
        close monitor if status = 1
        disable mouse if status = and mouse = False
        disable keyboard if status = and keyboard = False
        """
        monitor_status = 'on' if status else 'off'
        mouse_status = 1 if status else 0
        keyboard_status = 1 if status else 0
        cmd = ['xset', 'dpms', 'force', monitor_status]

        if not mouse:
            self.change_xinput_status(self.mouseId, mouse_status)
        if not keyboard:
            self.change_xinput_status(self.keyboardId, keyboard_status)
        subprocess.run(cmd, stdout=subprocess.PIPE)

    @staticmethod
    def check_status():
        """
        check status of monitor, return True if monitor is no else False.
        """
        cmd = ['xset', 'q']
        result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        for line in result.split("\n"):
            if "Monitor" in line:
                return True if "On" in line else False

    @staticmethod
    def idle_time():
        """
        return user's idle time in seconds.
        """
        cmd = ['xprintidle']
        result = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode('utf-8')
        return int(result) / 1000

    @staticmethod
    def change_xinput_status(deviceId, status=1):
        """
        disable or enable mouse or keyboard
        """
        cmd = ['xinput', 'set-prop', str(deviceId), 'Device Enabled', str(status)]
        subprocess.run(cmd, stdout=subprocess.PIPE)

def main(debug=True):
    mouseId = 9 
    # keyboardId = mouseId
    keyboardId = 10

    # the unit of time is second.
    # change monitor status of every this time
    interval = 60*10
    work_time = 60*50
    relax_time = 60*5
    sleep_time = "23:30"
    # interval = 0.5
    # work_time = 10
    # relax_time = 10
    monitor = MonitorStatus(mouseId=mouseId, 
                        keyboardId=keyboardId, 
                        interval = interval, 
                        max_on_time = work_time,
                        max_off_time = relax_time,
                        sleep_time = sleep_time,
                        debug=debug)
    for _ in monitor:
        pass

if __name__ == "__main__":
    # don't disable mouse and keyboard, if debug is True
    debug = False 
    main(debug)
