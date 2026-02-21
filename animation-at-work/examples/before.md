# Before

A CSS animation on a navigation drawer that animates `width` and `height` (layout-triggering properties) with `linear` easing and a 1.5-second duration, with no `prefers-reduced-motion` support.

```css
.nav-drawer {
  width: 0;
  height: 0;
  overflow: hidden;
  background-color: #1a1a2e;
}

.nav-drawer.open {
  width: 280px;
  height: 100vh;
  /* Animates layout properties — forces browser to recalculate layout
     on every frame, causing jank on low-powered devices */
  transition: width 1.5s linear, height 1.5s linear;
}

.nav-drawer .menu-item {
  opacity: 0;
  /* Also animates layout property margin */
  margin-left: -280px;
  transition: opacity 1.5s linear, margin-left 1.5s linear;
}

.nav-drawer.open .menu-item {
  opacity: 1;
  margin-left: 0;
}

/* No prefers-reduced-motion support — users with vestibular
   disorders experience the full 1.5s sweep animation */
```
