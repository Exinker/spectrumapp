from enum import Enum


class RedOrangeYellowGreenColorset(Enum):
    """https://www.schemecolor.com/red-orange-green-gradient.php"""

    RED = '#FF0D0D'
    ORANGE = '#FF8E15'
    YELLOW = '#FAB733'
    GREEN = '#69B34C'


class BluePinkColorset(Enum):

    BLUE = (0, 0.4470, 0.7410)
    PINK = (1, 0.4470, 0.7410)


class DatasetsColorset(Enum):

    TRAIN = (0.17254902, 0.62745098, 0.17254902, 0.5)  # '#009300'
    VALID = (1., 0.49803922, 0.05490196, 0.5)
    TEST = (0.12156863, 0.46666667, 0.70588235, 0.5)  # '#000096'


class FactorInfluenceColorset(Enum):

    ANALYTICAL = '#FFE1CC'
    INTERFERING = '#EBFFCC'
    MACROCOMPONENT = '#FFFACC'


class IntensityKingColorset(Enum):

    AMPLITUDE = '#2ca02c'
    LINEAR = '#ff7f0e'
    NEAREST = '#1f77b4'
    SHAPE = '#9467bd'


class MarkColorset(Enum):

    IS_NOT_ACTIVE = '#707C80'
    SELECTED = (0, 0.37254902, 0.88627451, .5)
