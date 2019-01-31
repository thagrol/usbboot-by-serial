# This is a proof of concept. It is by no means ready for production use.

## Requirements
* A Raspberry Pi running Raspbian Stretch
* Python 2
* RPF's rpiboot utility
* One, or more, Raspberry Pi zero/zeroW (A and A+ should work too)
* USB A to micro-B cable for each Pi zero (A male to A male for A/A+)

## Instalation
1. Ensure rpiboot is installed:
```
sudo apt update
sudo apt install rpiboot
```
2. Download this repository
3. Copy or link it to `/srv/usbboot`
4. Install udev rules:
```
sudo cp /srv/usbboot/udev/10-rpiboot.rules /etc/udev/rules.d
sudo udevadm control --reload-rules
```
5. Set up first stage boot files:
```
sudo /srv/usbboot/utils/mklive.sh
```

## Configuration
For each client Pi create a directory `/srv/usbboot/clients/by-serial/<serial number>` and copy the required boot files into it.
For a default file set, create `/srv/usbboot/clients/default` and copy the required boot files into it.

## Usage
Run `sudo rpiboot -l -o -d /srv/usbboot/live`
Connect you client Pi

## Utility Scripts
`usbboot/utils/mklive.sh`: Create links in `usbboot/live` from `usbboot/clients/1ststage`
`usbboot/utils/clnlive.sh`: Remove boot overlay links from `/srv/usbboot/live`
`usbboot/utils/nukelive.sh`: Remove files and links from `/srv/usbboot/live`

## Notes
* Serial number must exactly match that reported by the client Pi including letter case and leading zeros.
* Message are logged to `/srv/usbboot/usbboot.log`
* If you don't know the serial number for a client Pi, connect it then check the log.

## To Do
* Tidy code
* Remove hard coded paths
* Better configuration mechanism for the udev event handler
* Clean up of boot overlays when client disconnected
* Allow for more than one USB bus - needed for non-Pi boot servers

## How It Works
rpiboot sends a modified gpioexpander (https://github.com/raspberrypi/gpioexpander)
The udev event handler reads the serial number of the client Pi, creates the overlay for rpiboot, then sends a `reboot` command over the client's serial port.
rpiboot then serves the files from the overlay.

The additional boot stage is required as the broadcom code built in to the SoC does not expose the Pi's serial number.

## Gpioexpander Modifications
* hostname is now 1stagezero
* pid is now 0xb007
* Only provides a serial gadget
* gpiod is not started
* no gtty is started
* a very basic listen is run on the serial port