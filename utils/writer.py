import os
import ants
import SimpleITK as itk
from utils.paths_dirs_stuff import create_path

def write_nifti_from_vol(vol_array, itk_orig, itk_space, itk_dir, absolute_name):
    '''
    Write back an array into a compressed nifti format by maintaining the 
    essential meta-data for image geometrics.

    Parameters
    ----------
    vol_array : Numpy array
        A (volumetric) array of image(mask) data.
    itk_orig : Tuple
        The origin(coordinates) of the reference image use to save the new
        image.
    itk_space : Tuple
        The voxel spacing of the reference image use to save the name image.
    itk_dir : Tuple
        The standard direction of the reference image use to save the image.
    absolute_name : string
        the absolute path plus the name of the file excluding the extension
        file format. for example:
            '/mnt/mri/data/SubjectName'

    Returns
    -------
    A compressed nifti file will be saved with the same geometrical properties
    as a reference image. for example:
        '/mnt/mri/data/SubjectName.nii.gz'
    '''
    
    new_itk = itk.GetImageFromArray(vol_array)
    new_itk.SetSpacing(itk_space)
    new_itk.SetOrigin(itk_orig)
    new_itk.SetDirection(itk_dir)  
    fileName = absolute_name+'.nii.gz'     
    itk.WriteImage(new_itk, fileName)
    
    return None

def write_nifti_from_itk(itk_img, itk_orig, itk_space, itk_dir, absolute_name):
    '''
    Write back itk image into a compressed nifti format by maintaining the 
    essential meta-data for image geometrics.

    Parameters
    ----------
    vol_array : Numpy array
        A (volumetric) array of image(mask) data.
    itk_orig : Tuple
        The origin(coordinates) of the reference image use to save the new
        image.
    itk_space : Tuple
        The voxel spacing of the reference image use to save the name image.
    itk_dir : Tuple
        The standard direction of the reference image use to save the image.
    absolute_name : string
        the absolute path plus the name of the file excluding the extension
        file format. for example:
            '/mnt/mri/data/SubjectName'

    Returns
    -------
    A compressed nifti file will be saved with the same geometrical properties
    as a reference image. for example:
        '/mnt/mri/data/SubjectName.nii.gz'
    '''

    itk_img.SetSpacing(itk_space)
    itk_img.SetOrigin(itk_orig)
    itk_img.SetDirection(itk_dir)  
    fileName = absolute_name+'.nii.gz'     
    itk.WriteImage(itk_img, fileName)
    
    return None


def write_warped(img, subject_name, subject_folder):
    '''
    Write back the registered arrays as nifti images.

    Parameters
    ----------
    img : ant image
        warped image.
    subject_name : string
        name of the image sequence. eg. "example_t1ce.nii.gz"
    subject_folder : string
        folder path of the subject. eg. "/mnt/data/registered/subject1"

    Returns
    -------
    save the warped images as nifti files.

    '''
    create_path(subject_folder)
    filename_write = os.path.join(subject_folder, subject_name)
    ants.image_write(img, filename_write)
    
    return None