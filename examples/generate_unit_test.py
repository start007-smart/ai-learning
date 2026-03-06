"""
AI 单元测试生成器
让 AI 自动为 Java 代码生成 JUnit 单元测试用例
"""

import sys
sys.path.append('..')

from ai_client import AIClient


def generate_junit_test(code: str, client: AIClient, framework: str = "JUnit5") -> str:
    """生成 JUnit 单元测试"""
    system = f"""你是一位资深 Java 测试工程师，专精 {framework} 和 Mockito。
请为用户提供的代码生成完整的单元测试，要求：
1. 覆盖正常流程、边界条件、异常场景
2. 使用 @DisplayName 描述每个测试的意图
3. 使用 Mockito mock 外部依赖（Repository、Service 等）
4. 断言使用 AssertJ（assertThat）风格
5. 测试方法命名：方法名_场景_期望结果（如 createUser_whenNameEmpty_throwsException）
6. 只输出完整的测试类代码，用 ```java 包裹"""

    return client.chat(
        f"请为以下代码生成 {framework} 单元测试：\n\n```java\n{code}\n```",
        system=system,
        temperature=0.2
    )


def generate_test_with_coverage_tips(code: str, client: AIClient) -> str:
    """生成测试并给出覆盖率建议"""
    system = """你是资深 Java 测试工程师。请：
1. 先列出该代码需要测试的关键点（用 Markdown 列表）
2. 再生成完整的 JUnit5 测试类（用 ```java 包裹）
3. 最后给出提高覆盖率的建议

格式严格按照：
### 测试关键点
- ...

### 测试代码
```java
...
```

### 覆盖率建议
- ..."""

    return client.chat(
        f"请分析并为以下代码生成单元测试：\n\n```java\n{code}\n```",
        system=system,
        temperature=0.3
    )


def main():
    client = AIClient()

    # ── 示例1：工具类方法 ─────────────────────────────────────
    print("=" * 60)
    print("🧪 示例1：工具类 → 生成单元测试")
    print("=" * 60)

    util_code = """
public class StringUtils {

    /**
     * 手机号脱敏：138****8888
     */
    public static String maskPhone(String phone) {
        if (phone == null || phone.length() != 11) {
            throw new IllegalArgumentException("手机号格式不正确");
        }
        return phone.substring(0, 3) + "****" + phone.substring(7);
    }

    /**
     * 是否为空（null 或空字符串）
     */
    public static boolean isEmpty(String str) {
        return str == null || str.trim().isEmpty();
    }

    /**
     * 截断字符串，超出部分用...代替
     */
    public static String truncate(String str, int maxLength) {
        if (str == null) return "";
        return str.length() <= maxLength ? str : str.substring(0, maxLength) + "...";
    }
}
"""
    print("Java 代码：")
    print(util_code)
    print("生成的测试：")
    print(generate_junit_test(util_code, client))

    # ── 示例2：Service 层（含外部依赖）───────────────────────
    print("\n" + "=" * 60)
    print("🏗️  示例2：Service 层 → Mock 依赖 + 异常测试")
    print("=" * 60)

    service_code = """
@Service
@RequiredArgsConstructor
public class UserService {

    private final UserRepository userRepository;

    public User createUser(String name, String email) {
        if (StringUtils.isEmpty(name)) {
            throw new IllegalArgumentException("用户名不能为空");
        }
        if (userRepository.existsByEmail(email)) {
            throw new BusinessException("邮箱已被注册: " + email);
        }
        User user = new User();
        user.setName(name);
        user.setEmail(email);
        return userRepository.save(user);
    }

    public User getUserById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new NotFoundException("用户不存在: " + id));
    }
}
"""
    print("Java 代码：")
    print(service_code)
    print("生成的测试（含覆盖率建议）：")
    print(generate_test_with_coverage_tips(service_code, client))

    # ── 示例3：算法 / 复杂逻辑 ────────────────────────────────
    print("\n" + "=" * 60)
    print("⚙️  示例3：业务逻辑 → 边界条件 + 参数化测试")
    print("=" * 60)

    logic_code = """
public class OrderPriceCalculator {

    private static final double VIP_DISCOUNT = 0.9;
    private static final double SVIP_DISCOUNT = 0.8;

    /**
     * 计算订单实付金额
     * @param originalPrice 原价（元）
     * @param userLevel     用户等级：NORMAL / VIP / SVIP
     * @param couponAmount  优惠券金额（元），0 表示无优惠券
     */
    public double calculate(double originalPrice, String userLevel, double couponAmount) {
        if (originalPrice < 0) {
            throw new IllegalArgumentException("原价不能为负数");
        }
        if (couponAmount < 0) {
            throw new IllegalArgumentException("优惠券金额不能为负数");
        }

        double discount = switch (userLevel) {
            case "VIP"  -> VIP_DISCOUNT;
            case "SVIP" -> SVIP_DISCOUNT;
            default     -> 1.0;
        };

        double finalPrice = originalPrice * discount - couponAmount;
        return Math.max(finalPrice, 0); // 最低0元
    }
}
"""
    print("Java 代码：")
    print(logic_code)
    print("生成的测试（含参数化测试）：")
    print(generate_junit_test(logic_code, client, framework="JUnit5 + @ParameterizedTest"))

    print("\n" + "=" * 60)
    print("🎉 单元测试生成演示完成！")
    print("=" * 60)
    print("\n💡 使用技巧：")
    print("  generate_junit_test(code, client)          → 快速生成测试")
    print("  generate_test_with_coverage_tips(code, client) → 生成测试 + 覆盖率分析")


if __name__ == "__main__":
    main()
