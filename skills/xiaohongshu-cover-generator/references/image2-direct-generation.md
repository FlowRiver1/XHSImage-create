# Direct Generation (OpenAI / Gemini)

本说明用于在完成封面策划后，直接生成海报图片，减少复制提示词到第三方平台的步骤。

## 1) 前置条件

- 已设置其中一个环境变量：
  - `OPENAI_API_KEY`（ChatGPT Image / image2.0 路线）
  - `GEMINI_API_KEY`（Nano Banana 路线）
- 当前目录在技能目录下，或使用脚本绝对路径执行

PowerShell 设置示例：

```powershell
$env:OPENAI_API_KEY="你的OpenAIKey"
$env:GEMINI_API_KEY="你的GeminiKey"
```

也可以先复制同目录下的 `.env.example` 作为配置模板，再按你本地方式加载环境变量。

## 2) 命令模板

OpenAI（image2.0）：

```powershell
python scripts/generate_image2_cover.py --provider openai --model image2.0 --prompt-file outputs/cover_prompt.txt --output outputs/cover_openai.png --size 1024x1536
```

Gemini（Nano Banana）：

```powershell
python scripts/generate_image2_cover.py --provider gemini --model nanobanana --prompt-file outputs/cover_prompt.txt --output outputs/cover_gemini.png --aspect-ratio 3:4
```

说明：

- `--model image2.0` 会自动映射到 `gpt-image-1`
- `--model nanobanana` 会自动映射到 `gemini-2.5-flash-image`
- `--size 1024x1536` 对应 OpenAI 3:4 竖版封面
- `--aspect-ratio 3:4` 对应 Gemini 3:4 竖版封面
- 也可使用 `--prompt "..."` 直接传入提示词

## 3) 推荐执行流程

1. 先完成 A/B/C 三套方案与推荐方案  
2. 将推荐方案的中文提示词写入 `outputs/cover_prompt.txt`  
3. 选择一个 provider 执行脚本生成图片  
4. 回传输出路径给用户，并可继续做二次精修

## 4) 失败处理

- 报错 `OPENAI_API_KEY is not set` 或 `GEMINI_API_KEY is not set`：补充环境变量后重试
- 报错 HTTP 400：通常是尺寸或参数格式问题，先改为 `--size 1024x1536`
- 报错 HTTP 429：触发频控，稍后重试
- 报错 HTTP 401：检查 Key 是否有效
- 报错 `billing_hard_limit_reached`：OpenAI 账户额度或账单限制问题
- 报错 `RESOURCE_EXHAUSTED` 且 `free_tier limit: 0`：Gemini API 免费层额度不可用

## 5) 输出规范

执行后至少返回：

- 实际执行命令（可复现）
- 输出文件绝对路径
- 使用 provider 与 model
- 成功/失败状态
