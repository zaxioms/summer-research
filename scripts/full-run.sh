gpus=$1
seqname=$2
addr=$3
video_format=$4
preprocess_fps=$5
use_human=$6 #"yes"/"no"
use_symm=$7 #"yes"/"no"
num_epochs=120
batch_size=256

bash preprocess/preprocess.sh $seqname $video_format $use_human $preprocess_fps
python preprocess/img2lines.py --seqname $seqname
bash preprocess/run_colmap.sh $seqname
python preprocess/config-edit.py "configs/bg-$seqname.config"
seqname=bg-$seqname
bash scripts/template-bg.sh $gpus $seqname $addr $use_human $use_symm
bash scripts/render_nvs.sh $gpus $seqname logdir/dfl-$seqname-e120-b256-init/params_latest.pth 0 0



