"""
Java → Python 代码转换器
让 AI 把 Java 代码翻译成地道的 Python 代码
"""

import sys
sys.path.append('..')

from ai_client import AIClient


def java_to_python(java_code: str, client: AIClient) -> str:
    """将 Java 代码转换为 Python 代码"""
    system = """你是一位精通 Java 和 Python 的高级工程师。
请将用户提供的 Java 代码转换为地道的 Python 代码，要求：
1. 使用 Python 的惯用写法（Pythonic），而不是直接逐行翻译
2. 用 Python 标准库替代 Java 标准库（如 ArrayList → list，HashMap → dict）
3. 保留原有逻辑和注释
4. 只输出转换后的 Python 代码，不要额外解释
5. 代码用 ```python ``` 包裹"""

    return client.chat(
        f"请将以下 Java 代码转换为 Python：\n\n```java\n{java_code}\n```",
        system=system,
        temperature=0.2
    )


def java_to_python_with_explain(java_code: str, client: AIClient) -> str:
    """转换并解释差异"""
    system = """你是一位精通 Java 和 Python 的高级工程师。
请将 Java 代码转换为地道的 Python 代码，并在转换后说明：
- 两种语言的主要差异点
- Python 版本中使用了哪些 Pythonic 技巧
格式：
1. 先输出 Python 代码（用 ```python 包裹）
2. 再输出「转换说明」（Markdown 列表）"""

    return client.chat(
        f"请将以下 Java 代码转换为 Python，并解释差异：\n\n```java\n{java_code}\n```",
        system=system,
        temperature=0.3
    )


def main():
    client = AIClient()

    # ── 示例1：基础 POJO / 数据类 ──────────────────────────────
    print("=" * 60)
    print("📦 示例1：Java POJO → Python dataclass")
    print("=" * 60)

    java_pojo = """
public class User {
    private Long id;
    private String name;
    private String email;
    private int age;

    public User(Long id, String name, String email, int age) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.age = age;
    }

    public Long getId() { return id; }
    public String getName() { return name; }
    public String getEmail() { return email; }
    public int getAge() { return age; }

    @Override
    public String toString() {
        return "User{id=" + id + ", name='" + name + "', email='" + email + "', age=" + age + "}";
    }
}
"""
    print("Java 代码：")
    print(java_pojo)
    print("Python 转换结果：")
    print(java_to_python(java_pojo, client))

    # ── 示例2：集合操作 ────────────────────────────────────────
    print("\n" + "=" * 60)
    print("🔄 示例2：Java 集合操作 → Python List / Dict")
    print("=" * 60)

    java_collection = """
import java.util.*;
import java.util.stream.*;

public class OrderUtils {
    // 过滤金额大于100的订单，并按金额降序排列
    public List<Order> filterAndSort(List<Order> orders) {
        return orders.stream()
            .filter(o -> o.getAmount() > 100)
            .sorted(Comparator.comparingDouble(Order::getAmount).reversed())
            .collect(Collectors.toList());
    }

    // 统计每个用户的总金额
    public Map<String, Double> sumByUser(List<Order> orders) {
        return orders.stream()
            .collect(Collectors.groupingBy(
                Order::getUserName,
                Collectors.summingDouble(Order::getAmount)
            ));
    }
}
"""
    print("Java 代码：")
    print(java_collection)
    print("Python 转换结果（含说明）：")
    print(java_to_python_with_explain(java_collection, client))

    # ── 示例3：异常处理 ────────────────────────────────────────
    print("\n" + "=" * 60)
    print("⚠️  示例3：Java 异常处理 → Python 异常机制")
    print("=" * 60)

    java_exception = """
public class FileProcessor {
    public String readFile(String path) {
        BufferedReader reader = null;
        try {
            reader = new BufferedReader(new FileReader(path));
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                sb.append(line).append("\\n");
            }
            return sb.toString();
        } catch (FileNotFoundException e) {
            System.err.println("文件不存在: " + path);
            throw new RuntimeException(e);
        } catch (IOException e) {
            System.err.println("读取失败: " + e.getMessage());
            throw new RuntimeException(e);
        } finally {
            if (reader != null) {
                try { reader.close(); } catch (IOException ignored) {}
            }
        }
    }
}
"""
    print("Java 代码：")
    print(java_exception)
    print("Python 转换结果（含说明）：")
    print(java_to_python_with_explain(java_exception, client))

    print("\n" + "=" * 60)
    print("🎉 转换演示完成！")
    print("=" * 60)
    print("\n💡 提示：把你自己的 Java 代码粘进来试试：")
    print("   result = java_to_python('你的Java代码', client)")
    print("   print(result)")


if __name__ == "__main__":
    main()
