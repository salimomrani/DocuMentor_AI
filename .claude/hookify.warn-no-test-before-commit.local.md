---
name: warn-no-test-before-commit
enabled: true
event: bash
pattern: git\s+commit
action: warn
---

⚠️ **Commit détecté — tests lancés ?**

Avant de committer, confirme :
Iron law : aucun commit sans tests verts.
