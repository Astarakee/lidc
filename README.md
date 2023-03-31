## LIDC-IDRI dataset harmonization
LIDC-IDRI dataset includes a large-scale annotated CT images. The original data is stpred in Dicom series and
the corresponding annoations were stored as XML file format. Standard PyLIDC library was designed to read
the data and extract the images, segmentation masks, or some labeled features.
In different studies, researchers have employed this dataset in different ways. For example, many people 
computed the overlapping regions of masks annotated by different experts while some used union regions as segmentation masks.
Another example is related to the number of manual annotations for each nodule. In some publicatoins, they employed only
the nodules which were annotated by at least two experts, while some other employed all the nodules.
This simple script aims to extract comprehensive data from the LIDC in a harmonized way for further analyses.

