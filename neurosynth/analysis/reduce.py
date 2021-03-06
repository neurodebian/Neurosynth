import numpy as np

""" Dimensional/data reduction methods. """

def average_within_regions(dataset, img, threshold=None, remove_zero=True, replace=False):
	""" Averages over all voxels within each ROI in the input image.

	Takes a Dataset and a Nifti image that defines distinct regions, and 
	returns a numpy matrix of  ROIs x mappables, where the value at each ROI is 
	the proportion of active voxels in that ROI. Each distinct ROI must have a 
	unique value in the image; non-contiguous voxels with the same value will 
	be assigned to the same ROI.

	Args:
		dataset: A Dataset instance
		img: A NIFTI or Analyze-format image that provides the ROI definitions
		threshold: An optional float in the range of 0 - 1. If passed, the array 
			will be binarized, with ROI values above the threshold assigned to True 
			and values below the threshold assigned to False. (E.g., if threshold = 
			0.05, only ROIs in which more than 5% of voxels are active will be 
			considered active.).
		remove_zero: An optional boolean; when True, assume that voxels with value 
		of 0 should not be considered as a separate ROI, and will be ignored. 
		replace: When True, the voxel x mappable array contained within the Dataset's 
			ImageTable will be replaced with the resulting array.

	Returns:
		If replace == True, nothing is returned (the Dataset is modified in-place).
		Otherwise, returns a 2D numpy array with ROIs in rows and mappables in columns.
	"""
	regions = dataset.volume.mask(img)
	labels = np.unique(regions)
	if remove_zero: labels = labels[np.nonzero(labels)]
	n_regions = labels.size
	m = np.zeros((regions.size, n_regions))
	for i in range(n_regions):
		m[regions==labels[i],i] = 1.0/np.sum(regions==labels[i])
	# produces roi x study matrix
	result = np.transpose(m) * dataset.get_image_data(ids=None, dense=False)
	if threshold is not None:
		result[result < threshold] = 0.0
		result = result.astype(bool)
	return result

def random_voxels(dataset, img, n_voxels):
	pass