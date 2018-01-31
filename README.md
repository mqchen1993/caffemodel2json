# Description
A small tool to dump Caffe's \*.caffemodel and \*.binaryproto files to JSON for inspection (\*.prototxt files is not needed). By default [caffe.proto](https://raw.githubusercontent.com/BVLC/caffe/master/src/caffe/proto/caffe.proto) from the official Caffe repository is used.

# Usage
```shell
# to dump model structure without weights (unless `--data` switch is used) to JSON, using default caffe.proto:
./caffemodel2json.py model.caffemodel > dump.json

# to dump model structure without weights (unless `--data` switch is used) to JSON:
./caffemodel2json.py model.caffemodel CAFFE_ROOT/src/caffe/proto/caffe.proto > dump.json

# to dump a binaryproto:
wget http://dl.caffe.berkeleyvision.org/caffe_ilsvrc12.tar.gz
mkdir -p imagenet_mean && tar -xf caffe_ilsvrc12.tar.gz -C imagenet_mean
./caffemodel2json.py imagenet_mean/imagenet_mean.binaryproto --data > imagenet_mean.json
```

# Dependencies
1. Python
2. protobuf (with Python bindings)
3. (optional) Caffe's caffe.proto (or from a Caffe's fork, it's important if you are inspecting a model that implements new Caffe layers)

# License
MIT
