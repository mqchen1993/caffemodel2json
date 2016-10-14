import os
import sys
import json
import argparse
import tempfile
import subprocess

def log(x, prefix = None):
	if prefix != None:
		x = '%8s: %s' % (prefix, x)
	print >> sys.stderr, x

def pb2json(pb, print_arrays):
	from google.protobuf.descriptor import FieldDescriptor as FD
	_ftype2js = {
		FD.TYPE_DOUBLE: float,
		FD.TYPE_FLOAT: float,
		FD.TYPE_INT64: long,
		FD.TYPE_UINT64: long,
		FD.TYPE_INT32: int,
		FD.TYPE_FIXED64: float,
		FD.TYPE_FIXED32: float,
		FD.TYPE_BOOL: bool,
		FD.TYPE_STRING: unicode,
		FD.TYPE_BYTES: lambda x: x.encode('string_escape'),
		FD.TYPE_UINT32: int,
		FD.TYPE_ENUM: int,
		FD.TYPE_SFIXED32: float,
		FD.TYPE_SFIXED64: float,
		FD.TYPE_SINT32: int,
		FD.TYPE_SINT64: long,
	}
	js = {}
	fields = pb.ListFields()	#only filled (including extensions)
	for field,value in fields:
		if field.type == FD.TYPE_MESSAGE:
			ftype = pb2json
		elif field.type in _ftype2js:
			ftype = _ftype2js[field.type]
		else:
			log("WARNING: Field %s.%s of type '%d' is not supported" % (pb.__class__.__name__, field.name, field.type, ))
		if field.label == FD.LABEL_REPEATED:
			js_value = []
			for v in value:
				js_value.append(ftype(v))
			if not print_arrays and (len(js_value) > 64 or (field.name == 'data' and len(js_value) > 8)):
				head_n = 5
				js_value = js_value[:head_n] + ['(%d elements more)' % (len(js_value) - head_n)]
		else:
			js_value = ftype(value)
		js[field.name] = js_value
	return js

parser = argparse.ArgumentParser('Dump model_name.caffemodel to a file JSON format for debugging')
parser.add_argument('caffe.proto', help = 'Path to caffe.proto (typically located at CAFFE_ROOT/src/caffe/proto/caffe.proto)', metavar = 'caffe_proto')
parser.add_argument('model_caffemodel', help = 'Path to model.caffemodel')
parser.add_argument('--data', help = 'Print all arrays in full', action = 'store_true')
parser.add_argument('--codegenDir', help = 'Path to an existing temporary directory to save generated protobuf Python classes', default = tempfile.mkdtemp())
args = parser.parse_args()

log('calling protoc', 'protobuf')
local_caffe_proto = os.path.join(args.codegenDir, os.path.basename(args.caffe_proto))
with open(local_caffe_proto, 'w') as f:
	f.write((urllib2.urlopen(args.caffe_proto) if 'http' in args.caffe_proto else open(args.caffe_proto)).read())
	
subprocess.check_call(['protoc', '--proto_path', args.codegenDir, '--python_out', args.codegenDir, local_caffe_proto])
log('generated', 'protobuf')

sys.path.insert(0, args.codegenDir)
import caffe_pb2
log('imported', 'protobuf')


netParam = caffe_pb2.NetParameter()
msg = open(args.model_caffemodel, 'rb').read()
log('caffemodel read in memory. Deserialization will take a few minutes. Take a coffee!', 'model')
netParam.ParseFromString(msg)
log('deserialized', 'model')

json.dump(pb2json(netParam, args.data), sys.stdout, indent = 2)
log('json saved', 'model')

log('')
log('ALLOK. Quitting')
