# MCP_INTEGRATION.md — 麦当劳 MCP 集成说明

## 1. 使用的 MCP Server

| 项目 | 内容 |
|---|---|
| Server 名称 | `mcd-mcp`（麦当劳中国官方 MCP 服务） |
| 接入地址 | `https://mcp.mcd.cn` |
| 传输协议 | Streamable HTTP |
| 鉴权方式 | `Authorization: Bearer <MCP_TOKEN>`（Token 经 [open.mcd.cn/mcp](https://open.mcd.cn/mcp) 申请） |
| 限流约束 | 每 Token 600 次/分钟；401 = Token 失效，429 = 触发限流 |
| 接入平台 | WorkBuddy 自定义连接器（配置方式见 README「安装方法」） |

## 2. 实际使用的 Tool 列表

本 Skill 的核心创新是"侧写 → 落单"闭环，以下 Tool 按业务流程实际使用：

| Tool | 业务角色 | 使用场景 |
|---|---|---|
| `now-time-info` | 时段校准 | 侧写前获取真实时间，判定早餐/正餐/深夜菜单时段，杜绝模型凭空编造时段 |
| `query-nearby-stores` | 门店锁定 | 到店/得来速场景查询用户附近可用门店 |
| `delivery-query-stores` | 门店锁定（外送） | 外送场景按收货地址查询可配送门店 |
| `query-meals` | 菜单匹配 | 拉取当前门店可售菜单，把"人格套餐"映射为真实餐品编码 |
| `query-meal-detail` | 套餐核对 | 核对套餐组成、可替换项与特制选项（去冰、少酱等微操） |
| `list-nutrition-foods` | 营养佐证 | 侧写结论涉及热量焦虑时，用真实营养数据支撑断言 |
| `available-coupons` | 优惠发现 | 查询用户可领取的麦麦省优惠券 |
| `auto-bind-coupons` | 优惠执行 | "资源焦虑型人格"自动领取全部可用券 |
| `query-store-coupons` | 优惠发现（门店） | 查询当前门店可用优惠券列表 |
| `calculate-price` | 价格核算 | 商品金额、配送费、优惠金额与应付总价，作为下单前确认依据 |
| `create-order` | 订单执行 | 双确认后创建订单，返回订单详情与支付链接 |
| `cancel-order` | 订单回滚 | 用户反悔时取消订单 |
| `query-order` / `order-list` | 状态与回溯 | 跟踪订单进度；"侧写我的历史点单"场景读取历史订单 |

扩展人格场景（按需启用）：积分人格（`query-my-account`、`mall-points-products`、
`mall-create-order`）、活动人格（`campaign-calendar`）、抽奖人格（`query-lottery-info`、
`draw-lottery`、`query-my-prizes`）。

## 3. 调用流程

```
[输入碎片] 时间/场景/辣度/冰量/用券习惯/加购冲动
     │
     ▼
① now-time-info ──► 校准真实时段（早餐 05:00-10:30 / 正餐 / 深夜 1+1）
     │
     ▼
② query-nearby-stores / delivery-query-stores ──► 锁定门店
     │
     ▼
③ query-meals → query-meal-detail ──► "人格套餐" → 真实餐品编码
     │
     ▼
④ available-coupons → auto-bind-coupons / query-store-coupons ──► 按人格标签配券
     │
     ▼
⑤ calculate-price ──► 报出应付总价 ──► 【双确认：复述明细+金额，等用户同意】
     │
     ▼
⑥ create-order ──► 返回订单详情与支付链接 ──► （可选）query-order 跟踪
```

失败降级策略：侧写报告（纯推理）不依赖 MCP，任何 MCP 调用失败时先保证报告输出，
再提示用户检查 Token 与网络，保证核心体验永远可用。

## 4. 业务价值

1. **真实可跑通**：不是概念演示——侧写结束即产生一笔真实可支付的麦当劳订单，
   完整覆盖"查询 → 配券 → 计价 → 下单 → 支付"主链路。
2. **AI 决策与商业转化的闭环**：把"我该吃什么"的仪式感决策，直接转化为门店订单，
   为麦当劳 MCP 的点餐场景提供了一种高情绪价值的新入口。
3. **券利用率提升**：以"人格标签"驱动领券与配券（如资源焦虑型自动 `auto-bind-coupons`），
   让优惠券在恰当的心理时机被使用。
4. **限流友好与安全合规**：单会话调用控制在 20 次以内；`create-order` 强制双确认；
   所有配置仅使用 `YOUR_MCP_TOKEN` 占位符，不落任何真实凭证。

## 5. 安全声明

- 本项目不存储、不传输、不展示任何真实 MCP Token；示例一律使用占位符。
- 下单动作必须经用户明确确认；取消订单路径始终可用（`cancel-order`）。
- 侧写为娱乐化演绎，不构成营养或医疗建议；餐品、价格以 MCP 实时返回为准。
