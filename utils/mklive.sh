#!/bin/bash

case $(basename "$0") in
    "nukelive.sh")
        echo Removing files and links from /srv/usbboot/live. Subdirectories may not be removed
        rm /srv/usbboot/live/*
        ;;
    "mklive.sh")
        echo Linking first stage boot files to /srv/usbboot/live
        SOURCE=/srv/usbboot/clients/1ststage/
        DEST=/srv/usbboot/live/
        find $SOURCE -maxdepth 1 -mindepth 1 -name \* -exec ln -sf {} $DEST \;
        ;;
    "clnlive.sh")
        echo Removing boot overlay links from /srv/usbboot/live. Physical directories and hard links may not be removed.
        find /srv/usbboot/live -maxdepth 1 -mindepth 1 -name 1-\* -type l -delete
esac

