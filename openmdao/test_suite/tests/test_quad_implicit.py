import unittest

import numpy as np

from openmdao.api import Problem
from openmdao.test_suite.components.quad_implicit import QuadraticComp



class TestQuadImplicit(unittest.TestCase):



    def test_check_partials_for_docs(self):

        from openmdao.api import Problem
        from openmdao.test_suite.components.quad_implicit import QuadraticComp

        p = Problem()

        p.model.add_subsystem('quad', QuadraticComp())

        p.setup()

        p.check_partials(compact_print=True)

    def test_check_partials(self):
        p = Problem()

        p.model.add_subsystem('quad', QuadraticComp())

        p.setup()

        check = p.check_partials(suppress_output=True)

        for out_name, of in check.items():
            for i_name, wrt in of.items():
                J_fwd = wrt['J_fwd']
                J_fd = wrt['J_fd']
                if J_fd > 1e-5:
                    err = np.abs(J_fwd-J_fd)/J_fd
                else:
                    err = np.abs(J_fwd-J_fd)
                self.assertLess(err, 1e-4)


if __name__ == "__main__":
    unittest.main()
