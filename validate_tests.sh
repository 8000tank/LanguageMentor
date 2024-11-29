#!/bin/bash

echo "开始运行测试和覆盖率检查..."

# 设置最低覆盖率要求
MIN_COVERAGE=80

# 使用 pytest-cov 运行所有测试并生成覆盖率报告
if PYTHONPATH=src pytest tests/ --cov=src --cov-report=term-missing --cov-report=html -v; then
    echo "✓ 所有测试通过"
    
    # 获取总覆盖率数值
    COVERAGE=$(coverage report | grep TOTAL | awk '{print $NF}' | sed 's/%//')
    
    if (( $(echo "$COVERAGE >= $MIN_COVERAGE" | bc -l) )); then
        echo "✓ 测试覆盖率达标：${COVERAGE}% (要求：${MIN_COVERAGE}%)"
        exit 0
    else
        echo "✗ 测试覆盖率不达标：${COVERAGE}% (要求：${MIN_COVERAGE}%)"
        echo "请查看 htmlcov/index.html 了解详细覆盖率报告"
        exit 1
    fi
else
    echo "✗ 测试运行失败"
    exit 1
fi 