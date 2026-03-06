import json, base64, datetime

def pad_base64(b):
 return b + '=' * (-len(b) % 4)

def decode_base64url(data):
 return base64.urlsafe_b64decode(pad_base64(data))

def beautify_json(data):
  return json.dumps(data, indent=2, ensure_ascii=False)

def convert_exp(exp):
  try:
    dt = datetime.datetime.fromtimestamp(exp)
    return dt.strftime("%Y-%m-%d %H:%M:%S")
  except:
    return "❌ Invalid timestamp"

def decode_jwt(token):
  try:
    header_b64, payload_b64, signature_b64 = token.split('.')
    header_json, payload_json = json.loads(decode_base64url(header_b64)), json.loads(decode_base64url(payload_b64))
    LKH = {"status": True, }
    LKH["headers"] = json.loads(beautify_json(header_json))
    LKH["payload"] = json.loads(beautify_json(payload_json))
    if 'token_type' in payload_json:
      LKH["token_type"] = payload_json['token_type']
    else:
      LKH["token_type"] = None
    if 'exp' in payload_json:
      LKH["exp"] = convert_exp(payload_json['exp'])
    LKH["signature"] = signature_b64
    return LKH
  except Exception as e:
    return {"status": False, "error": e}
