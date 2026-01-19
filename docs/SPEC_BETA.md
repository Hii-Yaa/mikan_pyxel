# 納品！和歌山産みかん (β版 / Pyxel Only) - Specification

This document contains the complete specification for the beta version of the Wakayama Mikan delivery game.

Please refer to README.md for the full game description and mechanics.

## Implementation Notes

### Physics Engine
- Custom 2D circle collision detection
- Gravity-based falling
- Wall and floor bouncing with energy loss
- Simple friction for realistic stacking

### Freshness Display
- Before dropping: Numeric display with value
- After dropping: Visual effects only (sparkles, glow, dullness)
- No numeric display on dropped fruits

### Merge System
- Same type + contact = merge
- Cooldown prevents multiple rapid merges
- Freshness values sum + bonus
- Highest stage (mikan) auto-delivers

### Beta Adjustment Panel
- F1 to toggle
- Real-time parameter modification
- F5 to save current settings
- F9 to restore defaults (no save)

## Version
Beta - Balance Prototype
Last Updated: 2026-01-19
