## State-dependent relationship between lower and higher order networks in fMRI brain dynamics  

## Shreyas Harita<sup>1, 2</sup>, Davide Momi<sup>2, 3</sup>, Zheng Wang<sup>2</sup>, John D. Griffiths<sup>1, 2, 4, 5, **</sup>  

### Affiliations:    

1 = Institute of Medical Science, University of Toronto    
2 = Krembil Centre for Neuroinformatics, Centre for Addiction and Mental Health (CAMH), Toronto    
3 = Unit of Neuroimaging and Neurointervention, Department of Neurological and Neurosensorial Sciences, AOUS, 53100, Siena, Italy  
4 = Department of Physiology, University of Toronto    
5 = Department of Psychiatry, University of Toronto    
** = Corresponding Author  

### Highlights:  

- The reduced Wong-Wang neural mass model was implemented in a PyTorch environment and used to understand what drives resting-state network functional connectivity (FC).   
- Structural connectivity (SC) lesions were used to isolate functional networks to see how functional networks interact in various brain states.   
- There is a mutual antagonism between LONs and HONs in the resting-state.    
- This antagonism is seen to reverse in tasks with higher cognitive load (working memory, language).  
- Tasks with a lower cognitive load (motor) share a similar network interactivity profile to the resting-state following network SC lesions.  

  
### Keywords:  

Neural-mass model, Task fMRI, Resting-state fMRI, Functional Connectivity, Structural Connectivity.

### This manuscript is currently being prepared for submission as an original research article. BioRxiv and Pubmed links will follow soon. 

### Abstract  

Resting-state functional magnetic resonance imaging (rs-fMRI) is a powerful tool for exploring the brain's functional organization. It measures functional connectivity (FC) by analyzing the temporal correlations between activity patterns in different brain regions. FC research has identified specific networks, known as resting-state networks (RSNs), which connect various brain areas. RSNs are organized along a gradient: at one end are 'lower order' networks (LONs) for unimodal information processing, and at the other end are 'higher order' networks (HONs) for integrating multimodal information. Unlike stable structural connectivity (SC) based on fixed anatomical links, FC fluctuates over time and varies across brain regions. FC coordination within RSNs depends on SC, forming interconnected networks that regulate cognition, emotion, and behavior. In this study, we aimed to understand how brain RSNs interact and communicate based on the underlying SC. We used a whole-brain connectome-based neural mass modeling approach of resting-state and task-based fMRI FC data, implemented in the Whole Brain modelling in the PyTorch (WhoBPyT) software library. By creating virtual SC lesions, we characterized the FC changes within and between functional networks and observed how these changes varied across different cognitive states. Our findings reveal how FC dynamics depend on underlying SC, showcasing the flexibility of these interactions across different brain states. LON lesions generally decrease FC within and between other LONs, and vice-versa for HON lesions. Particularly, there is a mutual antagonism between LONs and HONs at rest, which reverses during task conditions. Additionally, during the working memory and language tasks, there is increased coordination between LONs and HONs. These results highlight the dynamic nature of brain network interactions, influenced by brain states and task demands. These findings have implications for clinical practice, offering insights into conditions like brain tumors and strokes, where SC lesions occur, and can inform personalized treatment and rehabilitation approaches.  


There are 3 main folders in this GitHub repository:  

1. Data: This folder contains all pertinent information regarding the data used for the analysis presented in this study. Details about the HCP dataset can be found here.

2. Code: This folder contains all the relevant scripts/code used for the analysis in this study.

3. Figures: This folder contains the figures from the manuscript. 

Please see the README within each folder for more information.  

If you have any further questions, please contact Shreyas Harita at shreyas.harita@mail.utoronto.ca.    
