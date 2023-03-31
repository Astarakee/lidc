# LIDC-IDRI dataset harmonization
LIDC-IDRI dataset includes a large-scale annotated CT images. The original data is stored in Dicom series format and
the corresponding annoations were stored as XML file format. Standard PyLIDC library was designed to read
the data and extract the images, segmentation masks, or some labeled features.
In different studies, researchers have employed this dataset in different ways. For example, many people 
computed the overlapping regions of masks annotated by different experts while some used union regions as segmentation masks.
Another example is related to the number of manual annotations for each nodule. In some publicatoins, they employed only
the nodules which were annotated by at least two experts, while some other employed all the nodules.
This simple script aims to extract comprehensive data from the LIDC in a harmonized way for further analyses.
In specific, the script returns:
* For each patient ID, a directory containing:
          Orignal volume in .nii.gz format
          segmentation masks in .nii.gz format for all the labeled nodules (both overlapped and union masks)
          images and masks are saved in full image size and same spacing system
* A csv file containing:
          Name of the saved images \n
          name of the saved segmentation masks (both overlapped and union masks)
          Number of annotation for each nodule(mask)
          Malignancy score
          calcificatoin score
          nodule volume
          nodule diameter
          lobulatoin score
          spiculation score
          sphericity score
          subtlety score
          nodule surfiace
          texture score
          
          
## set-up

Clone the git project:
```
$ https://github.com/Astarakee/lidc.git
```
Changed the directory to the cloned folder:
```
cd lidc
```
Install the required libraries:
```
pip install -r requirements.txt
```
Create the PyLIDC configutatin file and save it in the home directory:
/home/[user]/.pylidcrc
This config file should contain:
```
[dicom]
path = absolute_path_to_original_LIDC_dir
warn = True
```
Execute the script:
```
python main.py -i absolute_path_to_original_LIDC_dir -o absolute_path_to_saving_dir
```
TODO
```
Add requirements.txt
```

