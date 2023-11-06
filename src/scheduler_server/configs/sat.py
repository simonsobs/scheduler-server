import os.path as op

geometries_satp1 = {
  'full': {
    'left': {
      'ws6': {
        'center': [-10.9624, 6.46363],
        'radius': 6,
      },
      'ws5': {
        'center': [-10.9624, -6.46363],
        'radius': 6,
      },
    },
    'middle': {
      'ws1': {
        'center': [0, 12.634],
        'radius': 6,
      },
      'ws0': {
        'center': [0, 0],
        'radius': 6,
      },
      'ws4': {
        'center': [0, -12.634],
        'radius': 6,
      },
    },
    'right': {
      'ws2': {
        'center': [10.9624, 6.46363],
        'radius': 6,
      },
      'ws3': {
        'center': [10.9624, -6.46363],
        'radius': 6,
      },
    },
  },
  'bottom' : {
    'ws4': {
        'center': [0, -12.634],
        'radius': 6,
    },
    'ws3': {
        'center': [10.9624, -6.46363],
        'radius': 6,
    },
    'ws5': {
        'center': [-10.9624, -6.46363],
        'radius': 6,
    },
  }
}

blocks = {
    'calibration': {
        'saturn': {
            'type' : 'source',
            'name' : 'saturn',
        },
        'moon': {
            'type' : 'source',
            'name' : 'moon',
        },
    },
    'baseline': {
        'cmb': {
            'type': 'toast',
            'file': op.join(op.dirname(__file__), 'data/satp1_baseline_20231031.txt'),
        }
    }
}

config_satp1 = {
    'blocks': blocks,
    'geometries': geometries_satp1,
    'rules': {
        'sun-avoidance': {
            'min_angle_az': 45,
            'min_angle_alt': 45,
        },
        'min-duration': {
            'min_duration': 600
        },
        'az-range': {
            'az_range': [-90, 450],
            'trim': True
        }
    },
    'cal_targets': [
        # (source, array_query, el_bore, tag)
        ('saturn', 'left', 50, 'left_focal_plane'),
        ('saturn', 'mid', 50,  'mid_focal_plane'),
        ('saturn', 'right', 50, 'right_focal_plane'),
    ],
    'merge_order': ['calibration', 'baseline'],
    'time_costs': {
        'det_setup': 40*60,
        'bias_step': 60,
        'ufm_relock': 120,
    },
    'ufm_relock': True,
}