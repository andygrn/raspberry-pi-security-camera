
# Security Camera Web GUI
# @andygrn 2015

# ----- OPTIONS -----

directory_output_full = '/home/pi/securitycam/full'
directory_output_thumbs = '/home/pi/securitycam/thumbs'

debug_mode = False

# -------------------

from flask import Flask, render_template, make_response, request, redirect, url_for
import os
import fnmatch
import subprocess

app = Flask( __name__, template_folder = 'templates' )
app.debug = debug_mode

if app.debug:
	from werkzeug.debug import DebuggedApplication
	app.wsgi_app = DebuggedApplication( app.wsgi_app, True )

def getImageList():
	image_list = []
	for filename in os.listdir( directory_output_full ):
		if fnmatch.fnmatch( filename, '*.jpg' ):
			image_list.append( filename )
	return sorted( image_list, reverse = True )

def isCameraOnline():
	result = subprocess.check_output( './get_cam_status.sh' ).strip()
	return ( int( result ) > 0 )

@app.route( '/' )
def index():
	"""Display the webcam control panel."""
	response = make_response( render_template( 'security.html', images = getImageList(), online = isCameraOnline() ) )
	response.headers['Cache-Control'] = 'no-cache'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response

@app.route( '/delete', methods = ['POST'] )
def deleteImages():
	"""Delete selected webcam images."""
	if request.form.has_key( 'filenames' ):
		for filename in request.form.getlist( 'filenames' ):
			file_path = directory_output_full + '/' + filename
			if os.path.isfile( file_path ):
				os.remove( file_path )
			file_path_thumb = directory_output_thumbs + '/' + filename
			if os.path.isfile( file_path_thumb ):
				os.remove( file_path_thumb )
	return redirect( url_for( 'index' ) )

if __name__ == '__main__':
	app.run( host = '0.0.0.0', port = 8888 )
