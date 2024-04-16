import numpy as np
from PIL import Image
from skimage import morphology
import pydicom

def read_png(image_path):
    with Image.open(image_path).convert('L') as img:
        array = np.array(img)/255
    return array

def image_x_shift(img, shift_ratio=0.1,crop_ratio=1):
    h, w = img.shape
    new_h, new_w = int(h*crop_ratio), int(w*crop_ratio)
    mid_x, mid_y = w//2, h//2
    shift = int(img.shape[1] * shift_ratio)
    if shift == 0:
        return img
    img_shifted = np.zeros_like(img)
    img_shifted[:, :shift] = img[:, -shift:]
    img_shifted[:, shift:] = img[:, :-shift]
    img_shifted = img_shifted[mid_y-new_h//2:mid_y+new_h//2, mid_x-new_w//2:mid_x+new_w//2]
    return img_shifted
    
def image_y_shift(img, shift_ratio=0.1,crop_ratio=1):
    h, w = img.shape
    new_h, new_w = int(h*crop_ratio), int(w*crop_ratio)
    mid_x, mid_y = w//2, h//2
    shift = int(img.shape[0] * shift_ratio)
    if shift == 0:
        return img
    img_shifted = np.zeros_like(img)
    img_shifted[:shift, :] = img[-shift:, :]
    img_shifted[shift:, :] = img[:-shift, :]
    img_shifted = img_shifted[mid_y-new_h//2:mid_y+new_h//2, mid_x-new_w//2:mid_x+new_w//2]
    return img_shifted

def rotate_image(img, angle, crop_ratio=1, mirror=False):
    h, w = img.shape
    new_h, new_w = int(h*crop_ratio), int(w*crop_ratio)
    img_rotated = Image.fromarray(img).rotate(angle)
    mid_x, mid_y = img_rotated.size[0]//2, img_rotated.size[1]//2
    img_rotated = img_rotated.crop((mid_x-new_w//2, mid_y-new_h//2, mid_x+new_w//2, mid_y+new_h//2))
    img_rotated = np.array(img_rotated)

    if mirror:
        img_rotated = np.concatenate((img_rotated, img_rotated[:, ::-1]), axis=1)
        img_rotated = np.concatenate((img_rotated, img_rotated[::-1, :]), axis=0)
        
    img_rotated = morphology.remove_small_objects(img_rotated > 0, min_size=10)
    img_rotated = img_rotated.astype(float)
    return img_rotated
        
def add_margin(img, margin_range=2):
    if margin_range == 0:
        return img
    else:
        margin_img = np.zeros((img.shape[0]+margin_range*2, img.shape[1]+margin_range*2))
        margin_img[margin_range:-margin_range, margin_range:-margin_range] = img
        return margin_img

def png_to_slc(refer_dcm_file, image, pixel_spacing, num, pos, thickness, output_path):
    image2d = image.astype(np.float16)

    meta = pydicom.Dataset()
    meta.MediaStorageSOPClassUID = pydicom.uid.ExplicitVRLittleEndian
    meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian  

    ds = pydicom.dcmread(refer_dcm_file)

    ds.Rows = image2d.shape[0]
    ds.Columns = image2d.shape[1]

    ds.PixelData = image2d.tobytes()

    ds.PixelSpacing = "{}\\{}".format(pixel_spacing, pixel_spacing)
    ds.SliceThickness = thickness

    ds.InstanceNumber = num
    ds.ImagePositionPatient = [0, pos, pos]    

    ds.save_as(output_path) 
