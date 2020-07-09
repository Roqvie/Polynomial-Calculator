from io import BytesIO
import matplotlib.pyplot as plot

def _render_tex(tex_string, format='svg', fontsize=16):
    """Render TeX string to svg-file"""

    # Create figure
    plot.rc('mathtext', fontset='cm')
    figure = plot.figure(figsize=(0.01, 0.01))
    figure.text(0, 0, tex_string, fontsize=fontsize, color='black')
    # Save rendered figure in bytes
    output = BytesIO()
    figure.savefig(output, format=format, dpi=300, transparent=True, bbox_inches='tight', pad_inches=0.02)
    plot.close(fig=figure)
    output.seek(0)

    return output.read()


def _create_tex_string(power, base):
    """Generate TeX-based string from parameters"""

    if power == 0:
        return r'1'
    elif power == 1:
        return r'%s' % base
    else:
        return r'%s^{%s}' % (base, power)
