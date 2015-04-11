
# Raspberry Pi Security Camera + Web GUI

For [Raspberry Pi Camera Module](https://www.raspberrypi.org/products/camera-module/) and Python 3.


## `/service`

A python script that saves images when motion is detected. The motion detection is basic, but efficient.

By default, the contents of this folder belong in `/usr/local/bin/securitycam`, except the daemon script `securitycam` which belongs in `/etc/init.d`.

There are a few configuration settings in `securitycam.py` (make sure the output directories exist and are writable). If you are feeling more adventurous, you can tweak the detection settings further (look at the functions in imagehelpers.py).

Start the service with `sudo /etc/init.d/securitycam start`, stop it with `sudo /etc/init.d/securitycam stop`. If the service doesn't want to stay running, check `/usr/local/bin/securitycam/daemon.log` for debugging info. Don't forget to `sudo update-rc.d securitycam defaults` if you want the service to automatically start on reboot.

### Required Packages

- picamera
- pillow


## `/web_gui`

A minimal python Flask app to review and delete captured images.

By default, the contents of this folder belong in `/var/www/securitycam`. I recommend running it through uWSGI + nginx/apache, but it can be tested with `python3 /var/www/securitycam/securitycam_gui.py` if you adjust some of the image paths in the templates.

There are some settings in `securitycam_gui.py`; make sure the output directories exist and are readable.

### Required Packages

- flask
