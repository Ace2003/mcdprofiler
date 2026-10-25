# 麦当劳 MCP 调用手册（mcd-mcp 接入与调用链）

> 接入地址：`https://mcp.mcd.cn`（Streamable HTTP）
> 鉴权：`Authorization: Bearer <MCP_TOKEN>`，Token 从 [open.mcd.cn/mcp](https://open.mcd.cn/mcp) 申请。
> 限流：每 Token 600 次/分钟；401 = Token 失效，429 = 触发限流。

## 本 Skill 实际使用的工具及调用时机

| 阶段 | 工具 | 用途 |
|---|---|---|
| 时段校准 | `now-time-info` | 获取真实时间，判定早餐 / 正餐 / 深夜菜单时段，避免凭模型记忆猜时段 |
| 门店锁定 | `query-nearby-stores` / `delivery-query-stores` | 到店取餐场景查附近门店；外送场景按收货地址查可配送门店 |
| 菜单匹配 | `query-meals` → `query-meal-detail` | 拉取当前门店可售菜单，将"人格套餐"映射到真实餐品编码；用详情接口核对套餐组成与可替换项 |
| 营养佐证 | `list-nutrition-foods` | 当侧写结论涉及热量焦虑 / 健康管理人格时，用真实营养数据支撑断言 |
| 优惠执行 | `available-coupons` → `auto-bind-coupons`；门店内用 `query-store-coupons` | 侧写标签为"资源焦虑型 / 薅券之神"时自动领券；下单前取用户可用券 |
| 价格核算 | `calculate-price` | 按商品列表 + 优惠券计算商品金额、配送费、优惠与应付总价，作为下单前确认依据 |
| 订单执行 | `create-order` | 双重确认后创建订单，返回订单详情与支付链接；`cancel-order` 用于取消 |
| 状态查询 | `query-order` / `order-list` | 查订单进度与历史，支持"上次点的那单"回溯侧写 |

扩展场景（按需启用）：积分侧写用 `query-my-account`、`mall-points-products`、`mall-create-order`；
活动人格用 `campaign-calendar`；积分抽奖人格用 `query-lottery-info` / `draw-lottery`。

## 标准调用链（Phase 3 执行序列）

```
1. now-time-info
   → 输出：当前真实时间 → 判定时段（早餐 05:00-10:30 / 正餐 / 深夜 1+1）

2. query-nearby-stores（堂食/外带/得来速 择一）
   → 输入：用户位置或配送地址 → 输出：门店列表 → 用户选定门店

3. query-meals(storeId)
   → 输出：分类菜单（餐品编码、标签）→ 将"人格套餐"映射到真实餐品编码
   → query-meal-detail(mealCode) 核对套餐组成 / 可替换项 / 特制选项

4. available-coupons / query-store-coupons（可选 auto-bind-coupons）
   → 输出：可用券列表 → 按"人格标签"选择最适配的券组合

5. calculate-price(storeId, items[], couponId?)
   → 输出：商品金额、配送费、优惠金额、应付总价
   → 【双确认】向用户复述：餐品明细 + 优惠券 + 应付总价，等待确认

6. create-order(storeId, 就餐方式, items[], couponId?)
   → 输出：订单详情 + 支付链接 → 交付用户完成支付

7. （可选）query-order 跟踪订单状态
```

## 调用纪律

1. **禁止跳过双确认**：`create-order` 前必须复述订单内容与金额并获得用户明确同意。
2. **禁止明文 Token**：任何配置示例仅使用 `YOUR_MCP_TOKEN` 占位符。
3. **限流友好**：单次会话调用控制在 20 次以内，避免循环重试；429 时提示用户稍后再试。
4. **失败降级**：任何 MCP 调用失败时，先输出侧写报告（纯推理不依赖 MCP），再提示用户检查
   Token 与网络。侧写是主体验，下单是落地点，二者解耦。

## WorkBuddy 接入配置

```json
{
  "mcpServers": {
    "mcd-mcp": {
      "type": "streamablehttp",
      "url": "https://mcp.mcd.cn",
      "headers": {
        "Authorization": "Bearer YOUR_MCP_TOKEN"
      }
    }
  }
}
```

保存后在连接器中启用 `mcd-mcp` 即可。详细申请流程见官方仓库
[M-China/mcd-mcp-server](https://github.com/M-China/mcd-mcp-server)。
