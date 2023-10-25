config = """
    blocks:
        calibration:
            saturn: 
              type: source 
              name: saturn
            moon: 
              type: source
              name: moon
    rules:
        - name: sun-avoidance
          min_angle_az: 45
          min_angle_alt: 45
          time_step: 30
          n_buffer: 10
        - name: make-drift-scan
          block_query: calibration
          array_query: full
          el_bore: 50
          drift: true
    post_rules:
        - name: min-duration
          min_duration: 600
    merge_order:
        - moon
        - saturn
    geometries:
      full:
        left:
          ws6:
            center:
            - -10.9624
            - 6.46363
            radius: 6
          ws5:
            center:
            - -10.9624
            - -6.46363
            radius: 6
        middle:
          ws1:
            center: 
            - 0 
            - 12.634
            radius: 6
          ws0:
            center: 
            - 0 
            - 0 
            radius: 6
          ws4:
            center: 
            - 0 
            - -12.634
            radius: 6
        right:
          ws2:
            center:
            - 10.9624
            - 6.46363
            radius: 6
          ws3:
            center:
            - 10.9624
            - -6.46363
            radius: 6
"""