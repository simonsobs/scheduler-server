config = """
blocks:
  moon: !source moon

rules:
  - !rule
    name: sun-avoidance
    min_angle_az: 6
    min_angle_alt: 6
    time_step: 10
    n_buffer: 3
  - !rule
    name: min-duration
    min_duration: 300
  - !rule
    name: make-source-plan
    specs:
      - bounds_x:
        - -0.5
        - 0.5
        bounds_y:
        - -0.5
        - 0.5
    spec_shape: ellipse
    max_obs_length: 6000
  - !rule
    name: make-source-scan
    preferred_length: 1800
  - !rule
    name: alt-range
    alt_range:
      - 20
      - 90

merge_order:
  - moon
post_rules:
  - !rule
    name: min-duration
    min_duration: 600
"""