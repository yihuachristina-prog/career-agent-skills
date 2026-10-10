"""Stable job identifiers, readable package names and explicitly authorized retention."""
import re

JOB_ID_RE = re.compile(r'^[A-Z]{2,3}-(?:\d{3}|\d{8}-[A-Za-z0-9]+)$')
ACTIVE = {'用户保留','待用户筛选','待补材料','定向材料已生成','已投递—待反馈','面试中','HR沟通中'}
TERMINAL = {'已失效','HR无回应或失联'}
GRAY_TERMINAL = {'深度评估后不投','已结束','HR明确拒绝/不合适'}

def package_name(job_id, company, role):
    if not JOB_ID_RE.fullmatch(job_id):
        raise ValueError('Invalid job identifier')
    def component(value):
        if not isinstance(value,str) or not value.strip():
            raise ValueError('Company and role are required')
        return re.sub(r'[<>:"/\\|?*\x00-\x1f]','－',value).strip().rstrip('.')
    result=f'{job_id}_{component(company)}_{component(role)}'
    if len(result)>240: raise ValueError('Package name too long; choose a verified short company name')
    return result

def package_job_id(name):
    job_id=name.split('_',1)[0]
    if not JOB_ID_RE.fullmatch(job_id): raise ValueError('Invalid package name')
    return job_id

def cleanup_reason(status, gray=False, green=False, end_reason='', explicit_keep=False):
    """No age, automatic Skip, or inaccessible-page inference is permitted."""
    if explicit_keep or green or status in ACTIVE: return None
    if status in TERMINAL: return status
    if status in GRAY_TERMINAL and (gray or end_reason=='用户确认不投'):
        return '用户灰色终止'
    if status=='已结束' and end_reason in {'未找到同一企业方职位','猎头线索无法核验真实用人企业'}:
        return '系统核验猎头终止'
    return None
