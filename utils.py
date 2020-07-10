from io import BytesIO
import matplotlib.pyplot as plot


def render_tex(tex_string: str, format='svg', fontsize=16):
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


def create_tex_string(power: int, base: str) -> str:
    """Generate TeX-based string from parameters"""

    if power == 0:
        return r'1'
    elif power == 1:
        return r'%s' % base
    else:
        return r'%s^{%s}' % (base, power)


def _offset(vector: list) -> list:
    """Moves the list to the right by an element"""

    new_vector = [0]
    new_vector.extend(vector[:-1])
    return new_vector


def _new_vector(vector: list, polynomial: list) -> list:
    """Adds list items by xor"""

    vector = [vector[i] ^ polynomial[i] for i in range(len(vector))]
    return vector


def get_field(n: int, polynomial: list) -> list:
    """Generate Galois field from given primitive polynomial"""

    # Create primitive polynomial with degrees from polynomial list
    poly = [0]*n
    for i in range(len(poly)):
        poly[i] = 1 if i in polynomial else 0

    # Generate vectors for field
    vect = list(map(int, list('1'.ljust(n,'0'))))
    field = [vect,]
    new_vect = _offset(vect)
    while new_vect not in field:
        field.append(new_vect)
        if new_vect[-1] == 1:
            new_vect = _offset(new_vect)
            new_vect = _new_vector(new_vect, poly)
        else:
            new_vect = _offset(new_vect)
    new_vect = _offset(new_vect)
    new_vect = _new_vector(new_vect, poly)
    field.append(new_vect)

    return field
