# Category Prompt Templates

本文件提供四类封面的示范提示词骨架。  
使用方法：先判定案例分类，再将 `{}` 中占位符替换为当前脚本信息。

## 分类选择规则

- 若用户明确指定分类，严格按用户分类执行。
- 若用户给出风格偏好，按偏好映射分类：
  - 冲击感：`情绪表达` 或 `真人形象`
  - 专业感：`对比效果`
  - 创意感：`插画风格`
- 若无指定，按脚本语义自动判定，并保证三套方案至少两种分类。

## 1) 对比效果

### 触发信号

- 脚本出现“前后变化、一键优化、多视角、对照验证”等描述。

### 中文模板

小红书封面，3:4，1080x1440，对比效果风格。画面使用{对比结构}（如左右分屏/九宫格），左侧为{原始状态}，右侧为{优化结果}，中间用{连接符号}（箭头/轨迹线）强调变化路径。标题大字突出{核心结果}，副标题写{机制关键词}。背景保持{背景风格}，高对比配色{主色}+{强调色}+{中性色}，画面清晰、信息层级明确、首屏易读。

### Midjourney 英文模板

Xiaohongshu cover, vertical 3:4, 1080x1440, comparison-style layout, {comparison_structure} composition (split-screen or grid), left side shows {original_state}, right side shows {improved_result}, visual connector {connector_symbol} to highlight transformation, bold Chinese headline area for {core_outcome}, subtitle for {mechanism_keywords}, clean hierarchy, high contrast palette {primary_color} + {accent_color} + {neutral_color}, sharp and readable, social media thumbnail optimized --ar 3:4 --v 6

## 2) 情绪表达

### 触发信号

- 脚本出现“太强了、离谱、震惊、爆了、没想到”等强情绪词。

### 中文模板

小红书封面，3:4，1080x1440，情绪表达风格。主体是{人物设定}的夸张情绪特写（惊讶/兴奋/质疑），表情强烈，视线直面镜头。标题用超大字体现{争议或爆点句}，副标题补充{能力结论}。背景加入{辅助场景}，但不抢主体。整体使用{主色调}高对比，突出点击冲击力与情绪张力。

### Midjourney 英文模板

Xiaohongshu cover, vertical 3:4, 1080x1440, emotion-driven thumbnail, close-up of {character_setup} with strong expression (surprised/excited/skeptical), direct eye contact, huge Chinese headline area for {controversial_hook}, subtitle for {capability_conclusion}, supportive background {support_scene} with controlled visual noise, high-contrast {main_tone} color treatment, dramatic and click-worthy --ar 3:4 --v 6

## 3) 插画风格

### 触发信号

- 脚本偏产品机制说明，或适合用IP角色/拟物来表达能力。

### 中文模板

小红书封面，3:4，1080x1440，插画风格。使用{IP或拟物主体}作为视觉中心，体现{核心能力动作}（如自动生成、转换、加速）。标题写{结果型文案}，副标题写{能力机制}。画面采用{插画细节级别}，边缘干净，配色使用{主色}+{强调色}，确保缩略图下依然高辨识度。

### Midjourney 英文模板

Xiaohongshu cover, vertical 3:4, 1080x1440, illustration style, central character/object {ip_or_metaphor_subject} showing {core_capability_action}, bold Chinese headline area for {result_copy}, subtitle for {mechanism_copy}, stylized clean background, illustration detail level {illustration_detail_level}, high-recognition palette {primary_color} + {accent_color}, optimized for mobile thumbnail readability --ar 3:4 --v 6

## 4) 真人形象

### 触发信号

- 脚本是观点输出、职场讨论、趋势判断，强调“人”的立场与代入。

### 中文模板

小红书封面，3:4，1080x1440，真人形象风格。主体为{人物角色}半身或近景，姿态体现{情绪态度}（思考/质疑/自信）。标题大字呈现{观点句}，副标题补充{结论或收益}。背景放{场景元素}（办公室、屏幕、城市等）增强语境。整体要求人物清晰、文案强对比、信息一眼可读。

### Midjourney 英文模板

Xiaohongshu cover, vertical 3:4, 1080x1440, real-person portrait style, half-body or close-up of {persona_role}, pose and facial attitude {emotion_attitude}, strong Chinese headline area for {opinion_hook}, subtitle for {benefit_conclusion}, contextual background {context_elements} (office/screens/city), clean readability, high text contrast, realistic cinematic lighting --ar 3:4 --v 6

## 输出一致性要求

- 每套方案必须标记 `案例分类`。
- 分类、构图和提示词必须一致，禁止“分类写A，提示词却是B风格”。
- 若用户未指定分类，推荐方案优先选最能放大“引爆点”的分类。
