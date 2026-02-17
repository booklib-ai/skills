# Animation at Work — Chapter-by-Chapter Reference

Complete catalog of web animation concepts, techniques, and best practices
from all 5 chapters.

---

## Ch 1: Human Perception and Animation

### How Humans Perceive Motion
- The brain fills in gaps between static images to perceive fluid motion (persistence of vision)
- Animations create an illusion of life and spatial relationships in 2D interfaces
- Users perceive animated interfaces as faster and more responsive than static ones
- Motion draws attention — use this deliberately, not accidentally

### The 12 Principles of Animation (Disney)
Originally from *The Illusion of Life* by Frank Thomas and Ollie Johnston, adapted for UI:

1. **Squash and stretch** — Deformation to show weight/flexibility (limited use in UI — icon bounces, rubbery buttons)
2. **Anticipation** — Preparatory motion before main action (button shrink before expand, drawer slight pull before open)
3. **Staging** — Present ideas clearly; direct attention to the important element (dim background, spotlight focus)
4. **Straight ahead vs. pose to pose** — Drawing technique; in UI, "pose to pose" maps to keyframe animation
5. **Follow-through and overlapping action** — Not everything stops at once; stagger child elements (list items appearing in sequence)
6. **Slow in and slow out (ease in/out)** — Objects accelerate and decelerate; never use linear for UI motion
7. **Arcs** — Natural motion follows curved paths (use CSS motion paths or transform combinations)
8. **Secondary action** — Supporting motion that reinforces primary (badge bounce while drawer opens)
9. **Timing** — Number of frames/duration controls perceived weight and mood
10. **Exaggeration** — Amplify for clarity (overshoot on panel open, extra bounce on landing)
11. **Solid drawing** — 3D awareness; in UI, use shadows and transforms to create depth
12. **Appeal** — Pleasing, engaging quality; animations should feel appropriate for the brand

### Timing and Spacing
- **Timing** = total duration of animation
- **Spacing** = distribution of motion within that duration (controlled by easing)
- Fast timing + uniform spacing = snappy, lightweight
- Slow timing + varied spacing = heavy, dramatic
- Same duration with different easing = completely different feel

### Easing Functions
- **Linear**: Constant speed — robotic, only for continuous motion (progress bars, spinners)
- **Ease-in (slow in)**: Starts slow, ends fast — best for elements **leaving** the screen
- **Ease-out (slow out)**: Starts fast, ends slow — best for elements **entering** the screen
- **Ease-in-out**: Slow start and end — best for elements **repositioning** on screen
- **Cubic-bezier**: Custom curves for brand-specific personality
- **Steps()**: Discrete jumps — for sprite animations or typewriter effects

### Duration Guidelines
- **Micro-interactions**: 100–200ms (button feedback, toggle, hover)
- **State transitions**: 200–500ms (panel open, tab switch, modal)
- **Page transitions**: 300–500ms (route changes, full view swaps)
- **Demonstrations**: 500ms–1s (onboarding, tutorials)
- **Rule of thumb**: If a user initiates the action, keep it under 300ms; if the system initiates, up to 500ms is OK
- **Never**: Exceed 1s for functional animation; users perceive it as broken/slow

### Perception Thresholds
- **100ms**: Perceived as instantaneous; ideal for direct feedback
- **1 second**: Limit of feeling continuous; user starts to lose focus
- **10 seconds**: Maximum before attention wanders; must show progress indicator

---

## Ch 2: Patterns and Purpose

### The Five Animation Patterns

**1. Transitions**
- Change between two states or views in the system
- Examples: page navigation, modal open/close, tab switching, accordion expand/collapse
- Both states exist; animation shows the journey between them
- Should convey spatial relationship (where the new view "came from")
- Maintain context: user should understand they're in the same app

**2. Supplements**
- Add or remove elements from the current view without changing the view itself
- Examples: toast notification appearing, list item added, dropdown menu opening, tooltip showing
- The view remains; new elements join or leave it
- Often use enter/exit patterns: slide + fade in, slide + fade out
- Key difference from transitions: the "stage" stays the same

**3. Feedback**
- Acknowledge that the system received a user's action
- Examples: button press animation, form validation shake, successful submit checkmark, pull-to-refresh
- Must be immediate (under 200ms) — user needs instant confirmation
- Can be subtle (color flash) or prominent (success animation) depending on action importance
- Missing feedback makes interfaces feel broken or unresponsive

**4. Demonstrations**
- Show how something works or draw attention to a feature
- Examples: onboarding walkthroughs, feature discovery pulses, interactive tutorials, gesture hints
- Can be longer duration (up to several seconds) since they're instructional
- Should be skippable — not everyone needs the tutorial
- Diminishing returns: show once or twice, then stop
- Often used on first use, then hidden

**5. Decorations**
- Purely aesthetic, no functional purpose
- Examples: parallax backgrounds, floating particles, idle character animations, gradient shifts
- **Use sparingly**: They add visual interest but no information
- Can become annoying with repeated exposure
- Increase page weight and battery drain
- Should be the first thing removed for performance or accessibility

### Choosing the Right Pattern
- Ask: "What is this animation communicating?"
- If it communicates a state change → Transition
- If it communicates an element entering/leaving → Supplement
- If it communicates acknowledgment → Feedback
- If it communicates how-to → Demonstration
- If it communicates nothing functional → Decoration (consider removing)

### Stateful Animations
- Animations tied to application state (e.g., loading → loaded → error)
- Define motion for each state transition
- Consider all paths: forward, backward, error, timeout
- Loading states: provide progress animation to reduce perceived wait time

---

## Ch 3: Anatomy of a Web Animation

### CSS Transitions
```css
.element {
  transition: property duration easing delay;
}
```
- Animate between two states (A → B) triggered by state change (hover, class toggle, media query)
- **Properties**: Can animate most CSS properties, but only `transform` and `opacity` are performant
- **Shorthand**: `transition: all 300ms ease-out` or specify per property
- **Multiple properties**: `transition: transform 300ms ease-out, opacity 200ms ease-in`
- **Delay**: Useful for staggering (each list item delayed by N * 50ms)
- **Limitation**: Only two states; no looping; no mid-animation keyframes

### CSS Animations
```css
@keyframes slidein {
  from { transform: translateX(-100%); opacity: 0; }
  to   { transform: translateX(0); opacity: 1; }
}
.element {
  animation: slidein 300ms ease-out forwards;
}
```
- Define keyframes at arbitrary points (0%, 25%, 50%, 100%)
- **animation-iteration-count**: `infinite` for looping, number for finite
- **animation-direction**: `normal`, `reverse`, `alternate` (ping-pong)
- **animation-fill-mode**: `forwards` (stay at end), `backwards` (start at first keyframe), `both`
- **animation-play-state**: `running` or `paused` (toggle via JS)
- **Use for**: Loading spinners, attention pulses, multi-step sequences, any animation that starts automatically

### Web Animations API (WAAPI)
```js
const animation = element.animate(keyframes, options);
```
- Combines CSS animation performance with JavaScript control
- **Keyframes**: Array of keyframe objects or object with array properties
- **Options**: `duration`, `easing`, `iterations`, `direction`, `fill`, `delay`
- **Playback control**: `animation.play()`, `.pause()`, `.reverse()`, `.cancel()`, `.finish()`
- **Timeline scrubbing**: `animation.currentTime = value` — scrub to specific point
- **Promises**: `animation.finished` returns a Promise — chain sequential animations
- **Playback rate**: `animation.playbackRate` — speed up, slow down, or reverse

**WAAPI vs CSS Animations**:
| Feature | CSS Animations | WAAPI |
|---------|---------------|-------|
| Declarative | Yes | No (imperative) |
| Play/pause | Via play-state | Via .play()/.pause() |
| Reverse | Via direction | Via .reverse() |
| Scrub/seek | No | Via .currentTime |
| Chain sequences | No | Via .finished promise |
| Dynamic values | No (static keyframes) | Yes (JS-generated) |
| Performance | Compositor thread | Compositor thread |

### SVG Animation
- **SMIL** (deprecated but still supported): `<animate>`, `<animateTransform>`, `<animateMotion>`
- **CSS on SVG**: Apply CSS transitions/animations to SVG elements (limited to presentation attributes)
- **WAAPI on SVG**: Full animation control on SVG DOM elements
- **Use for**: Icon animations, character animation, path-based motion, morphing shapes

### Canvas Animation
- **2D Canvas**: `requestAnimationFrame` loop, manual drawing each frame
- Pros: Total control, handles thousands of objects efficiently
- Cons: No DOM, no accessibility, no CSS styling, must handle everything manually
- **Use for**: Particle systems, data visualizations with many points, game-like animations

### WebGL
- GPU-accelerated 3D and 2D rendering
- Libraries: Three.js, PixiJS, Babylon.js
- **Use for**: 3D effects, complex particle systems, immersive experiences
- Cons: Heavy, steep learning curve, accessibility challenges

### Performance Architecture
**The Rendering Pipeline**:
1. **JavaScript** — Run scripts, modify DOM/styles
2. **Style** — Calculate computed styles
3. **Layout** — Calculate positions and sizes (expensive!)
4. **Paint** — Fill in pixels for each layer
5. **Composite** — Combine layers on GPU

**Composite-only animations** skip Layout and Paint:
- `transform: translate()`, `scale()`, `rotate()`, `skew()`
- `opacity`
- Everything else triggers Layout or Paint

**`will-change` property**:
```css
.element { will-change: transform, opacity; }
```
- Promotes element to its own compositor layer
- Browser can optimize ahead of time
- **Warning**: Overuse wastes GPU memory; only apply right before animation starts, remove after

**RAIL Performance Model**:
- **Response**: Handle input within 100ms
- **Animation**: Produce frame within 16ms (60fps) — only 10ms budget after browser overhead
- **Idle**: Use idle time for deferred work in 50ms chunks
- **Load**: Deliver content within 1000ms

---

## Ch 4: Communicating Animation

### Why Communication Matters
- Animations are easy to miscommunicate — "make it slide in" means different things to different people
- Without shared language, developers implement something different from what designers intended
- Animation specs are often omitted from design handoff, leading to guesswork

### Storyboards
- Series of static frames showing key poses in an animation sequence
- Borrowed from film/animation industry
- **Use for**: Complex multi-step animations, page transitions, onboarding flows
- **Include**: Key frames, notes about timing/easing, interaction triggers
- Simple pencil sketches are fine — fidelity doesn't matter, communication does
- Number each frame, add annotations for timing and easing

### Motion Comps (Motion Compositions)
- Actual animated prototypes showing the real motion
- Created in tools like After Effects, Principle, Framer, or CSS/JS prototypes
- **Use for**: Precise timing communication, client presentations, developer handoff
- More accurate than storyboards but more time-consuming to create
- Can export as video/GIF for sharing, or as code for implementation

### Animation Spec Documentation
What to include in handoff:
- **Trigger**: What initiates the animation (click, hover, page load, scroll position)
- **Properties**: Which CSS properties change (transform, opacity, etc.)
- **Duration**: Exact timing in milliseconds
- **Easing**: Named function or cubic-bezier values
- **Delay**: If staggered or delayed
- **States**: Start state, end state, and any intermediate keyframes
- **Accessibility**: Reduced-motion alternative behavior

### Shared Vocabulary
Establish team-wide terminology:
- Use the 5 animation patterns (transition, supplement, feedback, demonstration, decoration) as shared language
- Name recurring animations in your system (e.g., "drawer-open", "toast-enter", "card-flip")
- Document in a motion design system alongside your component library

### Motion Design Systems
- Extension of your design system specifically for animation
- Define: standard durations, standard easings, standard patterns per component
- Token-based: `--duration-fast: 150ms`, `--duration-medium: 300ms`, `--ease-enter: ease-out`
- Component-level: "Modal opens with 300ms ease-out, closes with 200ms ease-in"
- Reduces inconsistency and speeds up development

---

## Ch 5: Best Practices

### Accessibility

**Vestibular Disorders**
- Affect ~35% of adults over 40 to some degree
- Triggered by: parallax scrolling, zooming animations, large-scale motion, spinning
- Symptoms: dizziness, nausea, disorientation
- Severity ranges from mild discomfort to debilitating

**`prefers-reduced-motion` Media Query**
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```
- Respects OS-level accessibility setting (macOS: Reduce Motion; Windows: Show animations)
- **Approach 1**: Remove all animations (nuclear option above)
- **Approach 2**: Replace problematic animations with safe alternatives (preferred)
- **Safe motions**: Opacity fades, color changes, small-scale transforms
- **Problematic motions**: Parallax, zooming, spinning, large-distance slides, auto-playing

**WCAG Guidelines**
- Flashing content must not flash more than 3 times per second (seizure risk)
- Auto-playing animations must have pause/stop mechanism
- Motion that starts automatically and lasts >5 seconds must be pausable
- Content must not cause seizures or physical reactions

**Implementing Accessible Animation**:
1. Start with `prefers-reduced-motion` media query on all animations
2. Provide alternative non-motion presentation for key content
3. Never rely on animation alone to convey information
4. Auto-playing content must be pausable
5. Test with motion settings turned off — your UI should still be fully usable

### Performance Best Practices

**Property Tiers**:
- **Tier 1 (Composite)**: `transform`, `opacity` — GPU-accelerated, skip layout/paint
- **Tier 2 (Paint)**: `color`, `background-color`, `box-shadow` — skip layout but trigger paint
- **Tier 3 (Layout)**: `width`, `height`, `margin`, `padding`, `top/left` — trigger full pipeline

**Optimization Strategies**:
- Animate only Tier 1 properties whenever possible
- Use `transform: translateX()` instead of `left`
- Use `transform: scale()` instead of `width/height`
- Use `opacity` instead of `visibility` or `display`
- Batch DOM reads and writes (avoid layout thrashing)
- Use `will-change` sparingly and remove after animation completes
- Avoid animating during page load — defer to idle time
- Use `requestAnimationFrame` for JavaScript-driven animations

**Testing Performance**:
- Chrome DevTools Performance panel — look for long frames (>16ms)
- Paint flashing overlay — identify unexpected repaints
- Layer borders — check compositor layer count (too many = memory waste)
- Test on real mobile devices — dev machines hide performance problems
- Throttle CPU in DevTools to simulate slower hardware

### Team Workflow

**Integrating Animation into Design Process**:
1. **Discovery**: Identify where animation adds value (don't animate everything)
2. **Design**: Create storyboards or motion comps for complex animations
3. **Spec**: Document trigger, properties, duration, easing, accessibility
4. **Implement**: Build using appropriate technology (CSS, WAAPI, library)
5. **Review**: Test performance, accessibility, and purpose alignment
6. **Maintain**: Document in motion design system for consistency

**Motion Design System Components**:
- **Tokens**: Duration scale, easing functions, delay increments
- **Patterns**: Standard enter/exit/transition behaviors per component type
- **Guidelines**: When to animate, when not to, accessibility requirements
- **Tools**: Approved libraries, prototyping tools, testing procedures

**Common Team Pitfalls**:
- Designer creates beautiful animation that tanks performance
- Developer implements animation without knowing intended timing/easing
- No one tests with reduced-motion setting enabled
- Animation added at the end of sprint as "polish" without proper design
- No shared motion language — everyone describes motion differently

### When NOT to Animate
- When the animation adds no information or functional value
- When the user has indicated they prefer reduced motion
- When the animation would delay the user from completing their task
- When it would trigger accessibility issues (seizures, vestibular)
- When performance would suffer on target devices
- When it would be distracting during focused work (data entry forms, reading)
- When the same content would be shown with or without the animation (meaningless decoration)

### Resources and Tools
- **Cubic-bezier playground**: cubic-bezier.com for custom easing curves
- **Chrome DevTools**: Performance panel, Animations panel, rendering tab
- **Can I Use**: Check browser support for animation features
- **WAAPI Polyfill**: web-animations-js for older browser support
- **Libraries**: GreenSock (GSAP), Anime.js, Lottie (After Effects to web), Framer Motion (React)
