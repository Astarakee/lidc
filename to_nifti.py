import numpy as np  
import matplotlib.pyplot as plt  
import pylidc as pl
import os 
import SimpleITK as itk
import pandas as pd
from copy import deepcopy
from utils.sitk_stuff import read_dicom_series, reorient_itk



def union_mask(expert_masks):
    
    temp_np = np.array(expert_masks)
    temp_sum = np.sum(temp_np, axis=0)
    binary_temp = deepcopy(temp_sum)
    binary_temp[binary_temp!=0] = 1
    binary_temp = binary_temp.astype('uint8')
    
    return binary_temp

def overlap_majority(expert_masks):
    
    n_masks = len(expert_masks)
    temp_np = np.array(expert_masks)
    temp_sum = np.sum(temp_np, axis=0)
    half_thr = int(np.ceil(n_masks/2))
    binary_temp = deepcopy(temp_sum)
    binary_temp[binary_temp<half_thr] = 0
    binary_temp[binary_temp>=half_thr] = 1    
    binary_temp = binary_temp.astype('uint8')
    
    return binary_temp



scans = pl.query(pl.Scan)

print(scans.count()) 

path = '/mnt/work/data/Lung/LIDC/LIDC-IDRI'
path_folders = os.listdir(path)

write_path = './'
count = 0
my_id = 1

df_colnames = [
            'img', 'mask_union', 'mask_overlap', 
            'n_annotation', 'malignancy', 'calcification', 
            'volume', 'diameter', 'lobulation', 'spiculation', 
            'sphericity', 'subtlety', 'surface_area', 'texture'
]

df = pd.DataFrame(columns=df_colnames)
feature_save_path = './lidc.csv'
path_folders = path_folders[:20]

for pid in path_folders: #adjust according to the number of folders you downloaded

    folder_subject = os.path.join(write_path, pid)
    if not os.path.exists(folder_subject):
        os.mkdir(folder_subject)

    scans = pl.query(pl.Scan).filter(pl.Scan.patient_id == pid).all() #obtain the scans
    
    n_scans = len(scans)
    
    for s_id in range(n_scans):
       
       scan =  scans[s_id]
       ann = scan.annotations
       # vol = scan.to_volume() # image volume
       dcm_path = scan.get_path_to_dicom_files()
       _, itk_img, _, _, _, _ = read_dicom_series(dcm_path)
       img_array, img_itk, imt_spacing, img_origin, img_direction = reorient_itk(itk_img)
       del itk_img
       nods = scan.cluster_annotations() # nodules of scan as object
       n_nodul = len(nods)
       
       print('Working on subject {} with {} image scan + {} nodules ...'.format(pid, n_scans, n_nodul))
       
       general_name = pid+'_scan_'+str(s_id+1)
       img_name = general_name+'.nii.gz'
       
       itk.WriteImage(img_itk, os.path.join(folder_subject, img_name))
  
       for n_id in range(n_nodul):

           annots = nods[n_id] 
           n_annots = len(annots)
           expert_masks = []
           
           for ix in range(n_annots):
               current_annot = annots[ix] #grab the first annotation
               
               annot_malignancy = current_annot.malignancy
               annot_calcification = current_annot.calcification
               annot_volume = current_annot.volume
               annot_diameter = current_annot.diameter
               annot_lobulation = current_annot.lobulation
               annot_spiculation = current_annot.spiculation
               annot_sphericity = current_annot.sphericity
               annot_subtlety = current_annot.subtlety
               annot_surface_area = current_annot.surface_area
               annot_texture = current_annot.texture
                             
               nodule_depth_ind = current_annot.contour_slice_indices
               nodule_slice_ind = current_annot.contours_matrix
               starting_slice = nodule_slice_ind[0]
               ending_slice = nodule_slice_ind[-1]
               padding_coord = [(int(starting_slice[0]),512),
                                (int(starting_slice[1]),512),
                                (int(starting_slice[2]),img_array.shape[0])]
               
               seg_mask = current_annot.boolean_mask(padding_coord)
               seg_mask = np.transpose(seg_mask, axes=(2,0,1))
               seg_mask = seg_mask.astype('uint8')
               
               expert_masks.append(seg_mask)
               
           unions =  union_mask(expert_masks)
           overlap = overlap_majority(expert_masks)
           
           itk_union = itk.GetImageFromArray(unions)
           itk_overlap = itk.GetImageFromArray(overlap)
           
           _, union_itk, _, _, _ = reorient_itk(itk_union)
           _, overlap_itk, _, _, _ = reorient_itk(itk_overlap)
           
           union_itk.SetOrigin(img_origin)
           union_itk.SetDirection(img_direction)
           union_itk.SetSpacing(imt_spacing)  
                     
           overlap_itk.SetOrigin(img_origin)
           overlap_itk.SetDirection(img_direction)
           overlap_itk.SetSpacing(imt_spacing)  
                     
           union_name = general_name+'_union_mask_'+str(n_id)+'.nii.gz'
           overlap_name = general_name+'_overlap_mask_'+str(n_id)+'.nii.gz'
           
           itk.WriteImage(union_itk, os.path.join(folder_subject, union_name))
           itk.WriteImage(overlap_itk, os.path.join(folder_subject, overlap_name))
           
           fingerprint = {}
           fingerprint[str(df_colnames[0])] = general_name
           fingerprint[str(df_colnames[1])] = union_name
           fingerprint[str(df_colnames[2])] = overlap_name
           fingerprint[str(df_colnames[3])] = n_annots
           
           fingerprint[str(df_colnames[4])] = annot_malignancy
           fingerprint[str(df_colnames[5])] = annot_calcification
           fingerprint[str(df_colnames[6])] = annot_volume
           fingerprint[str(df_colnames[7])] = annot_diameter
           fingerprint[str(df_colnames[8])] = annot_lobulation
           fingerprint[str(df_colnames[9])] = annot_spiculation
           fingerprint[str(df_colnames[10])] = annot_sphericity
           fingerprint[str(df_colnames[11])] = annot_subtlety
           fingerprint[str(df_colnames[12])] = annot_surface_area
           fingerprint[str(df_colnames[13])] = annot_texture
                     

           fingerprint_df = pd.DataFrame(fingerprint, index=[0])
           df = pd.concat([df, fingerprint_df], axis=0, ignore_index=True)
           

df.to_csv(feature_save_path)

          
               
           