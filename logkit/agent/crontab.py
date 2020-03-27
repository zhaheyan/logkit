import logging
import requests
from django.conf import settings
from agent.models import Agent

LOG = logging.getLogger('default')


def check_agent_health():
    """check agent api health"""
    agents_info = settings.OPSAGENT['agents_info']
    for agent_info in agents_info:
        agent_url = agent_info + "/agent/health_check"
        agent_ip = agent_url.split('/')[2]
        try:
            r = requests.get(agent_url, timeout=5)
            if r.status_code == 200:
                Agent.objects.filter(agent_ip=agent_ip).update(agent_status='health')
            else:
                Agent.objects.filter(agent_ip=agent_ip).update(agent_status='abnormal')
        except exceptions.Timeout as e:
            Agent.objects.filter(agent_ip=agent_ip).update(agent_status='abnormal')
            LOG.error('crontab: agent status abnormal! error info: %s', e)
        LOG.info("crontab: check agent: %s", agent_ip)

