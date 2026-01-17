"""
Pytest配置和共享fixtures
"""
import pytest
import sys
import os

# 添加项目根目录到Python路径
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)


@pytest.fixture
def sample_date():
    """提供测试用的日期"""
    return '2025-01-01'


@pytest.fixture
def mock_config_path(tmp_path):
    """提供临时配置路径用于测试"""
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    return str(config_dir)
