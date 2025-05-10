# Unity Game Development Learning Journey 🚀
Learning Unity physics, scripting, and game dev one bug at a time — with memes, color, and questionable experiments.


## 🗂️ Master Table of Contents
| Week | Key Topics Covered |
|------|---------------------|
| 1 | 🎮 Unity Setup, Game Objects, Components, Transforms, Tags, and Layers |
| 2 | 🧠 Scripting Basics, C# Integration, Input Handling, Movement Scripts |
| 3 | ⚙️ Rigidbody Physics, Mass, Damping, Collision Detection, Physics Materials |
| 4 | 🗺️ Terrain Generation from Heightmap, Scripting Terrain Textures & Trees |
| 5 | 🎥 Camera Systems, Cinemachine, 3rd Person Setup, Triggers & Collisions |
| 6 | 🧱 Object Pooling, Collectibles System, Coroutines, Health & Shields |
| 7 | 🔥 Particle Systems: Custom Fire, Snow, Gaussian Blur, Alpha, Billboard Effects |
| 8 | 🕺 Animation Basics, State Machines, Blend Trees, Root Motion, Attack Effects |

---

## Last Glass Catastrophe🔥💔

Made a vicious spike collider that ruthlessly destroys any ball daring to fall on it—until I figure out how to make them burst into glorious, dramatic explosions. Also generated a maze script… which, uh, kinda exists but isn't exactly *mazey* yet. Work in progress. 😅
![image](https://github.com/user-attachments/assets/1f1cc093-790e-4c39-8c45-0c8a72b93bd4)

## Maze Not Mazing
-When the walls exist but the logic took a day off
![image](https://github.com/user-attachments/assets/aa90d413-59a6-4a26-aafe-37db3671c028)


## Antarctica: Slippery Code Edition
–A winter wonderland of bugs, where even my logic froze. ❄️
![image](https://github.com/user-attachments/assets/429490ef-a961-42a7-b0cc-87cc1faf7609)
![image](https://github.com/user-attachments/assets/2e98fe34-2f17-446f-9216-1db1eef363fe)

![image](https://github.com/user-attachments/assets/9d8ab224-d23a-4ecd-a54b-e86bc931a175)



## 📚 Technical Concepts & Fun Tips 🛠️✨

| Week | Concept | Explanation | Fun Tip |
|------|---------|-------------|---------|
| **Week 1** | OpenGL vs. DirectX | Graphics APIs; OpenGL is cross-platform, DirectX is Windows-focused. | Choose wisely, like picking your Pokémon starter! 🔥🌱💧 |
|  | CPU vs. GPU | CPU handles logic, GPU handles rendering. | GPUs = artists, CPUs = managers. 🎨🧠 |
|  | 2D vs. 3D | 2D = points on a plane, 3D = axes and depth. | 2D: Simpler but less immersive; 3D: Welcome to the Matrix. 🕶️ |
| **Week 2** | Material Application | Drag & drop textures onto objects or assign via Mesh Renderer. | Lazy devs love drag-and-drop! 🐌🖱️ |
|  | Light Pollution Control | Avoid over-lighting; use intensity & range wisely. | If you feel blinded, so will your players. 😎💡 |
| **Week 3** | Rigidbody | Enables Unity physics; responds to gravity, forces, collisions. | Feels like bringing a rock to life. 🪨✨ |
|  | Gravity Control | Customizable in Rigidbody settings. | Zero gravity? Floating chaos unlocked! 🛸 |
|  | OnCollision vs. OnTrigger | OnCollision includes physics response; OnTrigger is for logic. | Triggers = invisible switches! 🚪✨ |
| **Week 4** | Character Controller | A specialized component for player movement. | Avoids reinventing the wheel for movement. 🛞🕹️ |
|  | SimpleMove vs. Move | SimpleMove includes time factor; Move doesn’t. | One does the math for you, one lets you suffer. 🧮😩 |
|  | Jumping Physics | Uses velocity + gravity for realistic movement. | Apply force upwards, let gravity do the rest. 🪂 |
|  | Heightmaps | Convert real-world elevation into Unity terrains. | Want to game in your backyard? Import its heightmap! 🏡🗺️ |
| **Week 5** | URP vs. Built-in Rendering | Learned to compare URP (Universal Rendering Pipeline) and Built-in rendering systems, and when to use each in a project. | Choose URP for high-quality visuals on newer hardware! 📸 |
|  | Terrain Sculpting & Layers | We manually sculpted the terrain and learned how to assemble layers through both code and mouse interaction. | Sculpt like a pro! Click Ctrl to reverse your terrain sculpting action. 🪄 |
|  | Wind Effects on Terrain & Trees | Learned to link wind with terrain details such as grass, leaves, and trees, and apply wind settings to these elements. | Make your trees sway! Add randomness to your wind to create more natural movement. 🌬️🌳 |
|  | Heightmaps | Explored creating terrains from heightmaps, adjusting resolution, and understanding scaling and elevation. | Heightmaps are like topographic art! Make sure your map’s dimensions are 2ⁿ+1. 📏🖼️ |
|  | Tree Placement | Worked on adding trees, applying colliders, and randomizing tree size for a more realistic look. | Don’t mess with tree scale in the transform settings! Adjust it in the import settings for best results. 🌲📐 |
|  | Raycasting | Explored Raycasting to view exact hit points in terrain, helpful for precise placement or collision detection. | Raycast to perfection! It’s like having X-ray vision for your game world. 🔦🎯 |
| **Week 6** | Torque vs. Force | Torque causes rotation, force causes translation. Used torque for spherical movement. | Torque = spin to win! Great for rolling characters. 🔄⚙️ |
|  | Shield Restoration | Shard collection triggers shield restoration using UI fill bars and timers. | Shields up! Gamify it with visuals for dramatic effect. 🛡️✨ |
|  | Tag vs. Layer | Tags help identify objects; layers are for grouping in rendering and physics. | Tags = name badges; Layers = VIP access groups. 🎟️📚 |
|  | LayerMask Filtering | Used in raycasting to detect only specific object types. | Raycast smarter, not harder. LayerMask your way to clarity. 🧠🔍 |
|  | Coroutine Timing | Used coroutine to spawn shards every 5 seconds with delay logic. | Time-based spawning? Coroutine is your bestie! ⏲️💙 |
|  | Event Triggers | Triggered audio, particles, and animations on shard collection. | Make interactions magical with sparkles and sounds! ✨🔊💫 |
| **Week 7** | Fire Particle Systems | Fire is created using Unity's Particle System. Parameters like lifetime, speed, emission rate, shape, and color over time simulate realistic fire. | If your fire looks like sad orange dots, tweak the alpha over lifetime curve — trust the process 🔥📈 |
| | Fire Prefab Setup | Fire effects are usually built as prefabs combining particle systems, lights, sound, and sometimes colliders (for damage or detection). | Bundle that flame! Think of it like a spicy sandwich — particles, glow, sound = 🔥 combo 🌯 |
| | Optimization Tips | Keep the particle count low, use GPU Instancing, and limit the update rate to save performance. | Fire’s cool until it burns your frame rate. Keep it classy, not laggy. 💻🔥 |
| **Week 8** | Animator Controller | The Animator controls transitions between animation states using a state machine (Idle → Walk → Jump, etc.). | The Animator is like a DJ: cueing up the next move based on the vibe. 🕺🎧 |
|  | Parameters & Transitions | Parameters (bool, float, int, trigger) control transitions. You set them in script with `animator.SetTrigger("Jump")`, etc. | Set it, don’t forget it — a missing trigger is how silent movies happen in Unity. 🎬😶 |
|  | Root Motion vs. Scripted | Root Motion uses animation data to move the character; Scripted uses Rigidbody or Transform. Choose based on control needs. | Root Motion = autopilot ✈️. Scripted = manual drive 🕹️. Know when to chill, and when to steer. |

---

## 🐞 Debug Table

| Week | Bug / Issue Encountered | Observations | Solution | 🧠 Comment / Funny Note |
|------|--------------------------|--------------|----------|--------------------------|
| **Week 1** | Scene too dark | Couldn’t see terrain details or player | Added directional light + adjusted intensity | It’s not a horror game yet, chill with the darkness. 🕯️ |
| **Week 2** | Materials not applying correctly | Materials looked flat and weird | Checked shader settings, reapplied correct material type | It wasn’t a bug. I just had commitment issues. 🎨💔 |
| **Week 3** | Rigidbody character wouldn’t jump | Used wrong force mode and forgot to check "isGrounded" | Switched to `ForceMode.Impulse`, added ground check logic | The floor is... not lava. It’s just unregistered. 🧱🤦‍♀️ |
| **Week 4** | Character floats or doesn’t land properly | Gravity didn’t feel real, bouncy effects | Added downward force manually and tweaked drag | Basically gave my character an existential crisis. 😵‍💫 |
|  | OnTrigger not detected | Forgot to check “Is Trigger” on collider | Enabled trigger on the collider | Checked everything except the checkbox. Classic. ✅🤡 |
| **Week 5** | Trees missing colliders | Player walks through trees | Realized Unity terrain trees don’t have mesh colliders by default | Used capsule colliders at tree bases only | Ghost trees are not the vibe. 👻🌲 |
|  | Terrain too spiky after heightmap import | Scale too large for heightmap depth | Reduced heightmap scale & smoothed terrain | Accidentally summoned Mount Doom. 🏔️🔥 |
|  | Wind Zone not affecting trees | Trees didn’t sway | Used proper Speed/Size values + enabled wind support in tree shader | Wind was like “Not my job.” Had to convince it. 💨🙅 |
| **Week 6** | Torque didn’t rotate player properly | Sphere rotated inconsistently; didn’t align with camera | Used `AddTorque` in `FixedUpdate` with normalized direction from input | Spinning out of control… story of my life. 🌀😭 |
|  | Shards spawned inside terrain | Some collectible shards were unreachable | Adjusted spawn height offset above terrain using `Terrain.SampleHeight` | Shards had tunnel vision. Literally underground. 💎⛏️ |
|  | Shield UI didn’t update visually | Logic worked but fill bar stayed empty | Forgot to assign `Image.fillAmount` in script | The code worked… but forgot to tell the UI. 😶🖼️ |
|  | Coroutine spawned shards too fast | Multiple shards appeared before 5s | Didn’t set `spawned` flag or use proper wait timing | Coroutine was a caffeine-fueled mess. ☕⚡ |
|  | Player triggered shard but no feedback | No sound or particles on collection | Added particle system + audio source + trigger detection | The shard was shy. Gave it a glow-up. ✨🎶 |
| **Week 7**| Fire particle flickering too fast | Flames looked like they were panicking 💥 | Adjusted particle lifetime and added slight delay between bursts | The fire had more anxiety than me during finals 🔥😅 |
|  **Week 8**| Animation snapping between idle/walk | Jerky blend when speed was near zero | Smoothed the parameter threshold + added damping | My character’s dance moves were not it 💃🪩 |
|  | Character floating during jump animation | Jump clip had root motion enabled | Disabled root motion for vertical transitions | Moonwalking in the air like it’s 2099 🚀🌕 |
|  |Timeline didn’t trigger animation | Bound objects weren’t set in PlayableDirector | Manually dragged GameObject into track binding | Unity really said “do it yourself” 🧱👷 |
---


## ⚖️ Comparisons (Each With Their Own Charm!)

## Week 1

#### 🎮 OpenGL vs DirectX
| Feature      | OpenGL 🌍                         | DirectX 🎯                     |
|--------------|----------------------------------|--------------------------------|
| Platform     | Cross-platform                   | Windows-centric                |
| Flexibility  | Open standard, highly customizable | Tight Microsoft ecosystem      |
| Performance  | Good for scientific visuals      | Optimized for gaming           |

#### 🛠️ Unity Setup (Unity Hub + Unity 6 + VS2022)
| Feature    | Description                                     |
|------------|-------------------------------------------------|
| Unity Hub  | Project management tool, version control 🗂️       |
| Unity 6    | Latest stable release with new physics features 🔧|
| VS2022     | IDE for scripting with IntelliSense support 💻   |

#### ⚡ CPU vs GPU While Coding
| Role     | CPU 🧠                                       | GPU 🖥️                                         |
|----------|---------------------------------------------|-------------------------------------------------|
| Usage    | Handles logic, scripting, and single-threaded tasks | Handles rendering, shaders, and parallel processing |
| Strength | Flexibility and control                    | Speed and high-volume math                        |

#### 🌐 2D vs Isometric vs 3D
| Type        | Description                              |
|-------------|------------------------------------------|
| 2D          | Point-based visuals, simpler physics     |
| Isometric   | 2.5D perspective for depth illusion      |
| 3D          | Full axis-based space (no cheating!)     |

#### 🔄 Global vs Local Transforms
| Type     | What Happens                                |
|----------|---------------------------------------------|
| Global   | Movement/rotation relative to world axes 🌎  |
| Local    | Movement/rotation relative to object axes 🔗|

## Week 2

#### 🧩 Mesh vs Mesh Renderer
| Feature         | Mesh 🔶                            | Mesh Renderer 🎥                          |
|-----------------|-----------------------------------|------------------------------------------|
| Purpose         | Holds geometry                    | Renders mesh with materials             |
| Visibility      | Not visible on its own            | Controls how object appears in-game     |

#### 🛡️ Colliders vs Triggers
| Feature         | Collider ⚔️                       | Trigger 🎯                                |
|-----------------|-----------------------------------|------------------------------------------|
| Purpose         | Physics boundaries                | Logical event detection                 |
| Reaction        | Causes physical interactions      | Does not cause physical forces          |

#### 🗳️ Prefab vs Asset
| Feature    | Prefab 🏗️                              | Asset 🎨                                 |
|------------|--------------------------------------|------------------------------------------|
| Description| A reusable game object template     | Files (textures, sounds, etc.)          |

#### 🕰️ Baking (Lighting)
| Type     | Description                                        |
|----------|----------------------------------------------------|
| Realtime | Dynamic lighting updates during gameplay ⏱️           |
| Mixed    | Combination of baked and realtime effects 🍰         |
| Baked    | Pre-calculated lighting for performance boost 🍞    |

## Week 3

#### 🎨 Base Map vs Normal Map vs Height Map
| Map Type    | Description                                       |
|-------------|---------------------------------------------------|
| Base Map    | The texture’s main color information 🖼️            |
| Normal Map  | Simulates surface detail without geometry changes 🛠️|
| Height Map  | Adds depth by displacing vertices 🌄               |

#### 💡 Point Light vs Directional Light vs Spot Light
| Light Type   | Description                                      |
|--------------|--------------------------------------------------|
| Point        | Emits light in all directions like a bulb 💡     |
| Directional  | Parallel rays, infinite distance 🌞              |
| Spot         | Focused beam of light, like a flashlight 🔦      |

#### 🧱 GameObject vs Component
| Feature      | GameObject 🏗️                                  | Component 🧩                             |
|--------------|------------------------------------------------|----------------------------------------|
| Description  | The container object                           | Behavior or property attached to GameObject |

#### 🔄 Linear Damping vs Angular Damping
| Feature         | Linear Damping 🚗                          | Angular Damping 🔁                       |
|-----------------|--------------------------------------------|------------------------------------------|
| Function        | Slows linear motion                        | Slows rotation                          |

#### ⚖️ Angular Damping vs Inertia on Axis
| Feature          | Angular Damping 🔁                        | Inertia Tensor ⚖️                       |
|------------------|------------------------------------------|------------------------------------------|
| Purpose          | Reduces rotational velocity              | Determines rotation resistance on axes   |

#### 🧩 Discrete vs Continuous Collision Detection
| Type      | Description                                     |
|-----------|-------------------------------------------------|
| Discrete  | Periodic collision checks 🕐                     |
| Continuous| Constant checking for fast objects 🚀            |

#### 🎯 Interpolation vs Extrapolation
| Feature      | Interpolation 🧵                            | Extrapolation 🧭                        |
|--------------|--------------------------------------------|----------------------------------------|
| Description  | Smooths values between frames              | Predicts future position beyond frames |

#### 🏎️ Dynamic vs Static Friction (Physics Material)
| Friction Type | Description                                 |
|---------------|---------------------------------------------|
| Dynamic       | Resistance when object is moving 🛷          |
| Static        | Resistance before object starts moving 🏋️    |

## Week 4
#### Character Controller vs. Capsule Collider 🏗️
| Feature | Explanation |
|---------|------------|
| Character Controller | Has built-in movement handling, not affected by physics. |
| Capsule Collider | Simple physics object, needs manual movement scripting. |

#### SimpleMove vs. Move
| Feature | Explanation |
|---------|------------|
| SimpleMove | Includes delta time, applies gravity automatically. |
| Move | Requires manual gravity handling and physics calculations. |

#### Update vs. FixedUpdate
| Feature | Explanation |
|---------|------------|
| Update | Frame-dependent; used for UI and non-physics logic. |
| FixedUpdate | Runs at a fixed timestep; used for physics-related updates. |

#### Gravity Acceleration
| Concept | Explanation |
|---------|------------|
| Gravity Effect | Gravity isn't a fixed velocity—it accumulates over time. |
| Acceleration Impact | Acceleration builds up, making movement feel natural. |

#### Slope Limit vs. Step Offset
| Feature | Explanation |
|---------|------------|
| Slope Limit | Determines the max incline the character can walk up. |
| Step Offset | Defines how high a character can step without jumping. |

#### Shock Physics 🛠️✨
| Concept | Explanation |
|---------|------------|
| Shock Force | A sudden application of force instead of gradual acceleration. |
| Use Case | Used for instant bursts of movement, like explosions. |

#### Heightmaps
| Feature | Explanation |
|---------|------------|
| Grayscale Heightmap | White = highest, black = lowest; used to generate terrain. |
| Application | Imported into Unity to create realistic landscape elevation. |

---
## Week 5

### URP vs. Built-in Rendering 🛠️

| Feature         | URP 🚀                        | Built-in 🧱                     |
|-----------------|------------------------------|--------------------------------|
| Performance     | Optimized for mobile/VR      | Better on older hardware       |
| Shader Support  | Requires conversion           | Works with Standard Shader     |
| Use Case        | Ideal for high-end visuals    | Great for legacy projects      |

---

### Tree Placement: Standalone vs. Terrain 🌳

| Feature     | Standalone 🌲               | Terrain 🌍                     |
|------------|-----------------------------|-------------------------------|
| Flexibility | Move freely                 | Locked to terrain             |
| Collision   | Manual setup required       | Auto-generated on placement   |

## Week 6

### 🎥 Cinemachine vs. Traditional Camera

| Feature                       | Traditional Camera        | Cinemachine Virtual Camera        |
|------------------------------|---------------------------|-----------------------------------|
| Position/Rotation            | Manual script control     | Auto-follows targets & blends     |
| Transitions                  | Snap or Lerp              | Smooth blends with timeline/curves |
| Field of View Adjustments    | Manually coded            | Built-in dynamic options          |
| Collision Handling           | Needs scripting           | Built-in damping + collision push |

### ☔ Post-Processing with Rain

| Aspect              | No Effects              | With Post-Processing              |
|---------------------|-------------------------|-----------------------------------|
| Visual Clarity      | Flat, less atmosphere   | Depth blur, fog, wet screen FX    |
| Mood                | Neutral or dry          | Dramatic, immersive rainy feel    |
| Camera Layering     | Static render           | Dynamic overlays based on weather |

## Week7 
| **Feature** | **Unity Particle System** | **Shader-based Fire** | **Real-Time VFX Plugins** |
|-------------|---------------------------|------------------------|---------------------------|
| Ease of Use | Beginner-friendly, built into Unity | Requires shader knowledge (HLSL/Shader Graph) | Drag-and-drop ready, minimal setup |
| Visual Quality | Good with tweaks, supports color/lifetime curves | Highly customizable, can look ultra-realistic | Often cinematic quality, pre-optimized |
| Performance | Moderate (depends on particle count) | Efficient if written well | Varies (some heavy, some GPU-accelerated) |
| Customization | Exposed parameters for shape, size, speed | Full control over noise, distortion, emissive glow | Depends on plugin limitations |
| Integration | Easily used in prefabs, triggerable via script | Needs setup for interaction, harder to reuse | Usually prefab-ready, sometimes overkill |
| Best Use Case | Simple in-game fire, torches, spells | Stylized or surreal fire, cutscenes | High-end VFX, boss battles, polished games |

## Week 8
### 🎞️ Week 8 Comparison Table – Animation Systems

| **Feature** | **Animator Controller (State Machine)** | **Timeline** | **Blend Trees** |
|-------------|-----------------------------------------|--------------|-----------------|
| Use Case | Character movement, transitions (Idle → Walk → Jump) | Cinematic sequences, cutscenes, synced events | Smooth transitions between animations (walk to run) |
| Setup Complexity | Moderate (nodes, transitions, parameters) | Visual and easy for non-coders | Requires properly parameterized motion states |
| Scripting Involvement | Controlled with SetTrigger, SetBool, etc. | Minimal — mostly used visually | Needs script if affected by speed/direction |
| Real-Time Interaction | Designed for interactive characters | Not interactive (pre-timed) | Real-time based on input or AI state |
| Control Granularity | Medium – works best with clear states | High – frame-accurate, event-controlled | High – responsive and fluid |
| Cool Factor | Feels like wiring up a robot brain 🤖 | Director’s chair mode 🎬 | Like teaching a dancer how to freestyle 💃 |


## 💡 Future Ideas & Experiments

| Week     | Idea/Experiment                                      | Why It’s Cool                                                |
|----------|------------------------------------------------------|---------------------------------------------------------------|
| **Week 2** | Light scenes for one player using layers             | Mystery game where Player 1 sees hidden clues! 🔦             |
|          | Torch reveals hidden objects                         | Perfect for puzzle or horror games 👀                         |
| **Week 3** | Test colored cookies with alpha                      | Adds rainbow effects and dynamic shadows 🌈                   |
|          | Dual-layer lighting for hidden/exposed objects       | Example: torch reveals "secret" walls! 🔦                     |
|          | Camera output on UI devices                          | Display camera feed on in-game tablets 📱                     |
| **Week 4** | Implement Shock Physics                              | Sudden force application for instant motion 💥                |
|          | Create "Flappy Bird Mode"                            | Switch between flying & normal jump modes 🕊️                 |
|          | Use real-world extreme terrain heightmap             | See how Unity handles huge elevation differences 🏔️          |
| **Week 5** | Add dynamic fog zones based on player height         | Makes the environment feel more mysterious 🌫️               |
|          | Blend terrain textures based on slope                | Could auto-make steep areas rocky and flat areas grassy 🧗🌾 |
|          | Animate wind intensity to match in-game weather      | Adds realism with dynamic weather effects 🌪️                |
| **Week 6** | Add manual camera switch button for gamepad/mouse    | Lets player shift views interactively 🎮                      |
|          | Rain that affects post-processing (depth blur, fog)  | Boosts immersion with reactive FX based on weather ☔         |
|          | Customize camera blend curves for events             | Smooth transitions based on story or movement events 🎬       |
|

| **Week 7** | 🔥 Build a fire propagation system based on terrain type | Adds gameplay depth — imagine fire spreading differently on grass, stone, or magical tiles! |
| | 💨 Add wind force that dynamically affects flame direction | Makes fire feel alive — could use Unity’s wind zones or custom vector fields |
| | 🌋 Procedural lava + fire burst system using Perlin noise | Gives a dynamic volcano or enemy attack system — juicy visuals + chaos! |
| **Week 8** | 🕺 Procedural animation blending for hurt/win states | Adds polish — less animation assets, more fluid reactions |
| | 🎥 Add cinematic camera control tied to Timeline events | Could zoom, shake, or fade during critical hits or boss intros |
| | 🎭 Experiment with runtime rig retargeting for NPC variety | Makes crowd animations more varied — one rig, many identities |
## The Previous Spirals 🌀⏳

Here’s a screenshot to immortalize the absolute chaos—proof that my first attempt didn’t just fail, it spectacularly failed. Exposing my own mess so future me has no choice but to fix it. 😂
## Antarctica: Slippery Code Edition
![image](https://github.com/user-attachments/assets/4328bbf6-d460-4c93-b990-ad1a90598aba)
![image](https://github.com/user-attachments/assets/9e1a39a9-0285-4bb8-b39a-934b008b44ed)

![image](https://github.com/user-attachments/assets/16768694-4a3f-4a71-8c59-20badeb44445)

## Maze Not Mazing
![image](https://github.com/user-attachments/assets/23c59097-ca64-43d5-a639-294ce56e2767)

![image](https://github.com/user-attachments/assets/d7f980d3-b3cd-497c-8994-5dbaaeadc2bf)

# 7th Quiz - THE REAL TEST! 🚀

## 🎯 Project Scope & Core Elements

| Component          | Description |
|--------------------|-------------|
| 🧠 Game Concept    | A sphere ascends a mountain, dodges falling rocks, collects blue shards, and reaches a portal to win |
| 📦 Key Prefabs     | Sphere (Player), Rock, Shard, Portal, Trees |
| 🎮 Movement        | Physics-based rolling using Rigidbody.AddTorque() with acceleration and jump |
| 🧱 Terrain Setup   | Generated via heightmap, textured with terrain layers, decorated with tree prefabs |
| 🎥 Camera System   | Third-person follow camera with dynamic offset using Camera.main.transform.position and LateUpdate() |
| 💡 Environment     | Soft fog, real-time lighting, ambient wind sounds, chill night-skybox |
| 🔁 Game Loop       | Rocks fall from above (deal damage), shards spawn every 5s (25% chance), player regenerates shield on collection |
| 🌀 Portal End      | Triggers win condition when player enters |

## 🛠️ Script Summary & Behavior

| Script                  | Purpose | Key Functions |
|-------------------------|---------|---------------|
| MagicSphereMovement.cs  | Manages movement, collisions, and jumping | AddTorque(), OnCollisionEnter, AddForce() |
| CameraFollow.cs         | Smooth camera follow with slight lag | LateUpdate(), offset logic |
| RockSpawner.cs          | Spawns rocks at intervals | InvokeRepeating(), destroy rocks when velocity is low |
| Rock.cs                 | Handles rock behavior on collision and self-cleanup | OnCollisionEnter(), IsSleeping() |
| ShardSpawner.cs         | Spawns shards with 25% probability | Random.value, Instantiate() |
| Shard.cs                | Detects collision with player, heals shield | OnTriggerEnter(), UI update |
| Portal.cs               | Ends game upon contact | OnTriggerEnter() |

## 🌌 Game Story

*A magical sphere must climb a dangerous mountain to reach the Summit Portal, a mysterious gateway at the peak. But the journey is not easy, as huge rocks fall from above, threatening to break its protective blue shield.*

*To survive, the sphere must dodge falling rocks while collecting blue shards, which restore lost parts of its shield. Every hit from a rock weakens the shield, making the climb even riskier.*

*Can the sphere overcome the mountain's challenges and complete its journey?*

## 💡 Beyond the Basics
✅ Sound effects for rain falling  
✅ Sound effects for rock impact and shard pickup  
✅ Simple UI with health/shield bar and shard count  

---

## 🏞️ 1. Terrain Development

![Terrain Heightmap](https://github.com/user-attachments/assets/c3057406-fc14-4e02-ae79-e4313c35b1f1)
![Terrain Texturing](https://github.com/user-attachments/assets/8d67f8f2-ee96-4cd4-b06f-106726587b16)
![Terrain Details](https://github.com/user-attachments/assets/cae165cb-81f1-47a2-921f-6684484f5311)

**💡 Extra Mile:**  
- Integrated "smoothlayers" heightmap script for soft blending  
- Optimized billboard distance and max mesh trees  
- Increased detail distance and shadow settings  

### Environment Enhancements
![Fog Settings](https://github.com/user-attachments/assets/a715aa93-deef-4dea-89d8-2dc264c1bd2c)  
*Added atmospheric fog to complement rain system*

![Rain Sound](https://github.com/user-attachments/assets/8f4c67fc-f8ee-45c1-8bd2-bc6004e82278)  
*Implemented rain sound effects for immersion*

[Rain Particle Tutorial](https://www.youtube.com/watch?v=MBVGUD5nZeA)

---

## 🌳 2. Tree System

![Tree Placement](https://github.com/user-attachments/assets/81ab7c7b-cb99-4b79-928b-5e8a36823d1c)
![Tree Colliders](https://github.com/user-attachments/assets/b28b315b-e021-46e0-8b5a-cefb5bab1830)
![Wind Effect](https://github.com/user-attachments/assets/9a6b657c-86d7-4434-ad34-710d2fc0af1f)
![Tree Bend](https://github.com/user-attachments/assets/347b7144-1d55-43b4-aedc-7c78cc0f3573)

**💡 Extra Mile:**  
Added bend factor to trees for natural wind motion  

---

## 🌪️ 3. Wind System (EAST Direction)

![Wind Zone](https://github.com/user-attachments/assets/122be97b-c53c-4f2a-9fbf-bd9776c18689)
![Wind Settings](https://github.com/user-attachments/assets/c852a75a-e3e3-404b-aae4-ac8a6553c133)

---

## 🎥 4. Camera System

![Camera Orbit](https://github.com/user-attachments/assets/0e49aa62-a6e0-4f6f-a398-41a8646150cf)
![Camera Follow](https://github.com/user-attachments/assets/02eb5ff7-9668-4359-8adf-7b990ac76bc0)
![Camera Perspective](https://github.com/user-attachments/assets/35fb1fbb-2246-4a56-9a69-bceeeaddf420)

*Implemented 3-ring orbit follow system for optimal gameplay perspectives*

---

## 🌌 5. Portal Mechanics

![Portal Design](https://github.com/user-attachments/assets/f9b0114a-b034-45d3-afc9-0499198c1167)
![Portal Effect](https://github.com/user-attachments/assets/63d7b086-b833-4be7-97a5-7ca257ffc66f)
![Portal Blink](https://github.com/user-attachments/assets/c50daabc-dccb-43a2-99a1-346d4f704638)

**💡 Extra Mile:**  
Created blinking effect instead of static appearance  

---

## ✨ 6. Magic Sphere Player

![Sphere Design](https://github.com/user-attachments/assets/aaaf3034-36a2-412f-b7ce-130c9d1d417f)
![Sphere Physics](https://github.com/user-attachments/assets/534f4207-775c-4dfa-bfcb-9e9a1cd514cc)
![Sphere Movement](https://github.com/user-attachments/assets/889e08fa-e92d-4691-a165-aaff5332efee)

**Movement Features:**  
- No Flappy Bird jumping (grounded checks only)  
- Torque-based movement for realistic rolling  
- Rigidbody physics integration  

---

## 🌧️ 7. Rain System

![Rain Particles](https://github.com/user-attachments/assets/2c111373-9fef-43bf-8873-fe34016cb272)
![Rain Settings](https://github.com/user-attachments/assets/85509a60-f5cd-46c9-a64d-0964ddd3a8d7)

**System Configuration:**  
- 200 particles/sec emission  
- Collision-enabled drops  
- Follow-player system for performance  
- Sound effects synchronization  

**💡 Extra Mile:**  
"I didn't just make particles - I engineered weather 🌧️🛠️"

---
## 🎮 What Makes This Game "Me" - The Ultimate Breakdown

| Category          | What I Learned 🧠 | Funny Moments 😂 | Special Touches ✨ | Technical Wins 💻 |
|-------------------|-------------------|------------------|--------------------|-------------------|
| **Physics**       | Torque > Force for rolling | Sphere moonwalk bug 🕺 | Realistic rock tumbles | Perfect grounded checks |
| **Environment**   | Heightmap magic | Antarctica simulator ❄️ | Dynamic weather system | Optimized tree LODs |
| **Game Feel**     | Juice matters | Portal that blinks...menacingly 👁️ | Satisfying shard "ping" | Camera orbit rings |
| **Debugging**     | Console.log is life | "Why are trees ghosts?!" 👻 | Added debug rain toggle | Fixed infinite jump |
| **Art**           | Shader graph basics | "Modern art" terrain phase 🎨 | Custom portal glow | Performance-first shadows |
| **Sound**         | AudioSource nuances | Rain that sounds like bacon 🥓 | Environmental wind FX | Spatial blend setup |
| **UX**            | UI communicates state | Health bar that lied 😅 | Clear shard counter | Shield regen feedback |
| **Story**         | Emergent narrative | "Rock attack: revenge" plot 📖 | Environmental storytelling | Win/lose conditions |

| **My Signature Moves** | **Description** |
|------------------------|----------------|
| 🌧️ Rain Engineer | Built meteorologically-accurate weather |
| 🌀 Torque Master | Physics-based movement that feels *just right* |
| 🎮 Juice Wizard | Added satisfying SFX/VFX to every interaction |
| 🐛 Debug Shaman | Fixed bizarre bugs with creative solutions |
| 🖌️ Lazy Artist | Made simple assets look polished through lighting |


