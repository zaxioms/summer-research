# bash xx.sh "cat-pikachiu00 cat-pikachiu01"

input=$1

for seqname in $input
do
    echo $seqname
    python preprocess/mask_fg.py $seqname
    cpulimit -i -l 400 -- python preprocess/colmap2nerf.py --images ./tmp/$seqname/ --run_colmap
    python preprocess/colmap2banmo.py tmp/$seqname/transforms.json $seqname
done

