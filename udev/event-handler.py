#!/usr/bin/env python

"""
udev event handler for first stage USB boot of Pi zero/zeroW/A/A+

workaround to allow sending code based on Pi's serial number.
Needs rpiboot 20171023~154601 or later
"""

## imports
import logging
import os


## functions
def sendcmd(dev, cmd):
    os.system('stty -F %s speed 9600' % dev)
    with open(dev, 'w') as tty:
        tty.write('%s\n' % cmd)
##    os.system('echo %s > %s', (tty, cmd))


## constants
#    should really be taking BASEPATH, DEFAULTCLIENT, and LOGFILE
#    from the command line or a config file
BASEPATH = '/srv/usbboot'
LIVEPATH = os.path.join(BASEPATH, 'live')
CLIENTBASE = os.path.join(BASEPATH, 'clients/by-serial')
DEFAULTCLIENT = os.path.join(BASEPATH, 'clients/default')
LOGFILE = os.path.join(BASEPATH, 'usbboot.log')


## setup logging
logging.basicConfig(filename=LOGFILE,
##                    level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

try:
    ## get env variables
##    logging.debug(os.environ)
    # effectively constants so uppercased
    ACTION = os.getenv('ACTION')
    SERIAL = os.getenv('ID_SERIAL_SHORT')
    DEVPATH = os.getenv('DEVPATH')
    DEVNAME = os.getenv('DEVNAME')

    logging.debug('%s\t%s\t%s\t%s' % (ACTION, SERIAL, DEVPATH, DEVNAME))

    if ACTION == 'add':
        # it's an add action from udev
        overlayname = os.path.basename(DEVPATH.split(':')[0])
        linktarget = os.path.join(CLIENTBASE, SERIAL)
        linkto = os.path.join(LIVEPATH, overlayname)
##        logging.debug('overlayname: %s' % overlayname)
##        logging.debug('linktarget: %s' % linktarget)
##        logging.debug('link to: %s' % linkto)
##        logging.debug('DEFAULTCLIENT: %s' % DEFAULTCLIENT)
        if os.path.isdir(linktarget):
            os.symlink(linktarget, linkto)
            logging.info('Created boot overlay for %s.'
                         % SERIAL)
            sendcmd(DEVNAME, 'reboot')
        elif os.path.isdir(DEFAULTCLIENT):
            os.symlink(DEFAULTCLIENT, linkto)
            logging.info('Created default boot overlay for %s.'
                         % SERIAL)
            sendcmd(DEVNAME, 'reboot')
        else:
            logging.error('Unable to find client for %s and no default present. Sending poweroff.'
                          % SERIAL)
            sendcmd(DEVNAME, 'poweroff')
except:
    logging.exception('Exiting due to exception: ')
    raise
