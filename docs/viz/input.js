const init_matrix = [
 [28,  2,  4,  2,  2,  3,  4,  4,  0,  1,  0,  0,  0,  2,  4,  1,  0,  1,  1,  3,  2,  0],
 [ 2, 11,  4,  1,  0,  3,  1,  1,  0,  1,  0,  1,  2,  1,  1,  0,  0,  0,  1,  0,  0,  1],
 [ 4,  4, 27, 10,  2,  5,  3,  2,  1,  1,  0,  2,  3,  5,  5,  1,  4,  1,  1,  1,  2,  2],
 [ 2,  1, 10, 28,  3,  2,  4,  3,  2,  1,  3,  3,  3,  4,  5,  2,  4,  3,  1,  1,  1,  0],
 [ 2,  0,  2,  3,  7,  1,  1,  1,  1,  0,  0,  0,  1,  2,  4,  1,  1,  1,  0,  2,  1,  0],
 [ 3,  3,  5,  2,  1, 14,  3,  2,  0,  1,  0,  0,  0,  2,  4,  0,  0,  1,  0,  1,  0,  1],
 [ 4,  1,  3,  4,  1,  3, 20,  7,  1,  4,  3,  1,  1,  4,  7,  3,  3,  2,  0,  1,  1,  1],
 [ 4,  1,  2,  3,  1,  2,  7, 21,  1,  5,  1,  2,  1,  4,  7,  2,  2,  3,  1,  2,  2,  2],
 [ 0,  0,  1,  2,  1,  0,  1,  1,  3,  1,  1,  1,  1,  1,  1,  1,  1,  1,  0,  0,  0,  1],
 [ 1,  1,  1,  1,  0,  1,  4,  5,  1, 12,  1,  1,  1,  3,  4,  1,  2,  1,  1,  0,  1,  2],
 [ 0,  0,  0,  3,  0,  0,  3,  1,  1,  1,  6,  2,  1,  2,  3,  3,  1,  1,  0,  0,  0,  0],
 [ 0,  1,  2,  3,  0,  0,  1,  2,  1,  1,  2, 12,  4,  5,  2,  1,  1,  1,  0,  0,  1,  0],
 [ 0,  2,  3,  3,  1,  0,  1,  1,  1,  1,  1,  4, 13,  3,  4,  0,  3,  0,  0,  0,  0,  0],
 [ 2,  1,  5,  4,  2,  2,  4,  4,  1,  3,  2,  5,  3, 24,  6,  3,  5,  3,  1,  1,  3,  1],
 [ 4,  1,  5,  5,  4,  4,  7,  7,  1,  4,  3,  2,  4,  6, 25,  4,  5,  2,  0,  2,  3,  2],
 [ 1,  0,  1,  2,  1,  0,  3,  2,  1,  1,  3,  1,  0,  3,  4,  6,  1,  2,  1,  1,  1,  0],
 [ 0,  0,  4,  4,  1,  0,  3,  2,  1,  2,  1,  1,  3,  5,  5,  1, 12,  2,  0,  0,  0,  1],
 [ 1,  0,  1,  3,  1,  1,  2,  3,  1,  1,  1,  1,  0,  3,  2,  2,  2,  8,  0,  1,  1,  0],
 [ 1,  1,  1,  1,  0,  0,  0,  1,  0,  1,  0,  0,  0,  1,  0,  1,  0,  0, 10,  0,  0,  1],
 [ 3,  0,  1,  1,  2,  1,  1,  2,  0,  0,  0,  0,  0,  1,  2,  1,  0,  1,  0, 10,  1,  0],
 [ 2,  0,  2,  1,  1,  0,  1,  2,  0,  1,  0,  1,  0,  3,  3,  1,  0,  1,  0,  1, 10,  0],
 [ 0,  1,  2,  0,  0,  1,  1,  2,  1,  2,  0,  0,  0,  1,  2,  0,  1,  0,  1,  0,  0,  7]
];

const array = ['Dark UI Colors', 'Dynamic Retry Delay', 'Avoid Extraneous Work',
  'Race-to-idle', 'Open Only When Necessary', 'Push Over Poll', 'Power Save Mode',
  'Power Awareness', 'Reduce Size', 'WiFi Over Cellular', 'Suppress Logs',
  'Batch Operations', 'Cache', 'Decrease Rate', 'User Knows Best', 'Inform Users',
  'Enough resolution', 'Sensor Fusion', 'Kill Abnormal Tasks',
  'No screen Interaction', 'Avoid Extra. Graph. & Anim.', 'Manual Sync - On Demand']

const colorArray = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
  '#42d4f4', '#f032e6', '#bfef45', '#fabebe', '#469990', '#e6beff', '#9A6324', '#fffac8',
  '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#a9a9a9', '#ffffff', '#000000']

const originalColor = ['#034e7b','#feb24c','#b10026','#238443','#fdbb84',
  '#ffffb2','#fed976'];

const maxValue = Math.max.apply(null, init_matrix.map(x => Math.max.apply(null, x)));
document.getElementById('rangeSlider').max = maxValue;
