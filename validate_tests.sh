#!/bin/bash

# 设置颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

# 初始化错误计数器
error_count=0

# 确保在项目根目录下运行
if [ ! -d "tests" ]; then
    echo -e "${RED}错误：请在项目根目录下运行此脚本${NC}"
    exit 1
fi

# 安装项目包（开发模式）
echo "安装项目包..."
pip install -e .

# 运行所有测试文件
echo "开始运行测试..."

# 运行 agents 目录下的测试
for test_file in tests/agents/test_*.py; do
    if [ -f "$test_file" ]; then
        echo "运行测试: $test_file"
        if PYTHONPATH=src pytest "$test_file" -v; then
            echo -e "${GREEN}✓ $test_file 测试通过${NC}"
        else
            echo -e "${RED}✗ $test_file 测试失败${NC}"
            error_count=$((error_count + 1))
        fi
    fi
done

# 运行 utils 目录下的测试
for test_file in tests/utils/test_*.py; do
    if [ -f "$test_file" ]; then
        echo "运行测试: $test_file"
        if PYTHONPATH=src pytest "$test_file" -v; then
            echo -e "${GREEN}✓ $test_file 测试通过${NC}"
        else
            echo -e "${RED}✗ $test_file 测试失败${NC}"
            error_count=$((error_count + 1))
        fi
    fi
done

# 输出测试结果摘要
echo "测试完成。"
if [ $error_count -eq 0 ]; then
    echo -e "${GREEN}所有测试通过！${NC}"
    exit 0
else
    echo -e "${RED}测试失败：$error_count 个测试文件出现错误${NC}"
    exit 1
fi 