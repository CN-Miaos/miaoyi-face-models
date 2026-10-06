# miaoyi-face 模型包

「喵译·面对面」（Android 包名 `com.miaos.miaoyi`）**首次运行下载**所需的离线模型，供 App 内直接下载与校验。
本仓只放模型资产，**不含任何 App 代码**。

- 下载总量 ≈ **1.10 GB**（zip）｜解压后 ≈ **1.57 GB**
- 清单（程序读取）：`releases/download/v1.0/models.json`（清单 `version` **1.2.0**；release tag 保持 `v1.0` 不变，App 的 `defaultManifestUrl` 无需改）
- 装机位置：`/storage/emulated/0/Android/data/com.miaos.miaoyi/files/models/`（`getExternalStorageDirectory()/models`）

## v1.0 资产清单

| zip | 解压到 | 内容 | 上游来源 | 许可 |
|---|---|---|---|---|
| `asr-zh.zip` | `models/asr-zh/` | 中文+英语 流式 ASR（中英双语 zipformer，transducer，int8；052 起英语共用此包） | k2-fsa/sherpa-onnx 官方模型发布 | Apache-2.0 |
| `asr-es.zip` | `models/asr-es/` | 西语流式 ASR（transducer） | k2-fsa/sherpa-onnx 官方模型发布 | Apache-2.0 |
| `vad.zip` | `models/vad/` | Silero VAD（`silero_vad.onnx`） | snakers4/silero-vad，经 sherpa-onnx 分发 | MIT |
| `denoise.zip` | `models/denoise/` | GTCRN 语音降噪（`gtcrn_simple.onnx`） | k2-fsa/sherpa-onnx | Apache-2.0 |
| `mt-zh-en.zip` | `models/mt/zh-en/` | 中→英 机器翻译（Marian，int8） | `Helsinki-NLP/opus-mt-zh-en` | CC-BY-4.0 |
| `mt-en-es.zip` | `models/mt/en-es/` | 英→西 机器翻译（Marian，int8） | `Helsinki-NLP/opus-mt-en-es` | Apache-2.0 |
| `mt-es-zh.zip` | `models/mt/es-zh/` | 西→中 机器翻译（Marian，int8） | `Helsinki-NLP/opus-tatoeba-es-zh` | Apache-2.0 |
| `mt-en-zh.zip` | `models/mt/en-zh/` | 英→中 机器翻译（Marian，int8；052 新增） | 原作 `Helsinki-NLP/opus-mt-en-zh`（int8 转换：`Xenova/opus-mt-en-zh`） | Apache-2.0 |
| `mt-es-en.zip` | `models/mt/es-en/` | 西→英 机器翻译（Marian，int8；052 新增） | 原作 `Helsinki-NLP/opus-mt-es-en`（int8 转换：`Xenova/opus-mt-es-en`） | Apache-2.0 |
| `tts-zh.zip` | `models/tts/zh/` | 中文语音合成（VITS fp32；2026-10-06 由 piper `xiao_ya` 换为 MeloTTS） | MeloTTS（https://github.com/myshell-ai/MeloTTS） | **MIT** |
| `tts-es.zip` | `models/tts/es/` | 西语语音合成（piper VITS，int8，含 `espeak-ng-data/`） | piper 音色 `es_MX-claude-high` | 训练数据 apache-2.0 |
| `tts-en.zip` | `models/tts/en/` | 英语语音合成（piper VITS medium，含 `espeak-ng-data/`；051 新增） | piper 音色 `en_US-libritts_r-medium`（k2-fsa/sherpa-onnx 分发） | CC-BY-4.0 |

### 中文音色许可（已于 2026-10-06 解决 ✓）
原音色 `zh_CN-xiao_ya-medium`（训练数据 **Data Baker BZNSYP**，模型卡标注 **「Non-commercial use」**）
**已替换**为 `vits-melo-tts-zh_en`（**MeloTTS，MIT**，包内自带 LICENSE 全文）。

- 包结构不变（`zh/model.onnx` + `zh/tokens.txt` + `zh/lexicon.txt`），**App 侧零改动**。
- 体积：15.9 MB（zip）→ **152.1 MB**（zip）/ 169.1 MB（解压后）。
- 清单版本 **1.2.0 → 1.3.0**，`tts-zh` 的 `sha256` 已更新 → 已装设备会重新下载。
- 西语 `es_MX-claude-high` 训练数据集为 apache-2.0，无此限制。

### 本项目的改动
- 机器翻译 中→西/西→中/中→英/英→西 四个方向由本项目做 **int8 动态量化**（原模型为 fp32），体积与内存显著下降，精度经真机回环验证；英→中/西→英（052 新增）直接采用 **Xenova 上游 int8 导出**（`*_quantized.onnx` 落地改名 `*_int8.onnx`），译文经 PC 与真机验证。
- 中文 ASR 使用上游 int8 版本；西语 ASR 使用上游 fp32 版本（按上游发布为准）。
- 其余文件为上游原样。

## 用法

App 内会自动读取清单、逐个下载 → 校验 `sha256` → 解压 → 写入 `.installed/<id>.json` 标记。
手动安装（adb / 文件管理器）——把各 zip 的解压内容按上表落位即可，例如：

```bash
adb push asr-zh asr-es vad denoise  .../files/models/
adb push zh-en en-es es-zh en-zh es-en .../files/models/mt/
adb push zh es en                    .../files/models/tts/
```

## 目录结构约定

```
models/
  asr-zh/  asr-es/  vad/  denoise/
  mt/{zh-en,en-es,es-zh,en-zh,es-en}/
  tts/{zh,es,en}/
  .installed/        # 每个包装好后由 App 写入的标记（不进仓）
  .cache/            # 下载中的 .part（不进仓）
```

## 许可与出处

**各组件的完整许可声明见 [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md)（含 GPL-3.0 组件声明、CC-BY-4.0 署名与改动说明），许可全文见 [`LICENSES/`](LICENSES/)。**
模型版权归各自上游所有，许可以上游模型页标注为准（见上表）。本仓仅为再分发与校验（`sha256`）之便。
