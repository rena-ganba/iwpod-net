import numpy as np
from src.keras_utils import load_model
import cv2
from src.keras_utils import  detect_lp_width
from src.utils 					import  im2single
from src.drawing_utils			import draw_losangle



if __name__ == '__main__':

	#
	#  Parameters of the method
	#
	lp_threshold = 0.35 # detection threshold
	ocr_input_size = [80, 240] # desired LP size (width x height)
	
	#
	#  Loads network and weights
	#
	iwpod_net = load_model('weights/iwpod_net')
	

	#
	#  Loads image with vehicle crop or full image with vehicle(s) roughly framed.
	#  You can use your favorite object detector here (a fine-tuned version of Yolo-v3 was
	#  used in the paper)
	#
	
	#
	#  Also inform the vehicle type:
	#  'car', 'bus', 'truck' 
	#  'bike' 
	#  'fullimage' 
	#
	#

	Ivehicle = cv2.imread('images\\example_fullimage.jpg')
#	Ivehicle = cv2.imread('images\\brasil7.jpg')
	iwh = np.array(Ivehicle.shape[1::-1],dtype=float).reshape((2,1))
	vtype = 'fullimage' # indicates vehicle type (typically comes from the vehicle detector)

	if (vtype in ['car', 'bus', 'truck']):
		#
		#  Defines crops for car, bus, truck based on input aspect ratio (see paper)
		#
		ASPECTRATIO = max(1, min(2.75, 1.0*Ivehicle.shape[1]/Ivehicle.shape[0]))  # width over height
		WPODResolution = 256# faster execution
		lp_output_resolution = tuple(ocr_input_size[::-1])

	elif  vtype == 'fullimage':
		#
		#  Defines crop if vehicles were not cropped 
		#
		ASPECTRATIO = 1 
		WPODResolution = 480 # larger if full image is used directly
		lp_output_resolution =  tuple(ocr_input_size[::-1])
	else:
		#
		#  Defines crop for motorbike  
		#
		ASPECTRATIO = 1.0 # width over height
		WPODResolution = 208
		lp_output_resolution = (int(1.5*ocr_input_size[0]), ocr_input_size[0]) # for bikes, the LP aspect ratio is lower

	#
	#  Runs IWPOD-NET. Returns list of LP data and cropped LP images
	#
	Llp, LlpImgs,_ = detect_lp_width(iwpod_net, im2single(Ivehicle), WPODResolution*ASPECTRATIO, 2**4, lp_output_resolution, lp_threshold)
	for i, img in enumerate(LlpImgs):
		pts = Llp[i].pts * iwh
		draw_losangle(Ivehicle, pts, color = (0,0,255.), thickness = 2)
		cv2.imshow('Rectified plate %d'%i, img )
	cv2.imshow('Image and LPs', Ivehicle )
	cv2.waitKey()
	cv2.destroyAllWindows()
	

 

