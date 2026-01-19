# 納品！和歌山産みかん (β版 / Pyxel Only)

**Delivery! Wakayama Mikan**
Pyxelのみで動作する、フルーツ合体＋フレッシュ（鮮度）＋腐り（毒）システムのスコアアタックゲーム。

> 重要：このβ版は「バランス調整できるプロトタイプ」です。
> 物理は **Pyxel上で自作の簡易2D円衝突＆重力** を実装します（外部物理エンジン不使用）。

---

## Overview

上から果物（円）を落として、同じ種類同士をくっつけて合体させ、最終段階の「みかん」を納品してスコアを伸ばします。

このゲームの核は **フレッシュ値（鮮度）**：

- 落とす前に、次の果物のフレッシュ値が **数値で見える**
- 落とした後は数値が見えず、**キラキラ等のエフェクトだけで推測**
- フレッシュは時間で減るが、**合体するとフレッシュ値が合算（＋ボーナス）**され、復活ルートがある
- 腐ったみかんが増えるほど、**合計フレッシュ値が割合で目減り**してスコアが落ちる（毒）

---

## How to Play

### Run
Python 3.10+ 推奨（3.9+でも可）

\`\`\`bash
pip install -r requirements.txt
python main.py
\`\`\`

### Controls
- **Mouse Move**: 落下位置を移動
- **Left Click**: 投下
- **ESC**: Pause / Resume
- **F1**: β調整パネル ON/OFF
- **F5**: 現在設定を保存（\`config/game_config.json\` へ）
- **F9**: デフォルトへリセット（保存はしない）
- **S**: 出荷して終了（いつでもOK）

### Objective
1. 同じ種類を合体させて上位の果物を作る
2. 最終段階「みかん」をできるだけ多く納品する
3. **高フレッシュで納品**してスコアを伸ばす
4. 腐ったみかんが混じると **合計フレッシュが目減り**して全体のスコアが落ちる

### Game End Conditions
- **JAMMED**: 赤いラインより上に果物が一定時間残った
- **SHIP OUT**: いつでも「出荷して終了」できる（スコア確定）

---

## Game Mechanics

### Fruit Stages (6 stages)
1. 梅 (Ume)
2. 柿 (Kaki)
3. 桃 (Momo)
4. ぶどう (Budou)
5. デコポン (Dekopon)
6. みかん (Mikan) - 最終段階（生成された瞬間に納品され盤面から消える）

---

## Freshness System (フレッシュ値)

### Freshness Basics
- 各果物は \`fresh\`（0〜fresh_max）を持つ
- **生成時（次玉の時点）にランダムで決定**
- 落とす前：数値で表示（例：72）
- 落とした後：数値は非表示、**見た目（キラキラ/発光/くすみ）だけで表現**
- フレッシュは時間で減衰（段階が高いほど減りやすくできる）

### Decay (減衰)
\`fresh = max(0, fresh - decay_rate(stage) * dt)\`

### Merge Recovery (合体で合算＝復活ルート)
同種合体で生成される果物のフレッシュ値：
\`fresh_new = clamp(0, fresh_cap, fresh_a + fresh_b + merge_bonus)\`

---

## Rot Mechanics (腐ったみかん＝毒)

### Rotten判定（みかん納品時）
みかんが納品される瞬間の \`fresh_mikan\` がしきい値以下なら腐り扱い：
- \`fresh_mikan <= rotten_threshold\` → 腐ったみかん

### 腐りダメージ（合計フレッシュ値を割合で削る）
腐ったみかんが \`rotten_count\` 個あるとき：

\`effective_fresh = fresh_sum × (1 - rot_rate)^rotten_count\`

---

## Scoring (スコア)

\`\`\`text
effective_fresh = fresh_sum × (1 - rot_rate)^rotten_count
score = effective_fresh × fresh_to_score + delivered_count × count_bonus
\`\`\`

---

## β Version Features

### Adjustment Panel (F1)
β版はバランス検証用に、ゲーム内でパラメータを変更可能。

- UP/DOWN: パラメータ選択
- LEFT/RIGHT: 値の調整
- F5: 設定を保存
- F9: デフォルトに戻す

---

## Technical Stack

- **Pyxel**: Rendering / Input / Audio
- **Custom Physics**: 2D circle collision, gravity, bounce

---

## File Structure

\`\`\`
mikan_pyxel/
├── main.py                     # エントリーポイント
├── requirements.txt            # 依存パッケージ
├── game/
│   ├── __init__.py
│   ├── app.py                  # Pyxel起動・シーン管理
│   ├── scene_title.py          # タイトル画面
│   ├── scene_play.py           # ゲームプレイ
│   ├── scene_result.py         # リザルト画面
│   ├── config.py               # config読み書き
│   ├── scoring.py              # スコア計算
│   ├── fruit.py                # Fruit定義
│   ├── physics.py              # 簡易円物理
│   ├── merge.py                # 合体判定
│   └── ui_beta.py              # β調整パネル
├── config/
│   └── game_config.json        # 設定ファイル
├── assets/
│   ├── sprites/
│   ├── sfx/
│   └── LICENSE_ASSETS.txt
└── docs/
    └── SPEC_BETA.md
\`\`\`

---

## Testing Focus (β)

1. 同種接触で合体（多重発火しない）
2. 落下前だけフレッシュ数値表示
3. 落下後はエフェクトのみ（数値非表示）
4. フレッシュ減衰がフレームレートに依存しない
5. 合体でフレッシュ合算＋ボーナス
6. みかん生成で自動納品（盤面から消える）
7. 腐りダメージ（rot_rate）を上げるとスコアが明確に落ちる
8. 出荷でいつでも終了できる
9. config保存→再起動で反映される

---

## Future Enhancements (Post-β)
- 愛媛イベント（妨害/渋滞/逆転ボーナスなど）
- エフェクト強化、SE/BGM
- スコア履歴/ランキング（ローカル保存）
- 配布用EXE化（PyInstaller onefile）

---

**Game Version**: β (Balance Prototype)
**Last Updated**: 2026-01-19
**License**: MIT (see LICENSE for details)
