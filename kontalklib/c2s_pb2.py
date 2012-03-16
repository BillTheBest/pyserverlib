# Generated by the protocol buffer compiler.  DO NOT EDIT!

from google.protobuf import descriptor
from google.protobuf import message
from google.protobuf import reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)



DESCRIPTOR = descriptor.FileDescriptor(
  name='c2s.proto',
  package='',
  serialized_pb='\n\tc2s.proto\"$\n\x13\x41uthenticateRequest\x12\r\n\x05token\x18\x01 \x02(\t\"%\n\x14\x41uthenticateResponse\x12\r\n\x05valid\x18\x01 \x02(\x08\"U\n\x12MessagePostRequest\x12\x11\n\trecipient\x18\x01 \x03(\t\x12\x0c\n\x04mime\x18\x02 \x01(\t\x12\r\n\x05\x66lags\x18\x03 \x03(\t\x12\x0f\n\x07\x63ontent\x18\x04 \x01(\x0c\"\xa5\x02\n\x13MessagePostResponse\x12/\n\x05\x65ntry\x18\x01 \x03(\x0b\x32 .MessagePostResponse.MessageSent\x1a\xdc\x01\n\x0bMessageSent\x12\x42\n\x06status\x18\x01 \x02(\x0e\x32\x32.MessagePostResponse.MessageSent.MessageSentStatus\x12\x0f\n\x07user_id\x18\x02 \x02(\t\x12\x12\n\nmessage_id\x18\x03 \x01(\t\"d\n\x11MessageSentStatus\x12\x12\n\x0eSTATUS_SUCCESS\x10\x00\x12\x10\n\x0cSTATUS_ERROR\x10\x01\x12\x0f\n\x0bSTATUS_BUSY\x10\x02\x12\x18\n\x14STATUS_USER_NOTFOUND\x10\x03\"\xa2\x01\n\nNewMessage\x12\x12\n\nmessage_id\x18\x01 \x02(\t\x12\x11\n\ttimestamp\x18\x02 \x02(\t\x12\x0e\n\x06sender\x18\x03 \x02(\t\x12\r\n\x05group\x18\x04 \x03(\t\x12\x13\n\x0boriginal_id\x18\x05 \x01(\t\x12\x0c\n\x04mime\x18\x06 \x02(\t\x12\r\n\x05\x66lags\x18\x07 \x03(\t\x12\x0f\n\x07\x63ontent\x18\x08 \x02(\x0c\x12\x0b\n\x03url\x18\t \x01(\t\"\'\n\x11MessageAckRequest\x12\x12\n\nmessage_id\x18\x01 \x03(\t\"\xe7\x01\n\x12MessageAckResponse\x12(\n\x05\x65ntry\x18\x01 \x03(\x0b\x32\x19.MessageAckResponse.Entry\x1a\xa6\x01\n\x05\x45ntry\x12\x12\n\nmessage_id\x18\x01 \x02(\t\x12:\n\x06status\x18\x02 \x02(\x0e\x32*.MessageAckResponse.Entry.MessageAckStatus\"M\n\x10MessageAckStatus\x12\x12\n\x0eSTATUS_SUCCESS\x10\x00\x12\x10\n\x0cSTATUS_ERROR\x10\x01\x12\x13\n\x0fSTATUS_NOTFOUND\x10\x02\"\x85\x02\n\x0eReceiptMessage\x12$\n\x05\x65ntry\x18\x01 \x03(\x0b\x32\x15.ReceiptMessage.Entry\x1a\xcc\x01\n\x05\x45ntry\x12\x12\n\nmessage_id\x18\x01 \x02(\t\x12\x33\n\x06status\x18\x02 \x02(\x0e\x32#.ReceiptMessage.Entry.ReceiptStatus\x12\x11\n\ttimestamp\x18\x03 \x01(\t\"g\n\rReceiptStatus\x12\x12\n\x0eSTATUS_SUCCESS\x10\x00\x12\x10\n\x0cSTATUS_ERROR\x10\x01\x12\x18\n\x14STATUS_USER_NOTFOUND\x10\x02\x12\x16\n\x12STATUS_TTL_EXPIRED\x10\x03\"\'\n\x13RegistrationRequest\x12\x10\n\x08username\x18\x01 \x02(\t\"\xf3\x01\n\x14RegistrationResponse\x12\x38\n\x06status\x18\x01 \x02(\x0e\x32(.RegistrationResponse.RegistrationStatus\x12\r\n\x05token\x18\x02 \x01(\t\x12\x10\n\x08sms_from\x18\x03 \x01(\t\x12\x12\n\nemail_from\x18\x04 \x01(\t\"l\n\x12RegistrationStatus\x12\x12\n\x0eSTATUS_SUCCESS\x10\x00\x12\x10\n\x0cSTATUS_ERROR\x10\x01\x12\x13\n\x0fSTATUS_CONTINUE\x10\x02\x12\x1b\n\x17STATUS_INVALID_USERNAME\x10\x03\",\n\x11ValidationRequest\x12\x17\n\x0fvalidation_code\x18\x01 \x02(\t\"\xa6\x01\n\x12ValidationResponse\x12\x34\n\x06status\x18\x01 \x02(\x0e\x32$.ValidationResponse.ValidationStatus\x12\r\n\x05token\x18\x02 \x01(\t\"K\n\x10ValidationStatus\x12\x12\n\x0eSTATUS_SUCCESS\x10\x00\x12\x10\n\x0cSTATUS_ERROR\x10\x01\x12\x11\n\rSTATUS_FAILED\x10\x02\"$\n\x11UserLookupRequest\x12\x0f\n\x07user_id\x18\x01 \x03(\t\"\x8d\x01\n\x12UserLookupResponse\x12(\n\x05\x65ntry\x18\x01 \x03(\x0b\x32\x19.UserLookupResponse.Entry\x1aM\n\x05\x45ntry\x12\x0f\n\x07user_id\x18\x01 \x02(\t\x12\x11\n\ttimestamp\x18\x02 \x01(\x04\x12\x0e\n\x06status\x18\x03 \x01(\t\x12\x10\n\x08timediff\x18\x04 \x01(\x04\x42 \n\x12org.kontalk.clientB\x08ProtocolH\x03')



_MESSAGEPOSTRESPONSE_MESSAGESENT_MESSAGESENTSTATUS = descriptor.EnumDescriptor(
  name='MessageSentStatus',
  full_name='MessagePostResponse.MessageSent.MessageSentStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='STATUS_SUCCESS', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_ERROR', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_BUSY', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_USER_NOTFOUND', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=371,
  serialized_end=471,
)

_MESSAGEACKRESPONSE_ENTRY_MESSAGEACKSTATUS = descriptor.EnumDescriptor(
  name='MessageAckStatus',
  full_name='MessageAckResponse.Entry.MessageAckStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='STATUS_SUCCESS', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_ERROR', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_NOTFOUND', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=834,
  serialized_end=911,
)

_RECEIPTMESSAGE_ENTRY_RECEIPTSTATUS = descriptor.EnumDescriptor(
  name='ReceiptStatus',
  full_name='ReceiptMessage.Entry.ReceiptStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='STATUS_SUCCESS', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_ERROR', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_USER_NOTFOUND', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_TTL_EXPIRED', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1072,
  serialized_end=1175,
)

_REGISTRATIONRESPONSE_REGISTRATIONSTATUS = descriptor.EnumDescriptor(
  name='RegistrationStatus',
  full_name='RegistrationResponse.RegistrationStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='STATUS_SUCCESS', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_ERROR', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_CONTINUE', index=2, number=2,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_INVALID_USERNAME', index=3, number=3,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1354,
  serialized_end=1462,
)

_VALIDATIONRESPONSE_VALIDATIONSTATUS = descriptor.EnumDescriptor(
  name='ValidationStatus',
  full_name='ValidationResponse.ValidationStatus',
  filename=None,
  file=DESCRIPTOR,
  values=[
    descriptor.EnumValueDescriptor(
      name='STATUS_SUCCESS', index=0, number=0,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_ERROR', index=1, number=1,
      options=None,
      type=None),
    descriptor.EnumValueDescriptor(
      name='STATUS_FAILED', index=2, number=2,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=1602,
  serialized_end=1677,
)


_AUTHENTICATEREQUEST = descriptor.Descriptor(
  name='AuthenticateRequest',
  full_name='AuthenticateRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='token', full_name='AuthenticateRequest.token', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  serialized_start=13,
  serialized_end=49,
)


_AUTHENTICATERESPONSE = descriptor.Descriptor(
  name='AuthenticateResponse',
  full_name='AuthenticateResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='valid', full_name='AuthenticateResponse.valid', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
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
  serialized_start=51,
  serialized_end=88,
)


_MESSAGEPOSTREQUEST = descriptor.Descriptor(
  name='MessagePostRequest',
  full_name='MessagePostRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='recipient', full_name='MessagePostRequest.recipient', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='mime', full_name='MessagePostRequest.mime', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='flags', full_name='MessagePostRequest.flags', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='content', full_name='MessagePostRequest.content', index=3,
      number=4, type=12, cpp_type=9, label=1,
      has_default_value=False, default_value="",
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
  serialized_start=90,
  serialized_end=175,
)


_MESSAGEPOSTRESPONSE_MESSAGESENT = descriptor.Descriptor(
  name='MessageSent',
  full_name='MessagePostResponse.MessageSent',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='MessagePostResponse.MessageSent.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='user_id', full_name='MessagePostResponse.MessageSent.user_id', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='message_id', full_name='MessagePostResponse.MessageSent.message_id', index=2,
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
    _MESSAGEPOSTRESPONSE_MESSAGESENT_MESSAGESENTSTATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=251,
  serialized_end=471,
)

_MESSAGEPOSTRESPONSE = descriptor.Descriptor(
  name='MessagePostResponse',
  full_name='MessagePostResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='entry', full_name='MessagePostResponse.entry', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_MESSAGEPOSTRESPONSE_MESSAGESENT, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=178,
  serialized_end=471,
)


_NEWMESSAGE = descriptor.Descriptor(
  name='NewMessage',
  full_name='NewMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='message_id', full_name='NewMessage.message_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timestamp', full_name='NewMessage.timestamp', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='sender', full_name='NewMessage.sender', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='group', full_name='NewMessage.group', index=3,
      number=4, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='original_id', full_name='NewMessage.original_id', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='mime', full_name='NewMessage.mime', index=5,
      number=6, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='flags', full_name='NewMessage.flags', index=6,
      number=7, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='content', full_name='NewMessage.content', index=7,
      number=8, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='url', full_name='NewMessage.url', index=8,
      number=9, type=9, cpp_type=9, label=1,
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
  serialized_start=474,
  serialized_end=636,
)


_MESSAGEACKREQUEST = descriptor.Descriptor(
  name='MessageAckRequest',
  full_name='MessageAckRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='message_id', full_name='MessageAckRequest.message_id', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=638,
  serialized_end=677,
)


_MESSAGEACKRESPONSE_ENTRY = descriptor.Descriptor(
  name='Entry',
  full_name='MessageAckResponse.Entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='message_id', full_name='MessageAckResponse.Entry.message_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='status', full_name='MessageAckResponse.Entry.status', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _MESSAGEACKRESPONSE_ENTRY_MESSAGEACKSTATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=745,
  serialized_end=911,
)

_MESSAGEACKRESPONSE = descriptor.Descriptor(
  name='MessageAckResponse',
  full_name='MessageAckResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='entry', full_name='MessageAckResponse.entry', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_MESSAGEACKRESPONSE_ENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=680,
  serialized_end=911,
)


_RECEIPTMESSAGE_ENTRY = descriptor.Descriptor(
  name='Entry',
  full_name='ReceiptMessage.Entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='message_id', full_name='ReceiptMessage.Entry.message_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='status', full_name='ReceiptMessage.Entry.status', index=1,
      number=2, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timestamp', full_name='ReceiptMessage.Entry.timestamp', index=2,
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
    _RECEIPTMESSAGE_ENTRY_RECEIPTSTATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=971,
  serialized_end=1175,
)

_RECEIPTMESSAGE = descriptor.Descriptor(
  name='ReceiptMessage',
  full_name='ReceiptMessage',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='entry', full_name='ReceiptMessage.entry', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_RECEIPTMESSAGE_ENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=914,
  serialized_end=1175,
)


_REGISTRATIONREQUEST = descriptor.Descriptor(
  name='RegistrationRequest',
  full_name='RegistrationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='username', full_name='RegistrationRequest.username', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  serialized_start=1177,
  serialized_end=1216,
)


_REGISTRATIONRESPONSE = descriptor.Descriptor(
  name='RegistrationResponse',
  full_name='RegistrationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='RegistrationResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='token', full_name='RegistrationResponse.token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='sms_from', full_name='RegistrationResponse.sms_from', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='email_from', full_name='RegistrationResponse.email_from', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _REGISTRATIONRESPONSE_REGISTRATIONSTATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1219,
  serialized_end=1462,
)


_VALIDATIONREQUEST = descriptor.Descriptor(
  name='ValidationRequest',
  full_name='ValidationRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='validation_code', full_name='ValidationRequest.validation_code', index=0,
      number=1, type=9, cpp_type=9, label=2,
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
  serialized_start=1464,
  serialized_end=1508,
)


_VALIDATIONRESPONSE = descriptor.Descriptor(
  name='ValidationResponse',
  full_name='ValidationResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='status', full_name='ValidationResponse.status', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='token', full_name='ValidationResponse.token', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _VALIDATIONRESPONSE_VALIDATIONSTATUS,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1511,
  serialized_end=1677,
)


_USERLOOKUPREQUEST = descriptor.Descriptor(
  name='UserLookupRequest',
  full_name='UserLookupRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='user_id', full_name='UserLookupRequest.user_id', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
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
  serialized_start=1679,
  serialized_end=1715,
)


_USERLOOKUPRESPONSE_ENTRY = descriptor.Descriptor(
  name='Entry',
  full_name='UserLookupResponse.Entry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='user_id', full_name='UserLookupResponse.Entry.user_id', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timestamp', full_name='UserLookupResponse.Entry.timestamp', index=1,
      number=2, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='status', full_name='UserLookupResponse.Entry.status', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    descriptor.FieldDescriptor(
      name='timediff', full_name='UserLookupResponse.Entry.timediff', index=3,
      number=4, type=4, cpp_type=4, label=1,
      has_default_value=False, default_value=0,
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
  serialized_start=1782,
  serialized_end=1859,
)

_USERLOOKUPRESPONSE = descriptor.Descriptor(
  name='UserLookupResponse',
  full_name='UserLookupResponse',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    descriptor.FieldDescriptor(
      name='entry', full_name='UserLookupResponse.entry', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_USERLOOKUPRESPONSE_ENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=1718,
  serialized_end=1859,
)

_MESSAGEPOSTRESPONSE_MESSAGESENT.fields_by_name['status'].enum_type = _MESSAGEPOSTRESPONSE_MESSAGESENT_MESSAGESENTSTATUS
_MESSAGEPOSTRESPONSE_MESSAGESENT.containing_type = _MESSAGEPOSTRESPONSE;
_MESSAGEPOSTRESPONSE_MESSAGESENT_MESSAGESENTSTATUS.containing_type = _MESSAGEPOSTRESPONSE_MESSAGESENT;
_MESSAGEPOSTRESPONSE.fields_by_name['entry'].message_type = _MESSAGEPOSTRESPONSE_MESSAGESENT
_MESSAGEACKRESPONSE_ENTRY.fields_by_name['status'].enum_type = _MESSAGEACKRESPONSE_ENTRY_MESSAGEACKSTATUS
_MESSAGEACKRESPONSE_ENTRY.containing_type = _MESSAGEACKRESPONSE;
_MESSAGEACKRESPONSE_ENTRY_MESSAGEACKSTATUS.containing_type = _MESSAGEACKRESPONSE_ENTRY;
_MESSAGEACKRESPONSE.fields_by_name['entry'].message_type = _MESSAGEACKRESPONSE_ENTRY
_RECEIPTMESSAGE_ENTRY.fields_by_name['status'].enum_type = _RECEIPTMESSAGE_ENTRY_RECEIPTSTATUS
_RECEIPTMESSAGE_ENTRY.containing_type = _RECEIPTMESSAGE;
_RECEIPTMESSAGE_ENTRY_RECEIPTSTATUS.containing_type = _RECEIPTMESSAGE_ENTRY;
_RECEIPTMESSAGE.fields_by_name['entry'].message_type = _RECEIPTMESSAGE_ENTRY
_REGISTRATIONRESPONSE.fields_by_name['status'].enum_type = _REGISTRATIONRESPONSE_REGISTRATIONSTATUS
_REGISTRATIONRESPONSE_REGISTRATIONSTATUS.containing_type = _REGISTRATIONRESPONSE;
_VALIDATIONRESPONSE.fields_by_name['status'].enum_type = _VALIDATIONRESPONSE_VALIDATIONSTATUS
_VALIDATIONRESPONSE_VALIDATIONSTATUS.containing_type = _VALIDATIONRESPONSE;
_USERLOOKUPRESPONSE_ENTRY.containing_type = _USERLOOKUPRESPONSE;
_USERLOOKUPRESPONSE.fields_by_name['entry'].message_type = _USERLOOKUPRESPONSE_ENTRY
DESCRIPTOR.message_types_by_name['AuthenticateRequest'] = _AUTHENTICATEREQUEST
DESCRIPTOR.message_types_by_name['AuthenticateResponse'] = _AUTHENTICATERESPONSE
DESCRIPTOR.message_types_by_name['MessagePostRequest'] = _MESSAGEPOSTREQUEST
DESCRIPTOR.message_types_by_name['MessagePostResponse'] = _MESSAGEPOSTRESPONSE
DESCRIPTOR.message_types_by_name['NewMessage'] = _NEWMESSAGE
DESCRIPTOR.message_types_by_name['MessageAckRequest'] = _MESSAGEACKREQUEST
DESCRIPTOR.message_types_by_name['MessageAckResponse'] = _MESSAGEACKRESPONSE
DESCRIPTOR.message_types_by_name['ReceiptMessage'] = _RECEIPTMESSAGE
DESCRIPTOR.message_types_by_name['RegistrationRequest'] = _REGISTRATIONREQUEST
DESCRIPTOR.message_types_by_name['RegistrationResponse'] = _REGISTRATIONRESPONSE
DESCRIPTOR.message_types_by_name['ValidationRequest'] = _VALIDATIONREQUEST
DESCRIPTOR.message_types_by_name['ValidationResponse'] = _VALIDATIONRESPONSE
DESCRIPTOR.message_types_by_name['UserLookupRequest'] = _USERLOOKUPREQUEST
DESCRIPTOR.message_types_by_name['UserLookupResponse'] = _USERLOOKUPRESPONSE

class AuthenticateRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHENTICATEREQUEST
  
  # @@protoc_insertion_point(class_scope:AuthenticateRequest)

class AuthenticateResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _AUTHENTICATERESPONSE
  
  # @@protoc_insertion_point(class_scope:AuthenticateResponse)

class MessagePostRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MESSAGEPOSTREQUEST
  
  # @@protoc_insertion_point(class_scope:MessagePostRequest)

class MessagePostResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class MessageSent(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _MESSAGEPOSTRESPONSE_MESSAGESENT
    
    # @@protoc_insertion_point(class_scope:MessagePostResponse.MessageSent)
  DESCRIPTOR = _MESSAGEPOSTRESPONSE
  
  # @@protoc_insertion_point(class_scope:MessagePostResponse)

class NewMessage(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _NEWMESSAGE
  
  # @@protoc_insertion_point(class_scope:NewMessage)

class MessageAckRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _MESSAGEACKREQUEST
  
  # @@protoc_insertion_point(class_scope:MessageAckRequest)

class MessageAckResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Entry(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _MESSAGEACKRESPONSE_ENTRY
    
    # @@protoc_insertion_point(class_scope:MessageAckResponse.Entry)
  DESCRIPTOR = _MESSAGEACKRESPONSE
  
  # @@protoc_insertion_point(class_scope:MessageAckResponse)

class ReceiptMessage(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Entry(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _RECEIPTMESSAGE_ENTRY
    
    # @@protoc_insertion_point(class_scope:ReceiptMessage.Entry)
  DESCRIPTOR = _RECEIPTMESSAGE
  
  # @@protoc_insertion_point(class_scope:ReceiptMessage)

class RegistrationRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REGISTRATIONREQUEST
  
  # @@protoc_insertion_point(class_scope:RegistrationRequest)

class RegistrationResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _REGISTRATIONRESPONSE
  
  # @@protoc_insertion_point(class_scope:RegistrationResponse)

class ValidationRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VALIDATIONREQUEST
  
  # @@protoc_insertion_point(class_scope:ValidationRequest)

class ValidationResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _VALIDATIONRESPONSE
  
  # @@protoc_insertion_point(class_scope:ValidationResponse)

class UserLookupRequest(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _USERLOOKUPREQUEST
  
  # @@protoc_insertion_point(class_scope:UserLookupRequest)

class UserLookupResponse(message.Message):
  __metaclass__ = reflection.GeneratedProtocolMessageType
  
  class Entry(message.Message):
    __metaclass__ = reflection.GeneratedProtocolMessageType
    DESCRIPTOR = _USERLOOKUPRESPONSE_ENTRY
    
    # @@protoc_insertion_point(class_scope:UserLookupResponse.Entry)
  DESCRIPTOR = _USERLOOKUPRESPONSE
  
  # @@protoc_insertion_point(class_scope:UserLookupResponse)

# @@protoc_insertion_point(module_scope)
