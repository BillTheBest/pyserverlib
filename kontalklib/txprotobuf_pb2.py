# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='txprotobuf.proto',
  package='',
  serialized_pb='\n\x10txprotobuf.proto\":\n\x0c\x42oxContainer\x12\x0c\n\x04name\x18\x01 \x02(\t\x12\r\n\x05value\x18\x02 \x02(\x0c\x12\r\n\x05tx_id\x18\x03 \x01(\tB#\n\x12org.kontalk.clientB\x0b\x42oxProtocolH\x03')




_BOXCONTAINER = descriptor.Descriptor(
  name='BoxContainer',
  full_name='BoxContainer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='name', full_name='BoxContainer.name', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='value', full_name='BoxContainer.value', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='tx_id', full_name='BoxContainer.tx_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=20,
  serialized_end=78,
)

DESCRIPTOR.message_types_by_name['BoxContainer'] = _BOXCONTAINER

class BoxContainer(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BOXCONTAINER
  
  # @@protoc_insertion_point(class_scope:BoxContainer)

# @@protoc_insertion_point(module_scope)
