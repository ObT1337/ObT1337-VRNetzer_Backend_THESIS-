#!bash
tar -C $2 -xjf $1 '*.pdb.gz'
gzip -d $2/*.pdb.gz