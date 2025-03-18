# Command Reference

This document provides a complete reference for all commands available in BlenderMCP Ultimate Cinematic Upgrade. These commands can be used programmatically through the Python API or through the BlenderMCP Ultimate panel.

## Command Structure

Commands in BlenderMCP Ultimate follow a hierarchical structure:

```
module.submodule.function
```

For example:
```
scene_setup.hdri_lighting.apply_hdri
```

## Asset Management Commands

### Mixamo Integration

| Command | Description | Parameters |
|---------|-------------|------------|
| `asset_management.mixamo.import_character` | Import a character from Mixamo | `character_type`: Type of character to import<br>`name`: Name for the imported character |
| `asset_management.mixamo.import_animation` | Import an animation from Mixamo | `animation_name`: Name of the animation<br>`character_name`: Name of the target character |
| `asset_management.mixamo.retarget_animation` | Retarget a Mixamo animation to a Rigify rig | `source_armature`: Source armature name<br>`target_armature`: Target armature name |

### Sketchfab Integration

| Command | Description | Parameters |
|---------|-------------|------------|
| `asset_management.sketchfab.search_models` | Search for models on Sketchfab | `query`: Search query<br>`category`: Optional category filter |
| `asset_management.sketchfab.import_model` | Import a model from Sketchfab | `model_id`: Sketchfab model ID<br>`name`: Name for the imported model |
| `asset_management.sketchfab.get_model_info` | Get information about a Sketchfab model | `model_id`: Sketchfab model ID |

### TurboSquid Integration

| Command | Description | Parameters |
|---------|-------------|------------|
| `asset_management.turbosquid.search_models` | Search for models on TurboSquid | `query`: Search query<br>`category`: Optional category filter |
| `asset_management.turbosquid.import_model` | Import a model from TurboSquid | `model_id`: TurboSquid model ID<br>`name`: Name for the imported model |
| `asset_management.turbosquid.get_model_info` | Get information about a TurboSquid model | `model_id`: TurboSquid model ID |

### Quixel Integration

| Command | Description | Parameters |
|---------|-------------|------------|
| `asset_management.quixel.search_assets` | Search for assets on Quixel Megascans | `query`: Search query<br>`category`: Optional category filter |
| `asset_management.quixel.import_asset` | Import an asset from Quixel Megascans | `asset_id`: Quixel asset ID<br>`name`: Name for the imported asset |
| `asset_management.quixel.get_asset_info` | Get information about a Quixel asset | `asset_id`: Quixel asset ID |

## Scene Setup Commands

### HDRI Lighting

| Command | Description | Parameters |
|---------|-------------|------------|
| `scene_setup.hdri_lighting.apply_hdri` | Apply an HDRI environment map | `hdri_name`: Name of the HDRI<br>`strength`: Light strength |
| `scene_setup.hdri_lighting.create_three_point_lighting` | Create a three-point lighting setup | `key_strength`: Key light strength<br>`fill_strength`: Fill light strength<br>`rim_strength`: Rim light strength |
| `scene_setup.hdri_lighting.create_studio_lighting` | Create a studio lighting setup | `style`: Lighting style (soft, harsh, dramatic) |

### Procedural Environment

| Command | Description | Parameters |
|---------|-------------|------------|
| `scene_setup.procedural_environment.create_terrain` | Create procedural terrain | `size`: Terrain size<br>`resolution`: Terrain resolution<br>`height_scale`: Height scale |
| `scene_setup.procedural_environment.create_architecture` | Create procedural architecture | `building_type`: Type of building<br>`size`: Building size |
| `scene_setup.procedural_environment.create_environment` | Create a complete environment | `environment_type`: Type of environment<br>`prompt`: Text description |

### Scene Composition

| Command | Description | Parameters |
|---------|-------------|------------|
| `scene_setup.scene_composition.arrange_objects` | Arrange objects in the scene | `objects`: List of object names<br>`arrangement`: Arrangement type |
| `scene_setup.scene_composition.create_composition` | Create a scene composition | `composition_type`: Type of composition<br>`objects`: List of object names |
| `scene_setup.scene_composition.apply_rule_of_thirds` | Apply rule of thirds to camera | `camera_name`: Name of the camera |

## Character Animation Commands

### Rigify Auto-Rigging

| Command | Description | Parameters |
|---------|-------------|------------|
| `character_animation.rigify_auto_rigging.create_metarig` | Create a Rigify metarig | `character_name`: Name of the character<br>`rig_type`: Type of rig |
| `character_animation.rigify_auto_rigging.generate_rig` | Generate a rig from a metarig | `metarig_name`: Name of the metarig |
| `character_animation.rigify_auto_rigging.auto_weight_paint` | Automatically weight paint a character | `character_name`: Name of the character<br>`armature_name`: Name of the armature |

### Animation Retargeting

| Command | Description | Parameters |
|---------|-------------|------------|
| `character_animation.animation_retargeting.retarget_animation` | Retarget animation between rigs | `source_armature`: Source armature name<br>`target_armature`: Target armature name |
| `character_animation.animation_retargeting.create_bone_mapping` | Create a bone mapping between rigs | `source_armature`: Source armature name<br>`target_armature`: Target armature name |
| `character_animation.animation_retargeting.apply_animation` | Apply an animation to a rig | `armature_name`: Name of the armature<br>`animation_name`: Name of the animation |

### IK/FK Switching

| Command | Description | Parameters |
|---------|-------------|------------|
| `character_animation.ikfk_switching.switch_to_ik` | Switch a limb to IK mode | `armature_name`: Name of the armature<br>`limb`: Limb name (arm.L, arm.R, leg.L, leg.R) |
| `character_animation.ikfk_switching.switch_to_fk` | Switch a limb to FK mode | `armature_name`: Name of the armature<br>`limb`: Limb name (arm.L, arm.R, leg.L, leg.R) |
| `character_animation.ikfk_switching.snap_ik_to_fk` | Snap IK controls to FK pose | `armature_name`: Name of the armature<br>`limb`: Limb name (arm.L, arm.R, leg.L, leg.R) |
| `character_animation.ikfk_switching.snap_fk_to_ik` | Snap FK controls to IK pose | `armature_name`: Name of the armature<br>`limb`: Limb name (arm.L, arm.R, leg.L, leg.R) |

### Keyframe Generation

| Command | Description | Parameters |
|---------|-------------|------------|
| `character_animation.keyframe_generation.generate_walk_cycle` | Generate a walk cycle animation | `armature_name`: Name of the armature<br>`duration`: Animation duration |
| `character_animation.keyframe_generation.generate_run_cycle` | Generate a run cycle animation | `armature_name`: Name of the armature<br>`duration`: Animation duration |
| `character_animation.keyframe_generation.generate_jump_animation` | Generate a jump animation | `armature_name`: Name of the armature<br>`height`: Jump height |
| `character_animation.keyframe_generation.generate_animation` | Generate animation from text | `character_name`: Name of the character<br>`animation_type`: Type of animation<br>`prompt`: Text description<br>`duration`: Animation duration |

### Cinematic Camera

| Command | Description | Parameters |
|---------|-------------|------------|
| `character_animation.cinematic_camera.create_tracking_camera` | Create a camera that tracks an object | `target_name`: Name of the target object<br>`distance`: Camera distance |
| `character_animation.cinematic_camera.create_path_animation` | Create a camera path animation | `path_type`: Type of path (circle, dolly, crane, arc)<br>`duration`: Animation duration |
| `character_animation.cinematic_camera.set_depth_of_field` | Set depth of field for a camera | `camera_name`: Name of the camera<br>`focus_object`: Name of the focus object<br>`aperture`: Aperture size |
| `character_animation.cinematic_camera.create_cinematic_camera` | Create a cinematic camera | `camera_type`: Type of camera<br>`target_name`: Name of the target object<br>`duration`: Animation duration |

## Physics & VFX Commands

### Cloth Physics

| Command | Description | Parameters |
|---------|-------------|------------|
| `physics_vfx.cloth_physics.add_cloth_simulation` | Add cloth simulation to an object | `object_name`: Name of the object<br>`preset`: Cloth preset (silk, cotton, denim, leather, rubber) |
| `physics_vfx.cloth_physics.add_collision` | Add collision to an object | `object_name`: Name of the object |
| `physics_vfx.cloth_physics.pin_vertex_group` | Pin a vertex group for cloth simulation | `object_name`: Name of the object<br>`vertex_group`: Name of the vertex group |
| `physics_vfx.cloth_physics.bake_cloth_simulation` | Bake a cloth simulation | `object_name`: Name of the object<br>`start_frame`: Start frame<br>`end_frame`: End frame |

### Hair Physics

| Command | Description | Parameters |
|---------|-------------|------------|
| `physics_vfx.hair_physics.add_hair_particles` | Add hair particles to an object | `object_name`: Name of the object<br>`hair_length`: Hair length<br>`hair_count`: Number of hairs |
| `physics_vfx.hair_physics.style_hair` | Style hair particles | `object_name`: Name of the object<br>`style`: Hair style (straight, wavy, curly, afro) |
| `physics_vfx.hair_physics.add_hair_dynamics` | Add dynamics to hair particles | `object_name`: Name of the object<br>`stiffness`: Hair stiffness |
| `physics_vfx.hair_physics.bake_hair_dynamics` | Bake hair dynamics | `object_name`: Name of the object<br>`start_frame`: Start frame<br>`end_frame`: End frame |

### Rigid Body Physics

| Command | Description | Parameters |
|---------|-------------|------------|
| `physics_vfx.rigid_body_physics.add_rigid_body` | Add rigid body physics to an object | `object_name`: Name of the object<br>`body_type`: Body type (active, passive) |
| `physics_vfx.rigid_body_physics.fracture_object` | Fracture an object for destruction | `object_name`: Name of the object<br>`fracture_type`: Type of fracture<br>`pieces`: Number of pieces |
| `physics_vfx.rigid_body_physics.add_explosion_force` | Add explosion force to rigid bodies | `location`: Explosion location<br>`strength`: Explosion strength<br>`radius`: Explosion radius |
| `physics_vfx.rigid_body_physics.bake_rigid_body_simulation` | Bake a rigid body simulation | `start_frame`: Start frame<br>`end_frame`: End frame |

### Particle Effects

| Command | Description | Parameters |
|---------|-------------|------------|
| `physics_vfx.particle_effects.create_smoke` | Create a smoke simulation | `location`: Smoke location<br>`size`: Smoke size<br>`density`: Smoke density |
| `physics_vfx.particle_effects.create_fire` | Create a fire simulation | `location`: Fire location<br>`size`: Fire size<br>`intensity`: Fire intensity |
| `physics_vfx.particle_effects.create_explosion` | Create an explosion effect | `location`: Explosion location<br>`size`: Explosion size<br>`strength`: Explosion strength |
| `physics_vfx.particle_effects.create_fog` | Create fog in the scene | `name`: Fog name<br>`location`: Fog location<br>`size`: Fog size<br>`density`: Fog density<br>`color`: Fog color |
| `physics_vfx.particle_effects.create_rain` | Create rain particles | `coverage`: Rain coverage<br>`intensity`: Rain intensity |
| `physics_vfx.particle_effects.create_snow` | Create snow particles | `coverage`: Snow coverage<br>`intensity`: Snow intensity |
| `physics_vfx.particle_effects.create_storm` | Create a storm system | `location`: Storm location<br>`size`: Storm size<br>`intensity`: Storm intensity |

## Rendering Commands

### Render Engine Manager

| Command | Description | Parameters |
|---------|-------------|------------|
| `rendering.render_engine_manager.switch_to_cycles` | Switch to Cycles render engine | `use_gpu`: Whether to use GPU rendering |
| `rendering.render_engine_manager.switch_to_eevee` | Switch to Eevee render engine | None |
| `rendering.render_engine_manager.optimize_render_settings` | Optimize render settings | `target_quality`: Target quality level (preview, medium, high, ultra) |
| `rendering.render_engine_manager.apply_render_preset` | Apply a render preset | `preset`: Preset name (preview, medium, high, ultra) |
| `rendering.render_engine_manager.set_output_settings` | Configure output settings | `resolution_x`: X resolution<br>`resolution_y`: Y resolution<br>`resolution_percentage`: Resolution percentage<br>`file_format`: Output file format<br>`output_path`: Output path |

### Post-Processing

| Command | Description | Parameters |
|---------|-------------|------------|
| `rendering.post_processing.add_motion_blur` | Add motion blur effect | `shutter_speed`: Shutter speed |
| `rendering.post_processing.add_bloom` | Add bloom effect | `threshold`: Bloom threshold<br>`intensity`: Bloom intensity |
| `rendering.post_processing.add_vignette` | Add vignette effect | `intensity`: Vignette intensity |
| `rendering.post_processing.add_film_grain` | Add film grain effect | `intensity`: Grain intensity |
| `rendering.post_processing.apply_color_grading` | Apply color grading | `lift`: Lift values<br>`gamma`: Gamma values<br>`gain`: Gain values |
| `rendering.post_processing.apply_lut` | Apply a LUT for color grading | `lut_name`: Name of the LUT |
| `rendering.post_processing.apply_post_preset` | Apply a post-processing preset | `preset`: Preset name (standard, warm, cool, vintage, sci-fi, cinematic) |

### Multi-Camera Manager

| Command | Description | Parameters |
|---------|-------------|------------|
| `rendering.multi_camera_manager.create_camera_array` | Create an array of cameras | `count`: Number of cameras<br>`arrangement`: Camera arrangement |
| `rendering.multi_camera_manager.render_from_all_cameras` | Render from all cameras | `output_path`: Output path |
| `rendering.multi_camera_manager.create_camera_sequence` | Create a sequence of camera shots | `cameras`: List of camera names<br>`durations`: List of shot durations |
| `rendering.multi_camera_manager.export_video` | Export a video from rendered frames | `input_path`: Input frames path<br>`output_path`: Output video path<br>`codec`: Video codec<br>`quality`: Video quality |

## Progress Tracking Commands

| Command | Description | Parameters |
|---------|-------------|------------|
| `progress_tracking.progress_tracker.start_operation` | Start tracking an operation | `operation_id`: Unique operation ID<br>`operation_name`: Operation name<br>`total_steps`: Total number of steps |
| `progress_tracking.progress_tracker.update_progress` | Update operation progress | `operation_id`: Operation ID<br>`step`: Current step<br>`message`: Progress message |
| `progress_tracking.progress_tracker.complete_operation` | Complete an operation | `operation_id`: Operation ID<br>`message`: Completion message |
| `progress_tracking.progress_tracker.fail_operation` | Mark an operation as failed | `operation_id`: Operation ID<br>`error_message`: Error message |
| `progress_tracking.progress_tracker.get_operation` | Get operation information | `operation_id`: Operation ID |
| `progress_tracking.progress_tracker.get_logs` | Get operation logs | `operation_id`: Optional operation ID<br>`limit`: Maximum number of logs |

## Performance Optimization Commands

| Command | Description | Parameters |
|---------|-------------|------------|
| `performance_optimization.performance_optimizer.optimize_memory_usage` | Optimize memory usage | None |
| `performance_optimization.performance_optimizer.optimize_viewport_performance` | Optimize viewport performance | `quality`: Viewport quality level (low, medium, high) |
| `performance_optimization.performance_optimizer.optimize_render_settings` | Optimize render settings | `target_quality`: Target quality level (preview, medium, high, ultra) |
| `performance_optimization.performance_optimizer.optimize_physics_sim<response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>