#!/usr/bin/env python3

import psutil
from subprocess import call

allowed_devices = ["sdb", "sdc", "sdd", "sde", "sdf", "sdg", "sdh", "sdi", "sdj", "sdk"]


def getDisks():
    paths = []
    partitions = psutil.disk_partitions()
    for p in partitions:
        if p.device.startswith("/dev/sd"):
            path = p.device[:-1]
            lbl = path.split("/")[-1]
            if lbl in allowed_devices and path not in paths:
                print("found {}".format(path))
                paths.append(path)
    return paths


def umount(device):
    if isinstance(device, list):
        for d in device:
            umount(d)
        return True
    try:
        call("umount {}".format(device), shell=True)
    except:
        pass


def copyToSD(img_file, device):
    if isinstance(device, list):
        # multi device imaging
        devices = " ".join(["of={}".format(a) for a in device])
        cmd = 'bash -c "gzip -d -c {}" | pv | dcfldd {}'.format(img_file, devices)
        print(cmd)
        call(cmd, shell=True)
        return True

    # single image
    cmd = 'bash -c "gzip -d -c {}" | pv | dd of={} bs=5M'.format(img_file, device)
    print(cmd)
    call(cmd, shell=True)


def magicImager(img_file):
    devices = getDisks()
    if len(devices) == 0:
        print("no sd cards found")
        return False
    if len(devices) == 1:
        devices = devices[0]
    umount(devices)
    copyToSD(img_file, devices)


import sys


def main():
    if len(sys.argv) < 2:
        print("requires disk image path\n\tsdcardforger.py disk.img")
    magicImager(sys.argv[1])


if __name__ == "__main__":
    main()
