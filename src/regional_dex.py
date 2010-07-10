#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""A collection of all regional pokedexes."""

IDS = {
  "kanto": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
    19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,
    37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54,
    55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72,
    73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90,
    91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107,
    108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122,
    123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137,
    138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151],

  "johto": [0, 152, 153, 154, 155, 156, 157, 158, 159, 160, 16, 17, 18, 21, 22,
    163, 164, 19, 20, 161, 162, 172, 25, 26, 10, 11, 12, 13, 14, 15, 165, 166,
    167, 168, 74, 75, 76, 41, 42, 169, 173, 35, 36, 174, 39, 40, 175, 176, 27,
    28, 23, 24, 206, 179, 180, 181, 194, 195, 92, 93, 94, 201, 95, 208, 69, 70,
    71, 187, 188, 189, 46, 47, 60, 61, 62, 186, 129, 130, 118, 119, 79, 80,
    199, 43, 44, 45, 182, 96, 97, 63, 64, 65, 132, 204, 205, 29, 30, 31, 32,
    33, 34, 193, 469, 191, 192, 102, 103, 185, 202, 48, 49, 123, 212, 127, 214,
    109, 110, 88, 89, 81, 82, 100, 101, 190, 424, 209, 210, 37, 38, 58, 59,
    234, 183, 184, 50, 51, 56, 57, 52, 53, 54, 55, 66, 67, 68, 236, 106, 107,
    237, 203, 128, 241, 240, 126, 238, 124, 239, 125, 122, 235, 83, 177, 178,
    211, 72, 73, 98, 99, 213, 120, 121, 90, 91, 222, 223, 224, 170, 171, 86,
    87, 108, 463, 114, 465, 133, 134, 135, 136, 196, 197, 116, 117, 230, 207,
    225, 220, 221, 473, 216, 217, 231, 232, 226, 227, 84, 85, 77, 78, 104, 105,
    115, 111, 112, 198, 228, 229, 218, 219, 215, 200, 137, 233, 113, 242, 131,
    138, 139, 140, 141, 142, 143, 1, 2, 3, 4, 5, 6, 7, 8, 9, 144, 145, 146,
    243, 244, 245, 147, 148, 149, 246, 247, 248, 249, 250, 150, 151, 251],

  "hoenn": [0, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264,
    265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279,
    280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 63, 64, 65, 290, 291,
    292, 293, 294, 295, 296, 297, 118, 119, 129, 130, 298, 183, 184, 74, 75,
    76, 299, 300, 301, 41, 42, 169, 72, 73, 302, 303, 304, 305, 306, 66, 67,
    68, 307, 308, 309, 310, 311, 312, 81, 82, 100, 101, 313, 314, 43, 44, 45,
    182, 84, 85, 315, 316, 317, 318, 319, 320, 321, 322, 323, 218, 219, 324,
    88, 89, 109, 110, 325, 326, 27, 28, 327, 227, 328, 329, 330, 331, 332, 333,
    334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348,
    174, 39, 40, 349, 350, 351, 120, 121, 352, 353, 354, 355, 356, 357, 358,
    359, 37, 38, 172, 25, 26, 54, 55, 360, 202, 177, 178, 203, 231, 232, 127,
    214, 111, 112, 361, 362, 363, 364, 365, 366, 367, 368, 369, 222, 170, 171,
    370, 116, 117, 230, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381,
    382, 383, 384, 385, 386],

  "sinnoh": [0, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398,
    399, 400, 401, 402, 403, 404, 405, 63, 64, 65, 129, 130, 406, 315, 407, 41,
    42, 169, 74, 75, 76, 95, 208, 408, 409, 410, 411, 66, 67, 68, 54, 55, 412,
    413, 414, 265, 266, 267, 268, 269, 415, 416, 417, 418, 419, 420, 421, 422,
    423, 214, 190, 424, 425, 426, 427, 428, 92, 93, 94, 200, 429, 198, 430,
    431, 432, 118, 119, 339, 340, 433, 358, 434, 435, 307, 308, 436, 437, 77,
    78, 438, 185, 439, 122, 440, 113, 242, 173, 35, 36, 441, 172, 25, 26, 163,
    164, 442, 443, 444, 445, 446, 143, 201, 447, 448, 194, 195, 278, 279, 203,
    449, 450, 298, 183, 184, 451, 452, 453, 454, 455, 223, 224, 456, 457, 72,
    73, 349, 350, 458, 226, 459, 460, 215, 461, 480, 481, 482, 483, 484, 490],

  "isshu": [0, 494, 495, 496, 497, 498, 499, 500, 501, 502]
}
