# Score Update Model

评分数据更新独立项目

## 项目简介

本项目是从 Data_update 项目中提取的评分更新模块，可以独立部署和运行。主要功能包括：

- RR评分数据更新
- 组合权重计算
- 评分组合更新
- 数据库同步

## 项目结构

```
score_update_model/
├── src/                      # 源代码目录
│   ├── score_update/        # 评分更新模块
│   ├── time_tools/          # 时间工具模块
│   ├── global_setting/      # 全局配置模块
│   └── setup_logger/        # 日志设置模块
├── config/                   # 配置文件目录
│   ├── config_path/         # 路径配置
│   └── config_project/      # 项目配置
├── tests/                    # 测试文件目录
├── logs/                     # 日志文件目录
├── docs/                     # 文档目录
├── score_update_main.py     # 主入口文件
├── requirements.txt         # 依赖管理文件
└── pytest.ini               # 测试配置文件
```

## 快速开始

### 1. 环境要求

- Python 3.8+
- 必须设置环境变量 `GLOBAL_TOOLSFUNC_new` 指向 global_tools 模块路径

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置文件

确保以下配置文件已正确设置：

- `config/config_path/data_update_path_config.xlsx` - 数据路径配置
- `config/config_project/Score_config/config_score_mode.xlsx` - 评分模式配置
- `config/config_project/Data_update/sql_connection.yaml` - 数据库连接配置
- `config/config_project/Data_update/time_tools_config.xlsx` - 时间配置

### 4. 运行项目

```bash
python score_update_main.py
```

### 5. 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_score_update.py

# 生成覆盖率报告
pytest --cov=src tests/
```

## 功能说明

### 主要功能

1. **RR评分更新** (`rrScore_update`)
   - 处理原始RR评分数据
   - 生成每日评分文件
   - 同步到SQL数据库

2. **组合权重计算** (`scorePortfolio_update`)
   - 计算Top组合权重
   - 计算沪深300组合
   - 计算中证2000组合
   - UBP500组合处理

3. **评分组合更新** (`scoreCombination_update`)
   - 多评分组合计算
   - 指数成分股筛选

### 日志

项目日志文件保存在 `logs/processing_log/` 目录下，文件名格式为 `processingLogs_YYYYMMDD.log`

## 注意事项

1. 运行前必须设置环境变量 `GLOBAL_TOOLSFUNC_new`
2. 确保配置文件中的路径正确指向数据目录
3. 数据库连接信息在 `sql_connection.yaml` 中配置
4. 输入数据和输出数据路径由 `config_path` 配置决定

## 依赖项目

本项目依赖以下外部模块（通过环境变量引用）：
- `global_tools` - 全局工具函数库

## 开发指南

### 添加新功能

1. 在 `src/` 对应模块下添加代码
2. 在 `tests/` 下添加对应的测试文件
3. 更新文档

### 代码规范

- 遵循PEP 8编码规范
- 添加适当的注释和文档字符串
- 编写单元测试

## 许可证

内部项目

## 维护者

数据团队
