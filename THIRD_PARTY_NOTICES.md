# 第三方组件与许可声明（THIRD_PARTY_NOTICES）

**仓库**：`CN-Miaos/miaoyi-face-models` —— 「喵译·面对面」App 首次运行所需离线模型包的再分发仓
**盘点日期**：2026-10-06

本仓**仅再分发**上游模型资产（为 App 内下载与 `sha256` 校验之便），**不含任何 App 代码**。
各模型著作权归其各自权利人所有，许可如下。许可**完整文本**见本仓 [`LICENSES/`](LICENSES/) 目录。

---

## ⚠️ 一、GNU GPL-3.0 组件声明（重要）

本仓分发的 **`tts-es.zip`** 与 **`tts-en.zip`** 内均包含 **eSpeak NG** 的数据文件目录
`espeak-ng-data/`（各 340+ 个文件）。

| 项 | 内容 |
|---|---|
| 许可 | **GNU General Public License, version 3 or later** |
| 在包内位置 | `tts-es.zip` → `models/tts/es/espeak-ng-data/` |
| 本项目是否修改 | **否，原样分发。** |
| 许可全文 | [`LICENSES/GPL-3.0-or-later.txt`](LICENSES/GPL-3.0-or-later.txt) |

**注意**：eSpeak NG 的**引擎代码**同样被静态编译进 App 的原生库 `libsherpa-onnx-c-api.so`。
该部分及其对应源码获取方式，详见 App 仓的 `THIRD_PARTY_NOTICES.md`。

### 对应源码获取方式

- 本项目所用版本对应提交：`ed530aa113046142eb5115cf2fc9157854d0ffe1`（`csukuangfj/espeak-ng`）
  - https://github.com/csukuangfj/espeak-ng/tree/ed530aa113046142eb5115cf2fc9157854d0ffe1
  - 归档 zip：https://github.com/csukuangfj/espeak-ng/archive/ed530aa113046142eb5115cf2fc9157854d0ffe1.zip
    （SHA256 `e4e262cbe34f7fe21f91f1ba3397f2728e1f30eafbae7853f2b753a9ed13f0dd`）
- 上游项目：https://github.com/espeak-ng/espeak-ng

---

## 二、资产清单与许可（清单 v1.2.0，共 12 个包）

| zip | 内容 | 上游来源 | 许可 |
|---|---|---|---|
| `asr-zh.zip` | 中英流式 ASR（zipformer transducer, int8） | k2-fsa/sherpa-onnx 官方模型发布 | Apache-2.0 |
| `asr-es.zip` | 西语流式 ASR（transducer） | k2-fsa/sherpa-onnx 官方模型发布 | Apache-2.0 |
| `vad.zip` | Silero VAD | https://github.com/snakers4/silero-vad （经 sherpa-onnx 分发） | MIT |
| `denoise.zip` | GTCRN 语音降噪 | https://github.com/k2-fsa/sherpa-onnx | Apache-2.0 |
| `mt-zh-en.zip` | 中→英 机器翻译（Marian, **本项目 int8 量化**） | https://huggingface.co/Helsinki-NLP/opus-mt-zh-en | **CC-BY-4.0** |
| `mt-en-es.zip` | 英→西 机器翻译（Marian, **本项目 int8 量化**） | https://huggingface.co/Helsinki-NLP/opus-mt-en-es | Apache-2.0 |
| `mt-es-zh.zip` | 西→中 机器翻译（Marian, **本项目 int8 量化**） | https://huggingface.co/Helsinki-NLP/opus-tatoeba-es-zh | Apache-2.0 |
| `mt-en-zh.zip` | 英→中 机器翻译（Marian, **采用上游 int8 导出**） | 原作 https://huggingface.co/Helsinki-NLP/opus-mt-en-zh ；int8 转换 https://huggingface.co/Xenova/opus-mt-en-zh | Apache-2.0 |
| `mt-es-en.zip` | 西→英 机器翻译（Marian, **采用上游 int8 导出**） | 原作 https://huggingface.co/Helsinki-NLP/opus-mt-es-en ；int8 转换 https://huggingface.co/Xenova/opus-mt-es-en | Apache-2.0 |
| `tts-zh.zip` | 中文语音音色 | **待替换**：当前为开发期临时音色 `zh_CN-xiao_ya-medium`（训练数据 DataBaker BZNSYP，标注 Non-commercial）；**目标替换为 MeloTTS（MIT）** | MIT（替换后） |
| `tts-es.zip` | 西语语音音色 + `espeak-ng-data/` | piper 音色 `es_MX-claude-high` | 数据集 apache-2.0；`espeak-ng-data/` 为 **GPL-3.0-or-later**（见 §一） |
| `tts-en.zip` | 英语语音音色 + `espeak-ng-data/` | piper 音色 `en_US-libritts_r-medium`（经 k2-fsa/sherpa-onnx 分发） | CC-BY-4.0；`espeak-ng-data/` 为 **GPL-3.0-or-later**（见 §一） |

### 改动说明

- **`mt-zh-en`（CC-BY-4.0）**：本仓将原模型由 fp32 转换为 **int8 动态量化**格式，以降低体积与内存占用；
  **未改变模型结构**。（CC-BY-4.0 §3(a)(1)(B) 要求指明改动）
- **`mt-en-es`、`mt-es-zh`（Apache-2.0）**：同上做了 int8 动态量化。
- **`mt-en-zh`、`mt-es-en`**：直接采用 Xenova 上游的 int8 导出（落地时仅重命名文件），本项目未做进一步改动。
- 其余文件为上游原样，未做修改。

---

## 三、许可文本

| 许可 | 文件 |
|---|---|
| Apache License 2.0 | [`LICENSES/Apache-2.0.txt`](LICENSES/Apache-2.0.txt) |
| MIT License | [`LICENSES/MIT.txt`](LICENSES/MIT.txt) |
| BSD 3-Clause License | [`LICENSES/BSD-3-Clause.txt`](LICENSES/BSD-3-Clause.txt) |
| Creative Commons Attribution 4.0 International | [`LICENSES/CC-BY-4.0.txt`](LICENSES/CC-BY-4.0.txt) |
| GNU GPL v3.0 or later | [`LICENSES/GPL-3.0-or-later.txt`](LICENSES/GPL-3.0-or-later.txt) |

---

## 四、勘误记录

| 日期 | 内容 |
|---|---|
| 2026-10-06 | **修正四处许可记录错误**：`opus-mt-en-es`、`opus-tatoeba-es-zh`、`opus-mt-en-zh`、`opus-mt-es-en` 的实际许可均为 **Apache-2.0**（此前 README 中误记为 CC-BY-4.0）；经 HuggingFace API 权威字段核实（原始上游 `Helsinki-NLP/*` 均标 apache-2.0）。 |
| 2026-10-06 | 补充 CC-BY-4.0 要求的「改动说明」（int8 量化）。 |
| 2026-10-06 | 补充 eSpeak NG（GPL-3.0-or-later）声明与对应源码获取方式。 |
| 2026-10-06 | 本声明覆盖清单 v1.2.0 全部 **12** 个包（此前记录仅覆盖 v1.0 的 9 个）。 |

---

## 五、声明

- 本文档为技术性许可盘点，**不构成法律意见**。
- 本仓仅为再分发与校验之便；各资产版权归各自权利人所有。
