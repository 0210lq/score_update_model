"""
Score Update Main Entry Point
评分数据更新主入口文件
"""
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# 导入global_tools（通过环境变量）
path = os.getenv('GLOBAL_TOOLSFUNC_new')
if not path:
    raise EnvironmentError(
        "环境变量 GLOBAL_TOOLSFUNC_new 未设置。\n"
        "请设置该环境变量指向 global_tools 模块路径。\n"
        "Windows: set GLOBAL_TOOLSFUNC_new=D:\\path\\to\\global_tools\n"
        "Linux/Mac: export GLOBAL_TOOLSFUNC_new=/path/to/global_tools"
    )
sys.path.append(path)
import global_tools as gt

# 导入项目内部模块
from src.time_tools.time_tools import time_tools
from src.score_update.score_update_main import score_update_main


def ScoreData_update_main(is_sql=True):
    """
    评分数据更新主函数

    Args:
        is_sql (bool): 是否将数据保存到SQL数据库，默认为True

    Returns:
        None
    """
    # 初始化时间工具
    tt = time_tools()

    # 决定目标日期
    date = tt.target_date_decision_score()
    date = gt.strdate_transfer(date)

    # 设置评分类型
    score_type = 'fm'

    # 执行评分更新
    score_update_main(score_type, date, date, is_sql)


if __name__ == '__main__':
    # 执行主函数
    ScoreData_update_main(is_sql=True)
