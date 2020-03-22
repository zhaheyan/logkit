import datetime
import jwt

def create_token(username):
    """Create jwt token"""
    playload = {
        'iss': "logkit",
        'sub': "logkit-console",
        'username': username,
        # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        'iat': datetime.datetime.utcnow() 
    }   
    key = "secret_key"
    token = str(jwt.encode(playload, key, algorithm="HS256"), encoding="utf-8")
    return token
    
def get_username(token):
    """根据token解析用户信息，如果解析成功，返回用户信息"""
    try:
        decode_token = jwt.decode(token, "secret_key", algorithm="HS256")
        username = decode_token.get("username")
        return username
    except Exception as e:
        return None

