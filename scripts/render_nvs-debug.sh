#Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
dev=$1
seqname=$2
model_path=$3
vidid=$4   # pose traj
rootid=$5  # root traj

testdir=${model_path%/*} # %: from end
echo $testdir
save_prefix=$testdir/nvs-$vidid-$rootid
scale=1
sample_grid3d=64
add_args="--sample_grid3d ${sample_grid3d} \
  --nouse_corresp --nouse_embed --nouse_proj --render_size 2 --ndepth 2 --nouse_cc"

# render
rootdir=$trgpath-ctrajs-
CUDA_VISIBLE_DEVICES=$dev python scripts/visualize/nvs.py --flagfile=$testdir/opts.log \
  --model_path $model_path \
  --vidid $vidid \
  --scale $scale --bullet_time -1 \
  --chunk 2048 \
  --nouse_corresp --nouse_unc --perturb 0\
  --rootdir $rootdir --nvs_outpath $save_prefix-traj
