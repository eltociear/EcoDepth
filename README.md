<div align="center">
<h1>ECoDepth: Effective Conditioning of Diffusion Models for Monocular Depth Estimation</h1>

**CVPR 2024**  
<a href='https://ecodepth-iitd.github.io' style="margin-right: 20px;"><img src='https://img.shields.io/badge/Project Page-ECoDepth-darkgreen' alt='Project Page'></a>
<a href="https://arxiv.org/abs" style="margin-right: 20px;"><img src='https://img.shields.io/badge/Paper-arXiv-maroon' alt='arXiv page'></a>
<a href="https://arxiv.org/abs" style="margin-right: 20px;"><img src='https://img.shields.io/badge/Paper-CvF-blue' alt='IEEE Xplore Paper'></a>
<a href="https://arxiv.org/abs" style="margin-right: 20px;"><img src='https://img.shields.io/badge/Supplementary-CvF-blue' alt='IEEE Xplore Paper'></a>

[Suraj Patni](https://github.com/surajiitd)\*,
[Aradhye Agarwal](https://github.com/Aradhye2002)\*,
[Chetan Arora](https://www.cse.iitd.ac.in/~chetan)<br/>

</div>

<!-- display pdf -->

![Architecture Diagram](figs/aarch_diagram.png)


## News
- [Coming soon] Pretrained checkpoints for NYUv2 and KITTI datasets.
- [March 2024] Training and Inference code released!
- [Feb 2024] ECoDepth accepted in CVPR'2024.


## Installation

``` bash
git clone https://github.com/Aradhye2002/EcoDepth
cd EcoDepth
conda env create -f env.yml
conda activate ecodepth
```
## Dataset
You can see the dataset preparation guide for NYUv2 and KITTI from [here](https://github.com/cleinc/bts). After Update the paths in the desired bash scripts for evaluation and training accordingly.
## Pretrained Models

Please download the pretrained weights form [this link]() and save `.ckpt` inside `<repo root>/depth/checkpoints` directory.

## Evaluation
To evaluate our performance on NYUv2 and KITTI datasets, use `test.py` file. The trained models are publicly available, download the models using [above links](#pretrained-models).

1. **Train on NYUv2 dataset**:  
`bash test_nyu.sh <path_to_saved_model_of_NYU>`  

2. **Train on KITTI dataset**:  
`bash test_kitti.sh <path_to_saved_model_of_KITTI>`

## Training 
We trained our models on 32 batch size using 8xNVIDIA A100 GPUs. Please set the `NPROC_PER_NODE` variable and `--batch_size` argument to set the batch size. We set them as `NPROC_PER_NODE=8` and `--batch_size=4`. So our effective batch_size is 32.  

1. **Evaluate on NYUv2 dataset**:  
`bash train_nyu.sh`  

2. **Evaluate on KITTI dataset**:  
`bash train_kitti.sh`

### Contact
If you have any questions about our code or paper, kindly raise an issue on Github.
### Acknowledgment
We thank [Kartik Anand](https://github.com/k-styles) for assistance with the experiments. 
Our source code is inspired from [VPD](https://github.com/wl-zhao/VPD) and [PixelFormer](https://github.com/ashutosh1807/PixelFormer), we thank their authors for publicly releasing the code.

### BibTeX (Citation)
If you find our work useful in your research, lease consider citing the following:
``` bibtex
TODO
.
.
.
.
```