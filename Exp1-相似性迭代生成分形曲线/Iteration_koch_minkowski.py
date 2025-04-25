import numpy as np
import sys
import os
from pathlib import Path
import unittest

# 添加父目录到路径，以便导入学生代码
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from solution.Iteration_koch_minkowski_solution import koch_generator, minkowski_generator
from Iteration_koch_minkowski import koch_generator, minkowski_generator

class TestFractalCurves(unittest.TestCase):
    def test_koch_generator_level1(self):
        import numpy as np
        u = np.array([0, 1])
        points = koch_generator(u, 1)
        self.assertIsInstance(points, np.ndarray)
        self.assertEqual(len(points), 5)

    def test_koch_generator_level2(self):
        import numpy as np
        u = np.array([0, 1])
        points = koch_generator(u, 2)
        self.assertIsInstance(points, np.ndarray)
        self.assertEqual(len(points), 20)  # 修改为20

    def test_minkowski_generator_level1(self):
        import numpy as np
        u = np.array([0, 1])
        points = minkowski_generator(u, 1)
        self.assertIsInstance(points, np.ndarray)
        self.assertEqual(len(points), 10)

    def test_minkowski_generator_level2(self):
        import numpy as np
        u = np.array([0, 1])
        points = minkowski_generator(u, 2)
        self.assertIsInstance(points, np.ndarray)
        self.assertEqual(len(points), 90)  # 修改为90

if __name__ == "__main__":
    unittest.main()
