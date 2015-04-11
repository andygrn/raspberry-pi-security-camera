
# Security Camera Image Processing Helpers
# @andygrn 2015

from PIL import Image

def diff( image_1, image_2, resolution = 32, difference_threshold = 16, save_debug_image = False ):
	"""
		Return the difference between two PIL Images as a decimal between 0 and 1.
		The sampling occurs every `resolution` pixels, and only differences above `difference_threshold` will count towards the result.
		Enable `save_debug_image` to generate a "debug.jpg" test image with sample points and differences highlighted.
	"""
	if image_1.size != image_2.size:
		return 0.0

	image_1 = image_1.convert( 'L' )
	image_2 = image_2.convert( 'L' )
	image_1_pixels = image_1.load()
	image_2_pixels = image_2.load()

	if save_debug_image:
		debug = Image.blend( image_1, image_2, 0.5 )
		debug = debug.convert( 'RGB' )
		debug_pixels = debug.load()

	total_differences = 0
	for x in range( ( resolution // 2 ), image_1.size[0], resolution ):
		for y in range( ( resolution // 2 ), image_1.size[1], resolution ):
			if ( abs( image_1_pixels[x, y] - image_2_pixels[x, y] ) > difference_threshold ):
				total_differences += 1
				if save_debug_image:
					debug_pixels[x+1, y] = ( 0, 255, 255 )
					debug_pixels[x, y+1] = ( 0, 255, 255 )
					debug_pixels[x-1, y] = ( 0, 255, 255 )
					debug_pixels[x, y-1] = ( 0, 255, 255 )

	if save_debug_image:
		debug.save( 'debug.jpg', quality = 95 )

	return ( total_differences / ( ( image_1.size[0] // resolution ) * ( image_1.size[1] // resolution ) ) )


def getBrightness( image, resolution = 64, brightness_threshold = 16 ):
	"""
		Return a quick-and-dirty brightness level of a PIL Image as a decimal between 0 and 1.
		The sampling occurs every `resolution` pixels, and only levels above `brightness_threshold` will count as "bright".
	"""
	image = image.convert( 'L' )
	image_pixels = image.load()

	total_above_threshold = 0
	for x in range( ( resolution // 2 ), image.size[0], resolution ):
		for y in range( ( resolution // 2 ), image.size[1], resolution ):
			if ( image_pixels[x, y] > brightness_threshold ):
				total_above_threshold += 1

	return ( total_above_threshold / ( ( image.size[0] // resolution ) * ( image.size[1] // resolution ) ) )
