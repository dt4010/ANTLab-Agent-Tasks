import os, json, time, urllib.request, urllib.error
from urllib.parse import urlparse

def _is_responses_endpoint(endpoint):
    return urlparse(endpoint).path.rstrip('/').endswith('/responses')

def call_model(messages, config, mock=False):
    if mock:
        return {'status':'mock','elapsed_seconds':0.0,
                'response':{'choices':[{'message':{'content':'{"answer":"MOCK_NOT_EVIDENCE","citations":[]}'}}]},
                'usage':None,'http_status':None}
    endpoint=config['endpoint']
    if urlparse(endpoint).scheme != 'https':
        raise ValueError('自费API endpoint必须为https；此骨架不自动调用本地模型')
    key=os.environ.get('ASSESSMENT_API_KEY','')
    if not key: raise ValueError('缺少环境变量ASSESSMENT_API_KEY；不要写入配置文件')
    params=config.get('parameters',{})
    responses_api=_is_responses_endpoint(endpoint)
    reserved={'model','input','messages','stream'} if responses_api else {'messages','model','stream'}
    if not isinstance(params,dict) or set(params)&reserved:
        raise ValueError('parameters不可覆盖请求保留字段')
    if responses_api:
        body={'model':config['model'],'input':messages,**params}
        if 'max_tokens' in body and 'max_output_tokens' not in body:
            body['max_output_tokens']=body.pop('max_tokens')
    else:
        body={'model':config['model'],'messages':messages,'stream':False,**params}
    req=urllib.request.Request(endpoint, data=json.dumps(body,ensure_ascii=False).encode(),
                               headers={'Content-Type':'application/json',
                                        'Accept':'application/json',
                                        'User-Agent':'ANTLab-Agent-Assessment/1.0',
                                        'Authorization':'Bearer '+key})
    start=time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=float(config.get('timeout_seconds',90))) as response:
            raw=response.read().decode('utf-8'); status=response.status
        try: parsed=json.loads(raw)
        except json.JSONDecodeError:
            return {'status':'invalid_provider_json','elapsed_seconds':time.perf_counter()-start,
                    'response':raw,'usage':None,'http_status':status}
        return {'status':'ok','elapsed_seconds':time.perf_counter()-start,'response':parsed,
                'usage':parsed.get('usage') if isinstance(parsed,dict) else None,'http_status':status}
    except urllib.error.HTTPError as e:
        # 不保存错误页正文，避免意外收录请求凭据；成功模型响应原样保存。
        raw=e.read().decode('utf-8','replace')
        try: error_response=json.loads(raw)
        except json.JSONDecodeError: error_response=raw
        return {'status':'http_error','elapsed_seconds':time.perf_counter()-start,
                'http_status':e.code,'error':'HTTP '+str(e.code),'response':error_response,'usage':None}
    except (urllib.error.URLError,TimeoutError) as e:
        return {'status':'transport_error','elapsed_seconds':time.perf_counter()-start,
                'http_status':None,'error':type(e).__name__,'response':None,'usage':None}
