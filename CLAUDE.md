# CLAUDE.md - Project Guidelines for Claude Code

## Project Overview

This project creates logic puzzle problems (思考パズル問題) for the Japan Civil Aviation College entrance exam "総合Part I" section. Problems test logical reasoning, spatial visualization, pattern recognition, and mathematical thinking.

## Language

- Primary language: **Japanese (日本語)**
- All problem content, explanations, and documentation should be in Japanese

## Problem Specifications

### Standard Problem (問題1)
- Points: 6点
- Time limit: 3 minutes
- Difficulty: ★★★★★ (5 stars)

### High-Difficulty Problem (問題2)
- Points: 6点
- Time limit: 5 minutes
- Difficulty: ★★★★★★★★ (8 stars)
- Must be a harder variant derived from Problem 1

## Required Workflow

1. **Design** - Choose problem type: constraint satisfaction, cryptography, spatial reasoning, pattern recognition, or data analysis
2. **Python Verification** - Validate solution uniqueness with brute-force enumeration
3. **Randomize Answer Position** - Run `python3 -c "import random; print(random.randint(1, 5))"` to determine correct answer number (1-5)
4. **Create HTML** - Use `template.html` as base, only edit between marked sections

## File Structure

```
template.html    - HTML template (DO NOT modify structure/styles)
難易度基準.md    - Difficulty standards reference
README.md        - Full project documentation
```

## HTML Guidelines

- **Template**: Always use `template.html` as base
- **Edit Zone**: Only modify between `<!-- ここから問題セクション -->` and `<!-- 解答・解説セクション -->`
- **Colors**: Black and white only (grayscale allowed)
- **Output naming**: `航大思考{N}.html`

## SVG Coordinate Guidelines

When creating SVG graphics:

1. **Document coordinate system** in comments before each SVG:
```html
<!--
座標系定義:
- 原点: (50, 250)
- X軸: 右方向, 1単位=30px
- Y軸: 上方向, 1単位=40px (SVGは下が正なので減算)
-->
```

2. **Verify coordinates** with Python after creation
3. **Ensure axis labels match** graph element positions

## Python Verification Template

```python
def verify_solution():
    """全ての可能性を検証し、唯一解を確認"""
    valid_solutions = []
    # Enumerate all possibilities
    # Apply constraints
    # Verify uniqueness
    assert len(valid_solutions) == 1, f"解が{len(valid_solutions)}個存在"
    return valid_solutions[0]
```

## Quality Checklist

- [ ] Python verification confirms unique solution
- [ ] All constraints are necessary for solution
- [ ] No contradicting constraints
- [ ] SVG coordinates match intended positions
- [ ] Table data matches calculations
- [ ] Answer position randomized (not manually chosen)
- [ ] Solvable in 170-310 seconds
- [ ] Requires multi-step reasoning

## Things to Avoid

- Visual contradictions (graph values vs. text values)
- Obvious solutions
- Requiring specialized aviation knowledge to solve
- Skipping Python verification
- Manually selecting answer positions (especially 1 or 5)
