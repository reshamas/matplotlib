import pytest
import platform

import matplotlib as mpl
from matplotlib.testing.decorators import check_figures_equal, image_comparison
import matplotlib.pyplot as plt


if not mpl.checkdep_usetex(True):
    pytestmark = pytest.mark.skip('Missing TeX of Ghostscript or dvipng')


@image_comparison(baseline_images=['test_usetex'],
                  extensions=['pdf', 'png'],
                  tol={'aarch64': 2.868, 'x86_64': 2.868}.get(platform.machine(), 0.3))
def test_usetex():
    mpl.rcParams['text.usetex'] = True
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.text(0.1, 0.2,
            # the \LaTeX macro exercises character sizing and placement,
            # \left[ ... \right\} draw some variable-height characters,
            # \sqrt and \frac draw horizontal rules, \mathrm changes the font
            r'\LaTeX\ $\left[\int\limits_e^{2e}'
            r'\sqrt\frac{\log^3 x}{x}\,\mathrm{d}x \right\}$',
            fontsize=24)
    ax.set_xticks([])
    ax.set_yticks([])


@check_figures_equal()
def test_unicode_minus(fig_test, fig_ref):
    mpl.rcParams['text.usetex'] = True
    fig_test.text(.5, .5, "$-$")
    fig_ref.text(.5, .5, "\N{MINUS SIGN}")


def test_mathdefault():
    plt.rcParams["axes.formatter.use_mathtext"] = True
    fig = plt.figure()
    fig.add_subplot().set_xlim(-1, 1)
    # Check that \mathdefault commands generated by tickers don't cause
    # problems when later switching usetex on.
    mpl.rcParams['text.usetex'] = True
    fig.canvas.draw()
