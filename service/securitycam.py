
# Security Camera Service
# @andygrn 2015

# ----- OPTIONS -----

directory_output_full = '/home/pi/securitycam/full'
directory_output_thumbs = '/home/pi/securitycam/thumbs'

camera_resolution = ( 1024, 768 )
camera_exposure_compensation = 2
camera_rotation = 0

# A number between 0 and 1. The lower the number, the more sensitive the motion detection.
# This number is pretty arbitrary - just play around until it captures only what you need.
motion_detection_threshold = 0.18

# The number of seconds between detection checks, if you don't want to thrash your Pi too hard.
# The image capture and analysis does take a second or so, so 0 doesn't mean constant monitoring.
motion_detection_interval = 0

# A number between 0 and 1. A photo with a brightness value lower than this will put the camera to sleep for 10 mins.
# Helps to save power at night time.
minimum_brightness = 0.15

# -------------------

import time
import atexit
import picamera
import logging
import io
import imagehelpers
from PIL import Image

logging.basicConfig( level = logging.WARNING )
logger = logging.getLogger( __name__ )

camera = picamera.PiCamera()
camera.resolution = camera_resolution
camera.exposure_compensation = camera_exposure_compensation
camera.rotation = camera_rotation
time.sleep( 2 ) # Camera warmup.

def cleanUp():
	logger.info( 'Cleaning up...' )
	camera.close()

atexit.register( cleanUp )

logger.info( 'Starting security camera...' )

image_previous_stream = io.BytesIO()
camera.capture( image_previous_stream, format = 'jpeg' )
image_previous = Image.open( image_previous_stream )

image_current_stream = io.BytesIO()

previous_loop_start_time = time.time()

while True:
	# Limit the loop to one photo per `motion_detection_interval` seconds.
	previous_loop_total_time = time.time() - previous_loop_start_time
	sleep_time = motion_detection_interval - previous_loop_total_time
	if sleep_time > 0:
		time.sleep( sleep_time )
	previous_loop_start_time = time.time()
	logger.info( 'Taking snapshot... ({0})'.format( time.strftime( '%Y-%m-%d_%H-%M-%S' ) ) )

	camera.capture( image_current_stream, format = 'jpeg' )
	image_current = Image.open( image_current_stream )
	image_current_stream = io.BytesIO() # Reset the current image stream.

	image_brightness = imagehelpers.getBrightness( image_current )
	if image_brightness < minimum_brightness:
		logger.info( 'Too dark ({0})! Sleeping... ({1})'.format( image_brightness, time.strftime( '%Y-%m-%d_%H-%M-%S' ) ) )
		time.sleep( 600 )
		continue

	# Compare previous image with latest image; if they are too similar, discard the latest image!
	similarity_score = imagehelpers.diff( image_previous, image_current, save_debug_image = False )
	score_above_threshold = ( similarity_score > motion_detection_threshold )
	image_previous = image_current # Set the latest image as our new base image.
	if not score_above_threshold:
		logger.info( 'Too similar ({0})! Sleeping... ({1})'.format( similarity_score, time.strftime( '%Y-%m-%d_%H-%M-%S' ) ) )
		continue
	logger.info( 'Score above threshold: {0}'.format( similarity_score ) )

	# Images didn't match - capture the scene!
	new_file_name = time.strftime( '%Y-%m-%d_%H-%M-%S' ) + '.jpg'
	image_current.save( directory_output_full + '/' + new_file_name, format = 'jpeg', exif = image_current.info.get( 'exif' ) )
	image_current.resize( ( 440, 330 ) ).save( directory_output_thumbs + '/' + new_file_name, format = 'jpeg' )
	logger.info( 'Captured {0}'.format( new_file_name ) )
