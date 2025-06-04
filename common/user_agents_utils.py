"""
user agents 解析
"""
import logging
from typing import Optional

from user_agents import parse
from common.common_model import BaseDict


logger = logging.getLogger(__name__)


class UserAgent(BaseDict):

    @property
    def browser(self) -> Optional[str]:
        return self.to_str('browser')

    @browser.setter
    def browser(self, val: Optional[str] = None):
        self.set_val(key='browser', val=val)

    @property
    def os(self) -> Optional[str]:
        return self.to_str('os')

    @os.setter
    def os(self, val: Optional[str] = None):
        self.set_val(key='os', val=val)

    @property
    def device(self) -> Optional[str]:
        return self.to_str('device')

    @device.setter
    def device(self, val: Optional[str]):
        self.set_val(key='device', val=val)

    @property
    def mobile(self) -> bool:
        return self.to_bool('mobile')

    @mobile.setter
    def mobile(self, val: Optional[bool] = False):
        self.set_val(key='mobile', val=val)

    @property
    def tablet(self) -> bool:
        return self.to_bool('tablet')

    @tablet.setter
    def tablet(self, val: Optional[bool] = False):
        self.set_val(key='tablet', val=val)

    @property
    def pc(self) -> bool:
        return self.to_bool('pc')

    @pc.setter
    def pc(self, val: Optional[bool] = False):
        self.set_val(key='pc', val=val)


def parse_useragent(agent_str: str = None) -> UserAgent:
    user_agent = UserAgent()
    try:
        agent = parse(agent_str)
        user_agent.browser = agent.browser.family
        user_agent.os = agent.os.family
        user_agent.device = agent.device.family
        user_agent.mobile = agent.is_mobile
        user_agent.tablet = agent.is_tablet
        user_agent.pc = agent.is_pc
    except Exception as e:
        logger.error(f'解析浏览器agent出错,agent_str:{agent_str}', exc_info=True)
    return user_agent



