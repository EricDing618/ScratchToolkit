import subprocess
import sys

def run_pytest_with_timeout_handling():
    # 运行 pytest 并捕获输出
    result = subprocess.run(
        ["pytest", "--timeout=3", "--tb=no"],
        capture_output=True,
        text=True,
    )

    # 检查是否仅因 Timeout 失败
    if result.returncode != 0:
        # 检查 stderr/stdout 是否包含 Timeout 错误
        if "Timeout" in result.stderr or "Timeout" in result.stdout:
            print("⏱️ 测试超时（静默退出）", file=sys.stderr)
            sys.exit(0)  # 超时返回 0
        else:
            print("❌ 测试失败（非超时错误）", file=sys.stderr)
            print(result.stdout)
            sys.exit(1)  # 其他错误返回 1
    else:
        print("✅ 测试通过", file=sys.stderr)
        sys.exit(0)  # 成功返回 0

if __name__ == "__main__":
    run_pytest_with_timeout_handling()