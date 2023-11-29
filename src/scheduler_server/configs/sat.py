import os.path as op
import numpy as np

ufm_mv19_shift = np.degrees([-0.01583734, 0.00073145])
ufm_mv15_shift = np.degrees([-0.01687046, -0.00117139])
ufm_mv7_shift = np.degrees( [-1.7275653e-02, -2.0664736e-06])
ufm_mv9_shift = np.degrees( [-0.01418133,  0.00820128])
ufm_mv18_shift = np.degrees([-0.01625605,  0.00198077])
ufm_mv22_shift = np.degrees([-0.0186627,  -0.00299793])
ufm_mv29_shift = np.degrees([-0.01480562,  0.00117084])

d_xi = 10.9624
d_eta_side = 6.46363
d_eta_mid = 12.634

geometries_satp1 = {
  'ws3': {
    'center': [-d_xi+ufm_mv29_shift[0], d_eta_side+ufm_mv29_shift[1]],
    'radius': 6,
  },
  'ws2': {
    'center': [-d_xi+ufm_mv22_shift[0], -d_eta_side+ufm_mv22_shift[1]],
    'radius': 6,
  },
  'ws4': {
    'center': [0+ufm_mv7_shift[0], d_eta_mid+ufm_mv7_shift[1]],
    'radius': 6,
  },
  'ws0': {
    'center': [0+ufm_mv19_shift[0], 0+ufm_mv19_shift[1]], 
    'radius': 6,
  },
  'ws1': {
    'center': [0+ufm_mv18_shift[0], -d_eta_mid+ufm_mv18_shift[1]],
    'radius': 6,
  },
  'ws5': {
    'center': [d_xi+ufm_mv9_shift[0], d_eta_side+ufm_mv9_shift[1]],
    'radius': 6,
  },
  'ws6': {
    'center': [d_xi+ufm_mv15_shift[0], -d_eta_side+ufm_mv15_shift[1]],
    'radius': 6,
  },
}

wafer_sets = {
    'left_boresight_0': 'ws3,ws2',
    'middle_boresight_0': 'ws0,ws1,ws4',
    'right_boresight_0': 'ws5,ws6',
    'bottom_boresight_0': 'ws1,ws2,ws6',
    'left_boresight_p45': 'ws3,ws4',
    'middle_boresight_p45': 'ws2,ws0,ws5',
    'right_boresight_p45': 'ws1,ws6',
    'bottom_boresight_p45': 'ws1,ws2,ws3',
    'left_boresight_n45': 'ws1,ws2',
    'middle_boresight_n45': 'ws6,ws0,ws3',
    'right_boresight_n45': 'ws4,ws5',
    'bottom_boresight_n45': 'ws1,ws6,ws5',
}

blocks = {
    'baseline': {
        'cmb': {
            'type': 'toast',
            'file': op.join(op.dirname(__file__), 'data/satp1_baseline_20231031.txt'),
        }
    },
    'calibration': {
        'saturn': {
            'type': 'source',
            'name': 'saturn',
        },
        'moon': {
            'type': 'source',
            'name': 'moon',
        },
        'sun': {
            'type': 'source',
            'name': 'sun',
        },
        'mercury': {
            'type': 'source',
            'name': 'mercury',
        },
        'venus': {
            'type': 'source',
            'name': 'venus',
        },
        'mars': {
            'type': 'source',
            'name': 'mars',
        },
        'jupiter': {
            'type': 'source',
            'name': 'jupiter',
        },
        'uranus': {
            'type': 'source',
            'name': 'uranus',
        },
        'neptune': {
            'type': 'source',
            'name': 'neptune',
        },
    },
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
            'az_range': [-10, 400],
            'trim': True
        }
    },
    'cal_targets': [],
    'merge_order': ['calibration', 'baseline'],
    'time_costs': {
        'det_setup': 40*60,
        'bias_step': 60,
        'ufm_relock': 15*60,
    },
    'ufm_relock': True,
    'allow_partial': True,
    'wafer_sets': wafer_sets,
}