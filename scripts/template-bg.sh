# Copyright (c) Facebook, Inc. and its affiliates. All rights reserved.
gpus=$1
seqname=$2
addr=$3
use_human=$4
use_symm=$5
num_epochs=120
batch_size=256

model_prefix=dfl-$seqname-e$num_epochs-b$batch_size
if [ "$use_human" = "" ]; then
  pose_cnn_path=mesh_material/posenet/human.pth
else
  pose_cnn_path=mesh_material/posenet/quad.pth
fi
echo $pose_cnn_path

# mode: line load
savename=${model_prefix}-init
bash scripts/template-mgpu.sh $gpus $savename \
    $seqname $addr --num_epochs $num_epochs \
  --use_rtk_file --nounc_filter \
  --warmup_shape_ep 5 --warmup_rootmlp \
  --noloss_flt --norm_novp --noroot_sm --alpha 6 --bound_factor 3\
  --nolbs --nouse_embed --nouse_proj --bound_reset 0 --nf_reset 1.1 --nouse_cc \
  --lineload --batch_size $batch_size\
  --${use_symm}symm_shape \
  --${use_human}use_human
  #--pose_cnn_path $pose_cnn_path  --freeze_root  --flow_wt 0 --img_wt 0   --nodist_corresp
