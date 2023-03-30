import pylidc as pl
import matplotlib.pyplot as plt
from pylidc.utils import consensus
from skimage.measure import find_contours

ann = pl.query(pl.Annotation).all()

first = ann[50].malignancy



from sqlalchemy import func

# Fetch all highly suspicious nodules
anns = pl.query(pl.Annotation).filter(pl.Annotation.malignancy == 5)

ann = anns.order_by(func.random()).first()
print(ann.id, ann.Malignancy)
# => 2516, 'Highly Suspicious'

ann = anns.order_by(func.random()).first()
print(ann.id, ann.Malignancy)
# => 4749, 'Highly Suspicious'




scans = pl.query(pl.Scan) # get all meta
ann = pl.query(pl.Annotation).first()
print(scans.count())
scans_all = scans.all() # get all scans
ex_pid = scans_all[15].patient_id



#pid = 'LIDC-IDRI-0078'
scan = pl.query(pl.Scan).filter(pl.Scan.patient_id == ex_pid).first()
nodules_annotation = scan.cluster_annotations()
vol = scan.to_volume()
vol.shape

if len(nodules_annotation) > 0:
    
    for nodule_idx, nodule in enumerate(nodules_annotation):
        
        cmask,cbbox,masks = consensus(nodule, clevel=0.5, pad=[(20,20), (20,20), (0,0)])
        k = int(0.5*(cbbox[2].stop - cbbox[2].start)) # central slice
        
        
                # Set up the plot.
        fig,ax = plt.subplots(1,1,figsize=(5,5))
        ax.imshow(vol[cbbox][:,:,k], cmap=plt.cm.gray, alpha=0.5)
        
        # Plot the annotation contours for the kth slice.
        colors = ['r', 'g', 'b', 'y']
        for j in range(len(masks)):
            for c in find_contours(masks[j][:,:,k].astype(float), 0.5):
                label = "Annotation %d" % (j+1)
                plt.plot(c[:,1], c[:,0], colors[j], label=label)
        
        # Plot the 50% consensus contour for the kth slice.
        for c in find_contours(cmask[:,:,k].astype(float), 0.5):
            plt.plot(c[:,1], c[:,0], '--k', label='50% Consensus')

ax.axis('off')
ax.legend()
plt.tight_layout()
#plt.savefig("../images/consensus.png", bbox_inches="tight")
plt.show()


        
        # We calculate the malignancy information
        malignancy, cancer_label = self.calculate_malignancy(nodule)


ann = pl.query(pl.Annotation).first()
contours = ann.contours

print(contours[0])

mask = ann.boolean_mask()





nods = scan.cluster_annotations()


print("%s has %d nodules." % (scan, len(nods)))
# => Scan(id=1,patient_id=LIDC-IDRI-0078) has 4 nodules.

for i,nod in enumerate(nods):
    print("Nodule %d has %d annotations." % (i+1, len(nods[i])))
# => Nodule 1 has 4 annotations.
# => Nodule 2 has 4 annotations.
# => Nodule 3 has 1 annotations.
# => Nodule 4 has 4 annotations.

scan.visualize(annotation_groups=nods)