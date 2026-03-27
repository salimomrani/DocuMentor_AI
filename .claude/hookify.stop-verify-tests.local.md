---
name: stop-verify-tests
enabled: true
event: stop
pattern: .*
action: warn
---

⚠️ **Avant de terminer — TDD check**

As-tu :
- [ ] Lancé les tests et vérifié qu'ils passent ?
- [ ] Lancé le lint ?
Iron law : aucun commit sans tests verts.
