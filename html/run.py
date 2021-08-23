# -*- coding: utf-8 -*-
# @Time    : 2021/7/28 15:43
# @Author  : zangtao
# @Email   : 461033382@qq.com
# @File    : run.py
# @Software: PyCharm

from streamlit import bootstrap
import os


def run(*args):
    real_script = os.path.join(os.path.dirname(__file__), 'server.py')
    system_str = "streamlit run {html_path} {args}".format(
        html_path=real_script,
        args=" ".join(args)
    )
    os.system(system_str)
    # bootstrap.run(real_script, 'run.py {real_script}', args, {})
