#!/bin/bash

echo "开始运行测试..."

# 运行 agents 目录下的测试
for test_file in tests/agents/test_*.py; do
    if [ -f "$test_file" ]; then
        echo "运行测试: $test_file"
        if PYTHONPATH=src pytest "$test_file" -v; then
            echo "✓ $test_file 测试通过"
        else
            echo "✗ $test_file 测试失败"
            exit 1
        fi
    fi
done

# 运行 utils 目录下的测试
for test_file in tests/utils/test_*.py; do
    if [ -f "$test_file" ]; then
        echo "运行测试: $test_file"
        if PYTHONPATH=src pytest "$test_file" -v; then
            echo "✓ $test_file 测试通过"
        else
            echo "✗ $test_file 测试失败"
            exit 1
        fi
    fi
done 